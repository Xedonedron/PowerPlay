import json
from kafka import KafkaConsumer
import psycopg2
from sqlalchemy import create_engine

if __name__ == '__main__':
    conn = psycopg2.connect(
                    host="localhost",
                    database="kafka_stream",
                    user="root",
                    password="root"
                    )

    # Create a cursor object
    cur = conn.cursor()

    # Kafka Consumer 
    consumer = KafkaConsumer(
        'iot_sensors',
        bootstrap_servers='localhost:9092',
        key_deserializer=lambda k: k.decode('utf-8') if k else None,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        group_id='iot_tools',
        auto_offset_reset='earliest', # CHANGE HERE (earliest or latest)
        enable_auto_commit=False # Mending pake consumer.commit() karena ini timer based sedangkan kita gak tau kapan error
    )
    
    for message in consumer:
        data = message.value
        key = message.key

        try:
            if key: # True
                table_name = f"data_{key}" # for table name based on key (iot objects)

                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        id SERIAL PRIMARY KEY,
                        timestamp TIMESTAMP,
                        value NUMERIC(5, 2)
                    );
                """)
            
            cur.execute(f"""
            INSERT INTO {table_name}
            (timestamp, value) 
            VALUES (%s, %s)
            """, (data[-1]['x'], data[-1]['y']))
            
            conn.commit()
            print(f"Inserted data into {table_name}: {data[-1]['y']}")
            consumer.commit()

        except Exception as e:
            print(f'Error processing message: {e}')
            conn.rollback()