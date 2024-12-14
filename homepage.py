import streamlit as st
import time

st.set_page_config(
    page_title="Project 1",
    page_icon=":notebook_with_decorative_cover:",
)

st.page_link("Homepage.py",label="Home",icon="💻")
press_app = st.page_link("pages/Handpainter.py",label="App",icon="📽️")
if press_app:
    with st.spinner(':blue[Deploying app] wait for it... :hourglass:'):
        time.sleep(5)

st.header("XIN CHÀO :wave:",divider="blue")
st.write("Dưới đây là bài làm :red[Project-1] của 1 sinh viên Bách Khoa Hà Nội")
st.subheader("Chủ đề :art:")
st.write("Sử dụng solution :blue[mediapipe] của google và ứng dụng vẽ bằng :blue[Hands Gestures]")
st.subheader("Hướng dẫn sử dụng")
st.sidebar.success("Select the app")