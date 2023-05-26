from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import streamlit as st
import os

os.environ["OPENAI_API_KEY"] = st.secrets.openai_api_key

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text=initial_text
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text+=token 
        self.container.info(self.text) 

query=st.text_input("input your query")
# ask_button=st.button("ask") 

st.markdown("### streaming box")
# here is the key, setup a empty container first
chat_box=st.empty() 
stream_handler = StreamHandler(chat_box)
chat = ChatOpenAI(streaming=True, callbacks=[stream_handler])

if query: 
    response = chat([HumanMessage(content=query)])
