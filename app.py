import streamlit as st
import base64

# ---------------- 初始化狀態 ----------------
if "current_station" not in st.session_state:
    st.session_state.current_station = 0
if "frame_ratio" not in st.session_state:
    st.session_state.frame_ratio = "16/9"

# ---------------- 上傳照片 ----------------
uploaded_files = st.file_uploader("📸 上傳相片（最多 5 張）", type=["jpg","jpeg","png"], accept_multiple_files=True)

if uploaded_files:
    img_list = []
    for file in uploaded_files[:5]:
        b64 = base64.b64encode(file.read()).decode()
        img_list.append(f"data:image/png;base64,{b64}")

    # 相框比例選項
    ratio_option = st.selectbox("選擇相框比例", ["16/9", "4/3", "1/1"], index=["16/9","4/3","1/1"].index(st.session_state.frame_ratio))
    st.session_state.frame_ratio = ratio_option

    # JS 輪播 + 固定相框
    st.markdown(f"""
    <style>
    .frame {{
        width: 100%;
        max-width: 600px;
        aspect-ratio: {st.session_state.frame_ratio};
        background: #000;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
        margin: auto;
    }}
    .frame img {{
        width: 100%;
        height: 100%;
        object-fit: contain;
    }}
    </style>

    <div class="frame">
      <img id="slideshow" src="{img_list[0]}">
    </div>

    <script>
    var images = {img_list};
    var index = 0;
    setInterval(function(){{
        index = (index + 1) % images.length;
        document.getElementById("slideshow").src = images[index];
    }}, 5000);
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

station = stations[st.session_state.current_station]

# 頻道名稱
st.markdown(f"""
<div style="text-align:center; margin-top:10px;">
  <span style="background:rgba(0,0,0,0.5); color:white; padding:6px 12px; border-radius:6px; font-size:16px; font-weight:bold;">
    🎶 {station['name']}
  </span>
</div>
""", unsafe_allow_html=True)

# 播放器（動態 id，確保切換時重建）
st.markdown(f"""
<div style="text-align:center; margin-top:10px;">
<audio id="player_{st.session_state.current_station}" controls autoplay>
  <source src="{station['url']}" type="audio/mpeg">
</audio>
</div>
""", unsafe_allow_html=True)

# ---------------- 控制列 ----------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <style>
    div[data-testid="channel_switch"] button {
        background-color: #1E90FF;
        color: white;
        font-weight: bold;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    if st.button("📻 頻道切換", key="channel_switch"):
        st.session_state.current_station = (st.session_state.current_station + 1) % len(stations)
    st.caption(f"目前頻道：{stations[st.session_state.current_station]['name']}")

with col2:
    st.markdown("""
    <style>
    div[data-testid="photo_toggle"] button {
        background-color: #32CD32;
        color: white;
        font-weight: bold;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    st.button("🖼️ 照片輪播", key="photo_toggle")
    st.caption("狀態：輪播中（JS 控制，不會斷音）")
