import streamlit as st

st.set_page_config(
    page_title="Project 1",
    page_icon=":notebook_with_decorative_cover:",
)

st.header("XIN CHÀO :wave:",divider="blue")
#st.write("Dưới đây là bài làm Project-1 của 1 sinh viên Bách Khoa")
st.markdown("""
<style>
.big-font {
    font-size:300px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">Hello World !!</p>', unsafe_allow_html=True)
st.sidebar.success("Select the app")