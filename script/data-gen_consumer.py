# For every message that get fetch from the topic, it'll loaded to the database
# So the concept will like doing OLTP database, event for every row of second the data

from kafka import KafkaConsumer
import psycopg2
import json

# Config consumer
consumer = KafkaConsumer(
    'fitbit_data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    group_id='second_app',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Config to connect the PostgreSQL Database
conn = psycopg2.connect(
    host="localhost",
    database="kafka_stream",
    user="root",
    password="root"
)
cur = conn.cursor()

# Create table
cur.execute("""
    CREATE TABLE IF NOT EXISTS morning_health_data (
        id SERIAL PRIMARY KEY,
        athlete_id INT,
        date DATE,
        time TIME,
        sleep_duration NUMERIC(3, 1),
        sleep_quality INT,
        resting_heart_rate INT,
        heart_rate_variability NUMERIC(4, 1),
        body_temperature NUMERIC(3, 1),
        stress_level INT,
        hydration_level NUMERIC(3, 1)
    );
""")
conn.commit()

# load the data
for message in consumer:
    data = message.value

    try:
        cur.execute("""
            INSERT INTO morning_health_data (
                athlete_id, date, time, sleep_duration, sleep_quality,
                resting_heart_rate, heart_rate_variability,
                body_temperature, stress_level, hydration_level
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['athlete_id'], data['date'], data['time'], 
            data['sleep_duration'], data['sleep_quality'], 
            data['resting_heart_rate'], data['heart_rate_variability'],
            data['body_temperature'], data['stress_level'], 
            data['hydration_level']
        ))

        conn.commit()
        print("Inserted data into morning_health_data")
        consumer.commit()

    except Exception as e:
        print(f'Error processing message: {e}')
        conn.rollback()

# Close connection
cur.close()
conn.close()
