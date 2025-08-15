"""
Mô tả:
    Chương trình Python này thực hiện đọc dữ liệu cảm biến từ Arduino thông qua
    cổng Serial, sau đó xử lý và gửi đồng thời dữ liệu lên hai hệ thống cơ sở dữ liệu.

Chức năng chính:
    1. Đọc và xử lý packet dữ liệu từ Arduino.
    2. Trích xuất các giá trị cảm biến từ packet.
    3. Gửi dữ liệu lên:
        - Firebase Realtime Database: lưu trữ dữ liệu thời gian thực.
        - Neon Database: lưu trữ dữ liệu dài hạn phục vụ phân tích và hậu xử lý dữ liệu.
    4. Sử dụng vòng lặp `while` để duy trì việc thu thập và đồng bộ dữ liệu liên tục.

Yêu cầu:
    Cài đặt các thư viện cần thiết:
        pip install -r requirements.txt
"""
import serial
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import psycopg2
from psycopg2 import pool

conn_string = "postgresql://neondb_owner:#############################################/neondb?sslmode=require"

port = '/dev/tty.usbserial-0001'
baud_rate = 9600  

path = credentials.Certificate("SmartAgricultureApplicationsFirebaseServiceAccount.json")
firebase_admin.initialize_app(path, {
    'databaseURL': 'https://#############################################.firebaseio.com/' })

def PacketProcessing(raw_packet):
    """
    Phân tích gói dữ liệu cảm biến từ Arduino thành dạng dictionary.

    Tham số:
        raw_packet (str): Chuỗi CSV chứa dữ liệu cảm biến theo thứ tự:
            Light, Temperature, Air_Humidity, CO2, Smoke, Soil_humidity.

    Trả về:
        dict: Dictionary với giá trị float cho từng loại cảm biến, 
        sẵn sàng để lưu trữ lên Firebase Realtime Database.
    """
    data_values = raw_packet.split(",")                           
    data = {
        "Light": float(data_values[0]),
        "Temperature": float(data_values[1]),
        "Air_Humidity": float(data_values[2]),
        "CO2": float(data_values[3]),
        "Smoke": float(data_values[4]),
        "Soil_humidity": float(data_values[5])
    }
    return data

def SendDataToFirebase(data):
    """
    Gửi dữ liệu cảm biến lên Firebase Realtime Database.

    Tham số:
        data (dict): Dictionary chứa dữ liệu cảm biến, với các key:
            Light, Temperature, Air_Humidity, CO2, Smoke, Soil_humidity.
    """
    ref = db.reference("sensor_data")
    # .push() để thêm với timestamp, hoặc ref.set(data) để ghi đè
    ref.push(data)                                                

def transform_data_to_tuple(data):
    """
    Chuyển đổi dữ liệu cảm biến từ dictionary sang tuple.

    Tham số:
        data (dict): Dictionary chứa dữ liệu cảm biến, với các key:
            Light, Temperature, Air_Humidity, CO2, Smoke, Soil_humidity.

    Trả về:
        tuple: Tuple chứa giá trị cảm biến theo thứ tự:
            (Light, Temperature, Air_Humidity, CO2, Smoke, Soil_humidity).
    """
    return (
        data["Light"],
        data["Temperature"],
        data["Air_Humidity"],
        data["CO2"],
        data["Smoke"],
        data["Soil_humidity"]
    )

try:
    connect = serial.Serial(port, baud_rate) 
    
    conn_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        dsn=conn_string
    )
    conn = conn_pool.getconn()
    cur = conn.cursor()

    while True:
        if connect.in_waiting > 0:
            # Đọc 1 dòng dữ liệu từ Serial, giải mã UTF-8 và loại bỏ ký tự thừa
            Packet = connect.readline().decode('utf-8').strip()    
            print(Packet)

            # Chuyển đổi dữ liệu & gửi lên Firebase
            data = PacketProcessing(Packet)
            SendDataToFirebase(data)

            # Lưu dữ liệu vào Neon Database
            cur.execute("""
                    INSERT INTO sensor_data (Light, Temperature, Air_Humidity, CO2, Smoke, Soil_humidity)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, transform_data_to_tuple(data))
            conn.commit()
        time.sleep(0.1)                                           

except serial.SerialException as e:                               
    print(f"Error: {e}") 
except KeyboardInterrupt:
    print(". . . . . . . . . . . . . . . . . . . .")
finally:
    connect.close()