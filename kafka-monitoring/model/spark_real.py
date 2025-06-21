from pyspark.sql import SparkSession
from pyspark.sql.avro.functions import from_avro
from pyspark.sql.functions import to_timestamp, col, last
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, TimestampType
import joblib
from pyspark.sql.functions import expr
import numpy as np
from pyspark.files import SparkFiles
import xgboost as xgb

def main():
    try:
        print("Starting Spark session")
        spark = SparkSession.builder \
        .appName("DynamicPricingUpdation") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.executor.instances", "1") \
        .config("spark.executor.cores", "2") \
        .config("spark.executor.memory", "2g") \
        .config("spark.task.cpus", "1") \
        .config("spark.driver.cores", "1") \
        .config("spark.driver.memory", "1g") \
        .config("spark.sql.shuffle.partitions", "2") \
        .config("spark.default.parallelism", "2") \
        .getOrCreate()
        print("Spark session started")

        sc = spark.sparkContext

        print("Broadcasting models")
        scaler_b = sc.broadcast(joblib.load(SparkFiles.get("scaler.pkl")))
        region_encoder_b = sc.broadcast(joblib.load(SparkFiles.get("region_encoder.pkl")))
        weather_encoder_b = sc.broadcast(joblib.load(SparkFiles.get("weather_encoder.pkl")))
        model = xgb.Booster()
        model.load_model(SparkFiles.get("xgb_model.json"))
        model_b = sc.broadcast(model)
        print("Broadcast completed")

        output_schema = StructType([
            StructField("timestamp", TimestampType()),
            StructField("hour", IntegerType()),
            StructField("day_of_week", IntegerType()),
            StructField("region", StringType()),
            StructField("weather", StringType()),
            StructField("demand", IntegerType()),
            StructField("inventory", IntegerType()),
            StructField("competitor_price", FloatType()),
            StructField("actual_price", FloatType()),
            StructField("demand_inventory_ratio", FloatType()),
            StructField("is_peak_hour", IntegerType()),
            StructField("is_weekend", IntegerType()),
            StructField("predicted_price", FloatType())
        ])

        def predict_batch(pdf_iter):
            print("Starting batch prediction")

            scaler = scaler_b.value
            region_encoder = region_encoder_b.value
            weather_encoder = weather_encoder_b.value
            model = model_b.value

            region_decoder = {i: label for i, label in enumerate(region_encoder.classes_)}
            weather_decoder = {i: label for i, label in enumerate(weather_encoder.classes_)}

            for pdf in pdf_iter:
                try:
                    print(f"Processing batch with {len(pdf)} rows")
                    print("Columns in prediction batch:", list(pdf.columns))

                    pdf['demand_inventory_ratio'] = pdf['demand'] / (pdf['inventory'] + 1e-5)
                    pdf['is_peak_hour'] = pdf['hour'].isin([7, 8, 17, 18]).astype(int)
                    pdf['is_weekend'] = pdf['day_of_week'].isin([5, 6]).astype(int)

                    pdf['region'] = region_encoder.transform(pdf['region'])
                    pdf['weather'] = weather_encoder.transform(pdf['weather'])
                    
                    pdf['competitor_price_raw'] = pdf['competitor_price'].copy()

                    scaled_features = ['demand', 'inventory', 'competitor_price', 'demand_inventory_ratio']
                    pdf[scaled_features] = scaler.transform(pdf[scaled_features])

                    print(f"Processing batch with {len(pdf)} rows")

                    feature_columns = ['hour', 'day_of_week', 'region', 'weather',
                   'demand', 'inventory', 'competitor_price',
                   'demand_inventory_ratio', 'is_peak_hour', 'is_weekend']

                    input_array = pdf[feature_columns].to_numpy(dtype=np.float32)

                    dmatrix = xgb.DMatrix(input_array, feature_names=feature_columns)

                    preds = model.predict(dmatrix)
                    pdf['predicted_price'] = preds

                    pdf['region'] = pdf['region'].map(region_decoder)
                    pdf['weather'] = pdf['weather'].map(weather_decoder)

                    pdf['competitor_price'] = pdf['competitor_price_raw']
                    pdf.drop(columns=['competitor_price_raw'], inplace=True)


                    yield pdf[output_schema.fieldNames()]

                except Exception as e:
                    print(f"Error processing batch: {e}")
                    raise e

        kafka_bootstrap_servers = "broker:29092"
        topic = "my-topic1"

        avro_schema = """
        {
          "type": "record",
          "name": "PriceEvent",
          "fields": [
            {"name": "timestamp", "type": "string"},
            {"name": "hour", "type": "int"},
            {"name": "day_of_week", "type": "int"},
            {"name": "region", "type": "string"},
            {"name": "weather", "type": "string"},
            {"name": "demand", "type": "int"},
            {"name": "inventory", "type": "int"},
            {"name": "competitor_price", "type": "float"},
            {"name": "actual_price", "type": "float"}
          ]
        }
        """

        

        kafka_raw_df = spark.readStream.format("kafka") \
            .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
            .option("subscribe", topic) \
            .option("startingOffsets", "latest") \
            .load()

        kafka_df = kafka_raw_df.select(
        expr("substring(value, 6, length(value)-5)").alias("avro_value"))\
            .select(from_avro(col("avro_value"), avro_schema).alias("data")) \
            .select("data.*") \
            .withColumn("timestamp", to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss")) \
            .filter(col("timestamp").isNotNull())

        enriched_df = kafka_df.mapInPandas(predict_batch, schema=output_schema)

        result_df = enriched_df.groupBy("region").agg(
            last("timestamp").alias("timestamp"),
            last("competitor_price").alias("competitor_price"),
            last("predicted_price").alias("predicted_price")
        ).select("timestamp", "region", "competitor_price", "predicted_price")

        print("Starting streaming query")
        query = result_df.writeStream \
            .outputMode("complete") \
            .format("console") \
            .option("truncate", "false") \
            .option("checkpointLocation", "file:///tmp/checkpoints/dynamic_pricing") \
            .trigger(processingTime="15 seconds") \
            .start()

        query.awaitTermination()

    except Exception as e:
        print(f"Exception in main: {e}")
        raise e

if __name__ == "__main__":
    main()



