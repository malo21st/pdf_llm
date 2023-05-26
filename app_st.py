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

def store_del_msg():
    st.session_state["qa"].append(st.session_state["user_input"])
    st.session_state["user_input"] = ""  # 入力欄を消去

# ユーザーインターフェイスの構築
st.sidebar.title("補助金さん")
st.sidebar.write("補助金・助成金についてお任せあれ")

if st.session_state["qa"]:
    messages = st.session_state["qa"]
    for idx, message in enumerate(messages):  # 直近のメッセージを上に
        if idx % 2:
            st.success(message)
        else:
            st.info(message)

user_input = st.sidebar.text_input("ご質問をどうぞ。", key="user_input", on_change=store_del_msg)
# here is the key, setup a empty container first
chat_box=st.empty() 
stream_handler = StreamHandler(chat_box)
chat = ChatOpenAI(streaming=True, callbacks=[stream_handler])
if st.session_state["qa"]: 
    query = st.session_state["qa"][-1]
    response = chat([HumanMessage(content=query)])
    st.session_state["qa"].append(response.content)
