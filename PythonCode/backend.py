"""
Mô tả:
    Phần backend xử lý logic chính của ứng dụng web, chịu trách nhiệm giao tiếp với
    Firebase Realtime Database và Neon Database để lấy, xử lý và hiển thị dữ liệu
    các cảm biến. Ngoài ra, file còn định nghĩa các hàm phục vụ cảnh báo qua Telegram.

Chức năng chính:
    1. Định nghĩa các hàm:
        - Lấy dữ liệu cảm biến mới nhất từ Firebase.
        - Lấy và hiển thị dữ liệu từ Neon Database dưới dạng bảng.
        - Gửi cảnh báo khói qua Telegram cho người dùng khi vượt ngưỡng.
    2. Cung cấp các tiện ích backend để ứng dụng web sử dụng trực tiếp.
    3. Hỗ trợ hiển thị dữ liệu theo thời gian thực trên giao diện Streamlit.

Yêu cầu:
    - Cài đặt các thư viện cần thiết:
        pip install -r requirements.txt
"""
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time
import psycopg2
from psycopg2 import pool
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import requests

def get_latest_sensor_data():
    """
    Lấy bản ghi dữ liệu cảm biến mới nhất từ Firebase Realtime Database.

    Trả về:
        dict: Dictionary chứa giá trị của bản ghi cảm biến mới nhất, 
        hoặc rỗng nếu không có dữ liệu.
    """
    ref = db.reference("sensor_data")
    data = ref.order_by_key().limit_to_last(1).get()
    if data:
        for key in data:
            return data[key]
    return {}

def display_data_table(cur):
    """
    Lấy và HIỂN THỊ dữ liệu cảm biến mới nhất dưới dạng bảng.

    Mô tả:
        Hàm này truy vấn cơ sở dữ liệu (Neon) để lấy tối đa 35 bản ghi
        mới nhất từ bảng `sensor_data`, sau đó chuyển dữ liệu thành 
        một DataFrame của Pandas để dễ dàng xử lý hoặc hiển thị.

    Tham số:
        cur (psycopg2.cursor): Đối tượng con trỏ cơ sở dữ liệu PostgreSQL.

    Giá trị trả về:
        pandas.DataFrame: Bảng dữ liệu chứa các cột:
            - id
            - light
            - temperature
            - air_humidity
            - co2
            - smoke
            - soil_humidity
            - timestamp
    """
    cur.execute("SELECT * " \
                "FROM sensor_data " \
                "ORDER BY timestamp " \
                "DESC LIMIT 35")
    rows = cur.fetchall()
    columns = ['id', 'light', 'temperature', 'air_humidity', 'co2', 'smoke', 'soil_humidity', 'timestamp']
    df = pd.DataFrame(rows, columns=columns)
    return df

def send_telegram_alert(message):
    """
    Gửi thông báo cảnh báo đến User thông qua Telegram.

    Tham số:
        message (str): Nội dung thông báo cần gửi.

    Trả về:
        requests.Response: Đối tượng phản hồi từ API Telegram.
    """
    bot_token = '########################################'
    chat_id = '########'
    url = f"########################################"
    data = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=data)
    # return response.json()

def check_smoke_alert(latest_data, threshold):
    """
    Kiểm tra nồng độ khói mới nhất và gửi cảnh báo nếu vượt ngưỡng cho phép.

    Tham số:
        latest_data (dict): Dictionary chứa dữ liệu cảm biến mới nhất, 
            bao gồm khóa 'Smoke' cho giá trị nồng độ khói (ppm).
        threshold (float): Ngưỡng nồng độ khói để kích hoạt cảnh báo.

    Trả về:
        None
    """
    if 'Smoke' in latest_data and latest_data['Smoke'] > threshold:
        message = f"🚨 CẢNH BÁO: Nồng độ khói vượt ngưỡng! Giá trị hiện tại: {latest_data['Smoke']} ppm \n🔥CÓ THỂ CHÁY!"
        response = send_telegram_alert(message)