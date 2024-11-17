# Start the postgres:13 image and attach it with the volume according to the directory 

```
docker run -d\
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="kafka_stream" \
  -v c:/Xedonedron/Learn/kafka/PowerPlay/postgres_db:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name postgres_kafka \
  postgres:13
```
# Run the built container
docker run --name postgres_kafka -e POSTGRES_PASSWORD=root -p 5432:5432 -d postgres:13

# start image pgadmin using network
## NOTE, the hostname/address is not "localhost", but the postgres databases name itself, dunno why
```
docker run -d \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 5433:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

## Kafka Commands
- create topic
```
bin/kafka-topics.sh --create --topic fitbit_data --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

- delete topic (sesuai kebutuhan)
  ```
bin/kafka-topics.sh --delete --topic iot_sensors --bootstrap-server localhost:9092
  ```

- check topic
  ```
bin/kafka-topics.sh --describe --topic iot_sensors  --bootstrap-server localhost:9092
```

- consume data from topic
  ```
bin/kafka-console-consumer.sh --topic fitbit_data  --bootstrap-server localhost:9092 --from-beginning
```

- consume topic on group (for testing consumer)
```
bin\windows\kafka-console-consumer.bat --topic iot_sensors --bootstrap-server localhost:9092 --from-beginning --group iot_tools
```

