'''
NHIỆM VỤ CỦA FILE PYTHON NÀY LÀ:
1. Tạo bản với các trường trong Neon database
    - Chỉ chạy một lần đầu tiên để tạo bảng -> Thay vì chạy query trên Neon thì chạy cái này ngầu hơn!
'''
import psycopg2
from psycopg2 import pool

conn_string = ""

try:
    conn_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        dsn=conn_string
    )
    conn = conn_pool.getconn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id SERIAL PRIMARY KEY,
            Light FLOAT,
            Temperature FLOAT,
            Air_Humidity FLOAT,
            CO2 FLOAT,
            Smoke FLOAT,
            Soil_humidity FLOAT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

# Xử lý ngoại lệ
except psycopg2.OperationalError as e:
    print(f"Lỗi: {e}")
except Exception as e:
    print(f"Lỗi khác: {e}")
finally:
    # Đóng cursor và trả kết nối về pool
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn_pool.putconn(conn)
    if 'conn_pool' in locals():
        conn_pool.closeall()