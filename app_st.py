from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import streamlit as st
import os

os.environ["OPENAI_API_KEY"] = st.secrets.openai_api_key

if "qa" not in st.session_state:
    st.session_state["qa"] = []
    
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text=initial_text
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text+=token 
        self.container.info(self.text) 

# ユーザーインターフェイスの構築
st.sidebar.title("補助金さん")
st.sidebar.write("補助金・助成金についてお任せあれ")
user_input = st.sidebar.text_input("ご質問をどうぞ。", key="user_input", on_change=communicate)
st.session_state["qa"].append(user_input)
# here is the key, setup a empty container first
chat_box=st.empty() 
stream_handler = StreamHandler(chat_box)
chat = ChatOpenAI(streaming=True, callbacks=[stream_handler])
    
if st.session_state["qa"]:
    messages = st.session_state["qa"]
    for idx, message in enumetate(messages):  # 直近のメッセージを上に
        if idx % 2:
            st.success(message)
        else:
            st.info(message)

if user_input: 
    response = chat([HumanMessage(content=user_input)])
