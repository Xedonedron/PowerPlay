from kafka import KafkaProducer
import json, time, random
import pandas as pd
from datetime import datetime, timedelta

producer = KafkaProducer(
    bootstrap_servers = ['localhost:9092'],
    value_serializer = lambda v: json.dumps(v).encode('utf-8')
)

def generate_morning_health_data(num_athletes=10):
    # List untuk menampung data kesehatan pagi
    data = []
    
    # Ambil waktu saat ini
    current_time = datetime.now()
    
    # Tentukan waktu tidur dan bangun
    sleep_start = current_time.replace(hour=22, minute=0, second=0)  # 10:00 PM
    sleep_end = current_time.replace(hour=6, minute=0, second=0)  # 6:00 AM
    
    # Jika sekarang waktu sudah lewat jam 6 pagi, batasi waktu tidur
    if current_time > sleep_end:
        sleep_end = current_time  # Waktu bangun adalah sekarang
        
    # Rentang nilai untuk setiap metrik kesehatan
    for athlete_id in range(1, num_athletes + 1):
        # Random sleep duration dalam rentang 5 hingga 9 jam
        sleep_duration = round(random.uniform(5, 9), 1)
        
        # Tentukan sleep quality berdasarkan durasi tidur
        if sleep_duration < 6:
            sleep_quality = random.randint(1, 4)
        elif sleep_duration < 8:
            sleep_quality = random.randint(5, 7)
        else:
            sleep_quality = random.randint(8, 10)
        
        # Resting heart rate dan variabilitas jantung
        resting_heart_rate = random.randint(40, 60)
        heart_rate_variability = round(random.uniform(50, 70), 1)
        
        # Body temperature
        body_temperature = round(random.uniform(36.5, 37.2), 1)

        # Stress level berdasarkan sleep quality dan durasi tidur
        if sleep_quality < 5 or sleep_duration < 6:
            stress_level = random.randint(7, 10)
        elif sleep_quality < 8:
            stress_level = random.randint(4, 6)
        else:
            stress_level = random.randint(1, 3)
        
        # Tingkat hidrasi
        hydration_level = round(random.uniform(3, 5), 1)

        # Tambahkan data ke list
        data.append({
            'athlete_id': athlete_id,
            'date': current_time.date().isoformat(),  # Tanggal sekarang
            'time': current_time.time().isoformat(),  # Waktu sekarang
            'sleep_duration': sleep_duration,
            'sleep_quality': sleep_quality,
            'resting_heart_rate': resting_heart_rate,
            'heart_rate_variability': heart_rate_variability,
            'body_temperature': body_temperature,
            'stress_level': stress_level,
            'hydration_level': hydration_level
        })

    # Convert list ke dataframe
    df = pd.DataFrame(data)
    return df

# Generate data kesehatan pagi untuk 10 atlet pada tanggal tertentu
try:
    while True:            
        morning_health_data = generate_morning_health_data(num_athletes=10)
        print(morning_health_data)

        topic_name = 'fitbit_data'
        for index, row in morning_health_data.iterrows():
            producer.send(topic_name, value=row.to_dict())
            
        # Flush dan cetak informasi untuk debugging
        producer.flush()
        print("Data kesehatan pagi berhasil dikirim ke topic Kafka!")

        # Delay selama 1 detik sebelum menghasilkan data lagi
        time.sleep(1)

except KeyboardInterrupt:
    print("Penghentian program oleh pengguna.")

finally:
    # Tutup producer jika loop berhenti
    producer.close()
    print("Kafka producer ditutup.")
