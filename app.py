import streamlit as st
import base64

# ---------------- 上傳照片 ----------------
uploaded_files = st.file_uploader("📸 上傳相片（最多 5 張）", type=["jpg","jpeg","png"], accept_multiple_files=True)

if uploaded_files:
    # 把圖片轉成 base64，前端 JS 輪播用
    img_list = []
    for file in uploaded_files[:5]:
        b64 = base64.b64encode(file.read()).decode()
        img_list.append(f"data:image/png;base64,{b64}")

    # JS 輪播
    st.markdown(f"""
    <div style="text-align:center;">
      <img id="slideshow" src="{img_list[0]}" width="500">
    </div>
    <script>
    var images = {img_list};
    var index = 0;
    setInterval(function(){{
        index = (index + 1) % images.length;
        document.getElementById("slideshow").src = images[index];
    }}, 5000); // 每 5 秒切換
    </script>
    """, unsafe_allow_html=True)

else:
    st.info("請上傳相片（最多五張）")

# ---------------- 收音機區 ----------------
stations = [
    {"name": "ICRT", "url": "https://n13.rcs.revma.com/nkdfurztxp3vv?rj-ttl=5&rj-tok=AAABmsT4bvUAqjd6WCHuBZRFQw"},
    {"name": "台北電台", "url": "https://streamak0130.akamaized.net/live0130lh-olzd/_definst_/fm/chunklist.m3u8"},
    {"name": "中廣流行網", "url": "https://stream.rcs.revma.com/aw9uqyxy2tzuv"},
]

if "current_station" not in st.session_state:
    st.session_state.current_station = 0

station = stations[st.session_state.current_station]

st.markdown(f"""
<div style="text-align:center; margin-top:10px;">
  <span style="background:rgba(0,0,0,0.5); color:white; padding:6px 12px; border-radius:6px; font-size:16px; font-weight:bold;">
    🎶 {station['name']}
  </span>
</div>
<div style="text-align:center; margin-top:10px;">
<audio controls autoplay>
  <source src="{station['url']}" type="audio/mpeg">
</audio>
</div>
""", unsafe_allow_html=True)

# ---------------- 控制列 ----------------
col1, col2 = st.columns(2)

with col1:
    if st.button("📻 頻道切換"):
        st.session_state.current_station = (st.session_state.current_station + 1) % len(stations)
    st.caption(f"目前頻道：{stations[st.session_state.current_station]['name']}")

with col2:
    if st.button("🖼️ 照片輪播"):
        st.info("照片輪播已啟動（前端 JS 控制，不會斷音）")
