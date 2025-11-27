# ---------------- 控制列（同一排兩個按鈕，顏色區分） ----------------
col1, col2 = st.columns([1,1])

with col1:
    st.markdown("""
    <style>
    div[data-testid="stButton"] button {
        background-color: #1E90FF;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    if st.button("📻 頻道切換"):
        st.session_state.current_station = (st.session_state.current_station + 1) % len(stations)

with col2:
    st.markdown("""
    <style>
    div[data-testid="stButton"] button {
        background-color: #32CD32;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    if st.button("🖼️ 照片輪播"):
        st.session_state.slideshow = not st.session_state.slideshow
