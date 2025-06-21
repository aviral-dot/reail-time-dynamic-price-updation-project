
docker exec -it mongo1 mongosh -u admin -p password --authenticationDatabase admin

rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" }
  ]
})


use pricing

db.createCollection("price_history")


db.price_history.createIndex(
  { region: 1, timestamp: 1 },
  { unique: true }
)

