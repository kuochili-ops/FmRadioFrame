import streamlit as st
import requests
import datetime

API_KEY = "dacfd5f7b7e6c05162ac1340b88b6cc0"  # 你的 API Key

# 顯示時間日期
now = datetime.datetime.now()
st.markdown(f"🕒 {now.strftime('%H:%M:%S')}  📅 {now.strftime('%Y-%m-%d')}")

# 城市輸入
city = st.text_input("🌍 輸入城市 (例如 Taipei,TW)", "Taipei,TW")

if city:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=zh_tw"
    res = requests.get(url).json()

    if res.get("cod") == 200:  # 成功
        temp = res["main"]["temp"]
        desc = res["weather"][0]["description"]
        st.markdown(f"🌤️ {city}：{temp}°C，{desc}")
    else:
        st.markdown(f"⚠️ API 錯誤：{res.get('message')}")
