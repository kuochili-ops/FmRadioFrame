
import streamlit as st

st.title("📻 台灣 FM 廣播代理播放")
proxy_url = "http://localhost:5000/proxy"  # Flask 代理 URL
st.audio(proxy_url, format="audio/mp3")
