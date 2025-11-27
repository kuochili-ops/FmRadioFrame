
import streamlit as st
import time

# 設定頁面標題
st.set_page_config(page_title="FM Radio + Photo Frame", layout="centered")

st.title("📻 FM 收音機 + 相片輪播")

# --- 圖片輪播 ---
st.subheader("相片輪播")
sample_photos = ["assets/photo1.jpg", "assets/photo2.jpg", "assets/photo3.jpg"]

# 使用 session state 控制圖片索引
if "index" not in st.session_state:
    st.session_state.index = 0

# 顯示圖片
img_placeholder = st.empty()
img_placeholder.image(sample_photos[st.session_state.index], use_column_width=True)

# 自動輪播（每 5 秒換一張）
def auto_slide():
    for _ in range(10):  # 播放 10 次循環
        time.sleep(5)
        st.session_state.index = (st.session_state.index + 1) % len(sample_photos)
        img_placeholder.image(sample_photos[st.session_state.index], use_column_width=True)

# 啟動輪播按鈕
if st.button("開始輪播"):
    auto_slide()

# --- FM 廣播串流 ---
st.subheader("FM 廣播串流")
stream_url = "http://fm983.cityfm.tw:8080/983.mp3"  # 可替換其他串流

st.audio(stream_url, format="audio/mp3")
st.write("🎶 正在播放：FM98.3 城市廣播")
