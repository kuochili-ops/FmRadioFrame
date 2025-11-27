import streamlit as st
import datetime
import requests

# 電台清單
stations = [
    {"name": "ICRT", "url": "https://n13.rcs.revma.com/nkdfurztxp3vv?rj-ttl=5&rj-tok=AAABmsT4bvUAqjd6WCHuBZRFQw"},
    {"name": "台北電台", "url": "https://streamak0130.akamaized.net/live0130lh-olzd/_definst_/fm/chunklist.m3u8"},
    {"name": "中廣流行網", "url": "https://stream.rcs.revma.com/aw9uqyxy2tzuv"},
    {"name": "好事989", "url": "https://n13.rcs.revma.com/fkdywbc59duvv?rj-ttl=5&rj-tok=AAABmsUmzjEAUA_XnW2QqGYA1w"},
    {"name": "港都983", "url": "https://n12.rcs.revma.com/q2m07dc59duvv?rj-ttl=5&rj-tok=AAABmsVEH6gAzFkrUTImPEJ_7w"},
    {"name": "中廣音樂網", "url": "http://n12.rcs.revma.com/ndk05tyy2tzuv?rj-ttl=5&rj-tok=AAABmsT4lG0A7BfBML2R8HqECw"}
]

# 初始化電台狀態
if "current" not in st.session_state:
    st.session_state.current = 0

station = stations[st.session_state.current]

# 主標題
st.markdown("<h1 style='text-align:center;'>🖼️ 相框收音機</h1>", unsafe_allow_html=True)

# 播放器
st.markdown(f"<h3>🎵 正在播放：{station['name']}</h3>", unsafe_allow_html=True)
st.markdown(f"""
<audio controls autoplay key="{station['url']}">
  <source src="{station['url']}" type="audio/mpeg">
</audio>
""", unsafe_allow_html=True)

# 切換按鈕
col1, col2 = st.columns(2)
if col1.button("⬅️ 上一台"):
    st.session_state.current = (st.session_state.current - 1) % len(stations)
if col2.button("➡️ 下一台"):
    st.session_state.current = (st.session_state.current + 1) % len(stations)

# 顯示時間與日期（右上角）
now = datetime.datetime.now()
st.markdown(f"""
<div style='position:fixed; top:10px; right:10px; text-align:right; font-size:16px;'>
🕒 {now.strftime('%H:%M:%S')}<br>📅 {now.strftime('%Y-%m-%d')}
</div>
""", unsafe_allow_html=True)

# 天氣資訊（右下角）
API_KEY = "dcd113bba5675965ccf9e60a7e6d06e5"  # 你的 OpenWeatherMap API Key
city = st.text_input("🌍 輸入城市（例如 Taipei）", "Taipei")

if API_KEY and city:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=zh_tw"
    try:
        res = requests.get(url).json()
        temp = res["main"]["temp"]
        desc = res["weather"][0]["description"]
        st.markdown(f"""
        <div style='position:fixed; bottom:10px; right:10px; text-align:right; font-size:16px;'>
        🌤️ {city}<br>{temp}°C，{desc}
        </div>
        """, unsafe_allow_html=True)
    except:
        st.markdown("⚠️ 無法取得天氣資訊")
