# Author: ludanchufang
# CreatTime: 2024/6/7
import streamlit as st
from langchain.memory import ConversationSummaryBufferMemory
from utils import qa_agent
from langchain_openai import ChatOpenAI
st.title('✌ Ye')

with st.sidebar:
    openai_api_key = st.text_input("暗号：",type='password')
model = ChatOpenAI(model="gpt-4o",openai_api_key=openai_api_key)
if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationSummaryBufferMemory(
        llm=model,
        return_messages=True,
        memory_key="chat_history",
        output_key="answer"
    )
upload_file = st.file_uploader("来个PDF：", type="pdf")
question = st.text_input("来个问题：",disabled=not upload_file)

if upload_file and question and not openai_api_key:
    st.info("hey boy,暗号")
if upload_file and question and openai_api_key:
    with st.spinner("别催ok？"):
        response = qa_agent(openai_api_key,st.session_state["memory"],
                            upload_file,question)
        st.write("### 答案")
        st.write(response["answer"])
        st.session_state["chat_history"]=response["chat_history"]
if "chat_history" in st.session_state:
    with st.expander("黑历史"):
        for i in range(0,len(st.session_state["chat_history"]),2):
            human_message = st.session_state["chat_history"][i]
            ai_message = st.session_state["chat_history"][i+1]
            st.write(human_message.content)
            st.write(ai_message.content)
            if i< len(st.session_state["chat_history"])-2:
                st.divider