import streamlit as st
import datetime
import requests
from PIL import Image
import base64
from io import BytesIO
import pytz  # 新增台北時區支持

# 初始化狀態
if "current_station" not in st.session_state:
    st.session_state.current_station = 0

# ---------------- 上半部：相框 ----------------
uploaded_files = st.file_uploader("📸 上傳相片（最多 5 張）", type=["jpg","jpeg","png"], accept_multiple_files=True)

photo_urls = []
if uploaded_files:
    photos = uploaded_files[:5]
    for file in photos:
        img = Image.open(file)
        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        b64 = base64.b64encode(byte_im).decode()
        photo_urls.append(f"data:image/png;base64,{b64}")

    # 輪播選項
    slideshow = st.checkbox("▶️ 啟動輪播")
    speed = st.selectbox("⏱️ 輪播速度", ["5 秒", "10 秒", "30 秒"], index=1)
    interval = {"5 秒":5000, "10 秒":10000, "30 秒":30000}[speed]

    # 顯示第一張照片
    st.image(photos[0], use_column_width=True)

    # JS 輪播
    st.markdown(f"""
    <div style="text-align:center;">
      <img id="slideshow" src="{photo_urls[0]}" width="600">
    </div>
    <script>
    var images = {photo_urls};
    var index = 0;
    var enable = {"true" if slideshow else "false"};
    if(enable){{
        setInterval(function(){{
            index = (index + 1) % images.length;
            document.getElementById("slideshow").src = images[index];
        }}, {interval});
    }}
    </script>
    """, unsafe_allow_html=True)

else:
    st.info("請上傳相片（最多五張）")

# ---------------- 下半部：收音機 ----------------
stations = [
    {"name": "ICRT", "url": "https://n13.rcs.revma.com/nkdfurztxp3vv?rj-ttl=5&rj-tok=AAABmsT4bvUAqjd6WCHuBZRFQw"},
    {"name": "台北電台", "url": "https://streamak0130.akamaized.net/live0130lh-olzd/_definst_/fm/chunklist.m3u8"},
    {"name": "中廣流行網", "url": "https://stream.rcs.revma.com/aw9uqyxy2tzuv"},
    {"name": "好事989", "url": "https://n13.rcs.revma.com/fkdywbc59duvv?rj-ttl=5&rj-tok=AAABmsUmzjEAUA_XnW2QqGYA1w"},
    {"name": "港都983", "url": "https://n12.rcs.revma.com/q2m07dc59duvv?rj-ttl=5&rj-tok=AAABmsVEH6gAzFkrUTImPEJ_7w"},
    {"name": "中廣音樂網", "url": "http://n12.rcs.revma.com/ndk05tyy2tzuv?rj-ttl=5&rj-tok=AAABmsT4lG0A7BfBML2R8HqECw"}
]

station = stations[st.session_state.current_station]
st.markdown(f"### 🎶 正在播放：{station['name']}")
st.markdown(f"""
<audio controls autoplay>
  <source src="{station['url']}" type="audio/mpeg">
</audio>
""", unsafe_allow_html=True)

col3, col4 = st.columns([1,1])
if col3.button("⬅️ 上一台"):
    st.session_state.current_station = (st.session_state.current_station - 1) % len(stations)
if col4.button("➡️ 下一台"):
    st.session_state.current_station = (st.session_state.current_station + 1) % len(stations)

# ---------------- 下半部：時間、日期、天氣 ----------------
tz = pytz.timezone("Asia/Taipei")
now = datetime.datetime.now(tz)
st.markdown(f"🕒 時間：{now.strftime('%H:%M:%S')}")
st.markdown(f"📅 日期：{now.strftime('%Y-%m-%d')}")

API_KEY = "dcd113bba5675965ccf9e60a7e6d06e5"
city = st.text_input("🌍 城市 (例如 Taipei,TW)", "Taipei,TW")

if API_KEY and city:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=zh_tw"
    try:
        res = requests.get(url).json()
        if res.get("cod") == 200:
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"]
            st.markdown(f"🌤️ {city}：{temp}°C，{desc}")
        else:
            st.warning(f"⚠️ API 錯誤：{res.get('message')}")
    except Exception as e:
        st.error(f"⚠️ 無法取得天氣資訊：{e}")
