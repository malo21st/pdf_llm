from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain import PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
import streamlit as st
import os
from PIL import Image

os.environ["OPENAI_API_KEY"] = st.secrets.openai_api_key

image = Image.open('tenjikai.png')

# プロンプトの定義
template = """
あなたは親切なアシスタントです。下記の質問に日本語で回答してください。
質問：{question}
回答：
"""

prompt = PromptTemplate(
    input_variables=["question"],
    template=template,
)

@st.cache_data
def load_vector_db():
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory="VECTOR_DB", embedding_function = embeddings)
    return vectordb

vectordb = load_vector_db()

if "qa" not in st.session_state:
    st.session_state["qa"] = []
    
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text=initial_text
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text+=token 
        self.container.success(self.text) 

def store_del_msg():
    st.session_state["qa"].append({"role": "Q", "msg": st.session_state["user_input"]})
    st.session_state["user_input"] = ""  # 入力欄を消去

# ユーザーインターフェイス
st.sidebar.title("補助金さん")
st.sidebar.write("補助金・助成金についてお任せあれ")

if st.session_state["qa"]:
    messages = st.session_state["qa"]
    for message in messages:
        if message["role"] == "Q":
            st.info(message["msg"])
        elif message["role"] == "A":
            st.success(message["msg"])
        elif message["role"] == "E":
            st.error(message["msg"])

user_input = st.sidebar.text_input("ご質問をどうぞ", key="user_input", on_change=store_del_msg)
st.sidebar.markdown("---")
st.sidebar.image(image, caption='展示会出展助成事業（令和５年度　東京都）', use_column_width="auto")
# here is the key, setup a empty container first
chat_box=st.empty() 
stream_handler = StreamHandler(chat_box)
qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(model_name="gpt-3.5-turbo", streaming=True, callbacks=[stream_handler]), 
                                 chain_type="stuff", retriever=vectordb.as_retriever())

if st.session_state["qa"]: 
    query = st.session_state["qa"][-1]["msg"]
    try:
        response = qa.run(query)
        st.session_state["qa"].append({"role": "A", "msg": response})
    except Exception:
        response = "エラーが発生しました！　もう一度、質問して下さい。"
        st.session_state["qa"].append({"role": "E", "msg": response})
