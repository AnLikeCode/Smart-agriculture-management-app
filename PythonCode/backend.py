'''
NHIỆM VỤ CỦA FILE PYTHON NÀY LÀ:
1. Backend xử lý chính của ứng dụng web
2. Định nghĩa các hàm mà app xử dụng
'''
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time
import psycopg2
from psycopg2 import pool
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import requests

#========== BACKEND ==========
def get_latest_sensor_data():
    '''
    Chức năng: Lấy dữ liệu mới nhất từ Firebase theo thời gian thức
        - db.reference("sensor_data") tham chiếu đến bảng sensor_data trong Firebase
            - order_by_key() -> Sort lại các Key trong table
            - limit_to_last(1) -> Lấy cái sau cùng sau khi sort
            - get() trả về một dictionary chứa dữ liệu của bản ghi được CHỌN
        Vòng lặp for để lấy Dictionary trong Dictionary
            - Nếu không sử dụng for thì dùng cái này: next(iter(data.values())) -> hiệu quả tương tự
    '''
    ref = db.reference("sensor_data")
    data = ref.order_by_key().limit_to_last(1).get()
    if data:
        for key in data:
            return data[key]
    return {}

def display_data_table(cur):
    '''
    Chức năng: Lấy dữ liệu từ Neon và hiển thị dưới dạng bảng (Lấy 10 giá trị mới nhất của bảng)
        - cur.fetchall() lấy tất cả các dữ liệu từ Row truy vấn được gán vào biết rows
        - rows có kiểu dữ liệu là một list các tuple
    '''
    cur.execute("SELECT * " \
                "FROM sensor_data " \
                "ORDER BY timestamp " \
                "DESC LIMIT 35")
    rows = cur.fetchall()
    columns = ['id', 'light', 'temperature', 'air_humidity', 'co2', 'smoke', 'soil_humidity', 'timestamp']
    df = pd.DataFrame(rows, columns=columns)
    return df

def send_telegram_alert(message):
    '''
    Function gửi thông báo cháy đến Telegram 
    '''
    bot_token = ''
    chat_id = ''
    url = f""
    data = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=data)
    # return response.json()

def check_smoke_alert(latest_data, threshold):
    '''
    Chức năng: Kiểm tra giá trị khói mới nhất và gửi cảnh báo nếu vượt ngưỡng
    '''
    if 'Smoke' in latest_data and latest_data['Smoke'] > threshold:
        message = f"🚨 CẢNH BÁO: Nồng độ khói vượt ngưỡng! Giá trị hiện tại: {latest_data['Smoke']} ppm \n🔥CÓ THỂ CHÁY!"
        response = send_telegram_alert(message)