import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import time
import psycopg2
from psycopg2 import pool
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import requests
from backend import get_latest_sensor_data, display_data_table, check_smoke_alert


st.set_page_config(page_title="Smart Dashboard", layout="wide") 
st_autorefresh(interval=8500, limit=None, key="auto_refresh") 
if not firebase_admin._apps:
    cred = credentials.Certificate("########################################")  
    firebase_admin.initialize_app(cred, {
        'databaseURL': '################################################'  
    })
conn_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        dsn="################################################"
    )
conn = conn_pool.getconn()    
cur = conn.cursor()

# Ngưỡng cảnh báo cháy
smoke_threshold = 45  
latest_data = get_latest_sensor_data()
check_smoke_alert(latest_data, smoke_threshold)


#========== FRONTEND - XỬ LÝ UI ==========
st.title("ỨNG DỤNG QUẢN LÝ NÔNG NGHIỆP THÔNG MINH")
df = display_data_table(cur)
if latest_data:
    st.subheader("🔄 Dữ liệu cảm biến thời gian thực")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💡 Light", f"{latest_data['Light']} lx")
        st.metric("🫁 CO2", f"{latest_data['CO2']} ppm")
    with col2:
        st.metric("🌡️ Temperature", f"{latest_data['Temperature']} °C")
        st.metric("🌱 Soil Humidity", f"{latest_data['Soil_humidity']} %")    
    with col3:
        st.metric("💧 Air Humidity", f"{latest_data['Air_Humidity']} %")
    with col4:   
        st.metric("⚖️ Smoke", f"{latest_data['Smoke']} ppm", delta="⚠️ Vượt ngưỡng!" if latest_data['Smoke'] > smoke_threshold else None) 
else:
    st.warning("Chưa có dữ liệu...")

df['timestamp'] = pd.to_datetime(df['timestamp'])
st.subheader("📈 Biểu đồ dữ liệu cảm biến 5 phút gần nhất")
chart_cols1, chart_cols2, chart_cols3 = st.columns(3)
with chart_cols1:
    st.caption("💡 Light (lux)")
    st.line_chart(df.set_index('timestamp')['light'], use_container_width=True)
    
    st.caption("🌡️ Temperature (°C)")
    st.line_chart(df.set_index('timestamp')['temperature'], use_container_width=True)
with chart_cols2:
    st.caption("💧 Air Humidity (%)")
    st.line_chart(df.set_index('timestamp')['air_humidity'], use_container_width=True)
    
    st.caption("🫁 CO2 (ppm)")
    st.line_chart(df.set_index('timestamp')['co2'], use_container_width=True)
with chart_cols3:
    st.caption("⚖️ Smoke (ppm)")
    st.line_chart(df.set_index('timestamp')['smoke'], use_container_width=True)
    
    st.caption("🌱 Soil Humidity (%)")
    st.line_chart(df.set_index('timestamp')['soil_humidity'], use_container_width=True)
    
st.subheader("📊 Thống kê dữ liệu cảm biến 5 phút gần nhất")
st.dataframe(display_data_table(cur))