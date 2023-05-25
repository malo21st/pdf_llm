import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀なアシスタントAIです。"}
        ]
if "qa" not in st.session_state:
    st.session_state["qa"] = []

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)
    
    st.session_state["qa"].append(bot_message)
    st.session_state["qa"].append(user_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.sidebar.title("補助金さん")
st.sidebar.write("補助金・助成金に関してお任せください。")

user_input = st.sidebar.text_input("ご質問を入力してください。", key="user_input", on_change=communicate)

if st.session_state["qa"]:
    messages = st.session_state["qa"]
    for message in reversed(messages):  # 直近のメッセージを上に
        if message["role"]=="assistant":
            st.success(message["content"])
        elif message["role"]=="user":
            st.info(message["content"])
