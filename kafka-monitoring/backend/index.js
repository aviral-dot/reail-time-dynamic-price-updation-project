const express = require("express");
const WebSocket = require("ws");
const { MongoClient } = require("mongodb");
const cors = require("cors");

const app = express();
app.use(cors());

const server = app.listen(3001, () => console.log("🚀 Backend running on port 3001"));
const wss = new WebSocket.Server({ server });

const MONGO_URI = process.env.MONGO_URI || 
  "mongodb://admin:password@mongo1:27017,mongo2:27017/?replicaSet=rs0&authSource=admin&readPreference=primary";

async function connectWithRetry() {
  try {
    const client = await MongoClient.connect(MONGO_URI);
    console.log("✅ Connected to MongoDB");

    const db = client.db("pricing");
    const collection = db.collection("price_history");

    const changeStream = collection.watch();

    changeStream.on("change", async (change) => {
      console.log("🔔 MongoDB Change Event:", change);
      const doc = await collection.findOne({ _id: change.documentKey._id });
      const message = JSON.stringify({
        region: doc._id,
        predicted_price: doc.predicted_price,
        timestamp: doc.timestamp
      });

      wss.clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
          client.send(message);
        }
      });
    });

  } catch (err) {
    console.error("❌ MongoDB connection failed. Retrying in 5s...", err.message);
    setTimeout(connectWithRetry, 5000);
  }
}

connectWithRetry();

