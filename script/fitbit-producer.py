# Run the define function for generate the data (still need enhancement in the logic)

from kafka import KafkaProducer
import json, time, random
import pandas as pd
from datetime import datetime, timedelta

producer = KafkaProducer(
    bootstrap_servers = ['localhost:9092'],
    value_serializer = lambda v: json.dumps(v).encode('utf-8')
)

def generate_morning_health_data(num_athletes=10):
    data = []
    
    current_time = datetime.now()
    
    # Determine the sleep and wake time
    # So everyone has to sleep at 10 PM and wake up at 6 PM
    sleep_start = current_time.replace(hour=22, minute=0, second=0)  # 10:00 PM
    sleep_end = current_time.replace(hour=6, minute=0, second=0)  # 6:00 AM
    
    # decision by current real time
    if current_time > sleep_end:
        sleep_end = current_time # Everyone has to wake up and keep the sleep_end at the 6 AM
        
    for athlete_id in range(1, num_athletes + 1):
        sleep_duration = round(random.uniform(5, 9), 1)
        
        # sleep quality based on the duration
        if sleep_duration < 6:
            sleep_quality = random.randint(1, 4)
        elif sleep_duration < 8:
            sleep_quality = random.randint(5, 7)
        else:
            sleep_quality = random.randint(8, 10)
        
        # Resting heart rate and cardiac variability
        resting_heart_rate = random.randint(40, 60)
        heart_rate_variability = round(random.uniform(50, 70), 1)
        
        # Body temperature
        body_temperature = round(random.uniform(36.5, 37.2), 1)

        # Stress level based on sleep quality dan sleep duration
        if sleep_quality < 5 or sleep_duration < 6:
            stress_level = random.randint(7, 10)
        elif sleep_quality < 8:
            stress_level = random.randint(4, 6)
        else:
            stress_level = random.randint(1, 3)
        
        # Hydration level
        hydration_level = round(random.uniform(3, 5), 1)

        # Append to the list
        data.append({
            'athlete_id': athlete_id,
            'date': current_time.date().isoformat(),
            'time': current_time.time().isoformat(),
            'sleep_duration': sleep_duration,
            'sleep_quality': sleep_quality,
            'resting_heart_rate': resting_heart_rate,
            'heart_rate_variability': heart_rate_variability,
            'body_temperature': body_temperature,
            'stress_level': stress_level,
            'hydration_level': hydration_level
        })

    # Convert list to dataframe
    df = pd.DataFrame(data)
    return df

try:
    while True:            
        morning_health_data = generate_morning_health_data(num_athletes=10)
        print(morning_health_data)

        topic_name = 'fitbit_data'
        for index, row in morning_health_data.iterrows():
            producer.send(topic_name, value=row.to_dict())
            
        producer.flush()
        print("Morning wellness data sent to Kafka Topic!")

        # Delay 1 sec for every event/rows
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped user by user.")

finally:
    producer.close()
    print("Closed Kafka producer.")
