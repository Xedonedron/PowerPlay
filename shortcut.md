# Menjalankan image postgres:13 yang punya volume biar nempel di folder terkait
## tujuannya biar bisa ngeload data ke postgres

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

docker run --name postgres_kafka -e POSTGRES_PASSWORD=root -p 5432:5432 -d postgres:13

# start image pgadmin pakai network
## NOTE, host name/address nya ini bukan localhost, melainkan nama database nya postgres (pg-database) - gatau kenapa, coba kulik ke chatgpt aja
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

- cek topic
  ```
bin/kafka-topics.sh --describe --topic iot_sensors  --bootstrap-server localhost:9092
```

- consume data hasil dari topic
  ```
bin/kafka-console-consumer.sh --topic fitbit_data  --bootstrap-server localhost:9092 --from-beginning
```

- consume topic on group (buat testing consumer)
```
bin\windows\kafka-console-consumer.bat --topic iot_sensors --bootstrap-server localhost:9092 --from-beginning --group iot_tools
```

