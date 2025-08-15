"""
Mô tả:
    Chương trình Python này kết nối đến Neon Database và tạo bảng chứa dữ liệu
    cảm biến.

Chức năng chính:
    1. Kết nối đến Neon Database bằng PostgreSQL.
    2. Tạo bảng với các trường dữ liệu cảm biến cần thiết.
    3. Thay thế thao tác tạo bảng thủ công trên Neon bằng việc thực thi trực tiếp qua Python.

Yêu cầu:
    - Chỉ chạy file này một lần khi khởi tạo dự án.
"""
import psycopg2
from psycopg2 import pool

conn_string = "postgresql://neondb_owner:#############################################/neondb?sslmode=require"

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

except psycopg2.OperationalError as e:
    print(f"Lỗi: {e}")
except Exception as e:
    print(f"Lỗi khác: {e}")
finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn_pool.putconn(conn)
    if 'conn_pool' in locals():
        conn_pool.closeall()