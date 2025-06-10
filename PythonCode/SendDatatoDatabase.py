'''
Nhiệm vụ chính của Python code này là:
1. Xử lý Packet từ Arduino
2. Rút data từ Packet
3. Thực hiện đồng thời hai việc:
    1. Gửi dữ liệu lên Firebase Realtime Database
    2. Gửi dữ liệu lên Neon database
4. Vòng lặp While được sử dụng để thực hiện liên tục việc đọc dữ liệu từ cổng Serial và gửi dữ liệu lên hai cơ sở dữ liệu
5. Lưu ý:
    1. Cơ sở dữ liệu Firebase Realtime Database được sử dụng để lưu trữ dữ liệu theo thời gian thực
    2. Cơ sở dữ liệu Neon database được sử dụng để lưu trữ dữ liệu lâu dài phục vụ cho việc phân tích và báo cáo
'''
import serial
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import psycopg2
from psycopg2 import pool

'''
Cài đặt các thư viện cần thiết:
    pip install -r requirements.txt
'''

conn_string = ""

port = '/dev/tty.usbserial-0001'
baud_rate = 9600  

path = credentials.Certificate("SmartAgricultureApplicationsFirebaseServiceAccount.json")
firebase_admin.initialize_app(path, {
    'databaseURL': '' })

def PacketProcessing(raw_packet):
    """
    Xử lý packet logic từ Arduino
    Chuyển đổi dữ liệu từ string sang dictionary để phù hợp với Firebase Realtime Database
    """
    data_values = raw_packet.split(",")                            # Cái này là một cái DICTIONARY chứa các key-value
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
    Gửi dữ liệu lên Firebase Realtime Database
    """
    ref = db.reference("sensor_data")
    ref.push(data)                                                 # push để thêm với timestamp, hoặc ref.set(data) để ghi đè

def transform_data_to_tuple(data):
    """
    Chuyển đổi dữ liệu từ dictionary sang tuple theo thứ tự:
    (Light, Temperature, Air_Humidity, CO2, Smoke, Soil_humidity)
    Để gửi dữ liệu lên Neon database
    """
    return (
        data["Light"],
        data["Temperature"],
        data["Air_Humidity"],
        data["CO2"],
        data["Smoke"],
        data["Soil_humidity"]
    )

# Logic xử lý chính
try:
    connect = serial.Serial(port, baud_rate) # Mở Serial 
    
    # Phần xử lý cho Neon Serverless database
    conn_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        dsn=conn_string
    )
    conn = conn_pool.getconn()
    cur = conn.cursor()

    # Đẩy dữ liệu realtime
    while True:
        if connect.in_waiting > 0:
            Packet = connect.readline().decode('utf-8').strip()    # Đọc dữ liệu từ cổng serial -> readline() để đọc từng dòng (Cho đến khi gặp '\n') | decode('utf-8') để chuyển đổi chuỗi bytes sang string | strip() để loại bỏ các ký tự không cần thiết (như '\r' và '\n') ở đầu và cuối string
            print(Packet)
            data = PacketProcessing(Packet)
            SendDataToFirebase(data)
            cur.execute("""
                    INSERT INTO sensor_data (Light, Temperature, Air_Humidity, CO2, Smoke, Soil_humidity)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, transform_data_to_tuple(data))
            conn.commit()
        time.sleep(0.1)                                            # White true sẽ dừng lại trong 0.1s trước khi bắt đầu vòng lặp mới


except serial.SerialException as e:                                # Xử lý các ngoại lệ
    print(f"Error: {e}") 
except KeyboardInterrupt:
    print(". . . . . . . . . . . . . . . . . . . .")
finally:
    connect.close()