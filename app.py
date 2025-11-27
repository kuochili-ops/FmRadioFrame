import streamlit as st

stations = [
    {"name": "ICRT", "url": "https://n13.rcs.revma.com/nkdfurztxp3vv?rj-ttl=5&rj-tok=AAABmsT4bvUAqjd6WCHuBZRFQw"},
    {"name": "台北電台", "url": "https://streamak0130.akamaized.net/live0130lh-olzd/_definst_/fm/chunklist.m3u8"},
    {"name": "中廣流行網", "url": "https://stream.rcs.revma.com/aw9uqyxy2tzuv"},
    {"name": "好事989", "url": "https://n13.rcs.revma.com/fkdywbc59duvv?rj-ttl=5&rj-tok=AAABmsUmzjEAUA_XnW2QqGYA1w"},
    {"name": "港都983", "url": "https://n12.rcs.revma.com/q2m07dc59duvv?rj-ttl=5&rj-tok=AAABmsVEH6gAzFkrUTImPEJ_7w"},
    {"name": "中廣音樂網", "url": "http://n12.rcs.revma.com/ndk05tyy2tzuv?rj-ttl=5&rj-tok=AAABmsT4lG0A7BfBML2R8HqECw"}
]

if "current" not in st.session_state:
    st.session_state.current = 0

st.title("📻 台灣電台播放器")

station = stations[st.session_state.current]
st.markdown(f"### 正在播放：{station['name']}")

# 用 key 保證每次切換都刷新
st.markdown(f"""
<audio controls autoplay key="{station['url']}">
  <source src="{station['url']}" type="audio/mpeg">
</audio>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
if col1.button("⬅️ 上一台"):
    st.session_state.current = (st.session_state.current - 1) % len(stations)
if col2.button("➡️ 下一台"):
    st.session_state.current = (st.session_state.current + 1) % len(stations)
