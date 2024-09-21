# 聚客 Ai 科技
# 讲师：kevin
import os
import streamlit as st
from openai import OpenAI

# 配置 openai 的连接属性
client = OpenAI(
    # 从系统环境变量来获取
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
    # api_key="hk-mc25aj1000043232f98f7330e625282ddb7dbaa7d7adae8d",
    # base_url="https://api.openai-hk.com/v1"
)

# 大模型给出的答案
def chat_stream():
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=st.session_state.messages_history,
        # 用于控制随机性，值越大随机性越高
        temperature=0.5,
        stream=True
    )
    # 返回响应结果
    return response


def init_chat():
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hi，我是 JPX～ 很高兴遇见你！有问必答，专注于懂你的 AI 👋 "
    }]
    st.session_state.messages_history = [{
        "role": "system",
        "content": st.session_state.system_message
    }]


st.markdown("""
<style>.st-emotion-cache-1c7y2kd {flex-direction: row-reverse; text-align:right }</style>
""", unsafe_allow_html=True)

# 构建左侧
with st.sidebar:
    st.markdown(f"""
    <center>
    <img src='https://vip.helloimg.com/i/2024/07/02/66841f6f4a3a5.png' width='100'/>
    <h1> JPX <sup>💬</sup><h1/>
    </center>
    """, unsafe_allow_html=True)

    # 角色定义输入框 System Message
    system_message = st.text_area("角色定义", "你是一个能帮助用户的 AI 助手。", on_change=init_chat,
                                  key='system_message')


    # 创造力调节 Temperature
    temperature = st.slider("创造力调节", min_value=0.0, max_value=2.0, value=1.0, step=0.1, help='值越大约具有创造力',
                            format="%.1f")

    if st.button("🧹 清除聊天记录"):
        init_chat()

# 构建右侧
st.title("JPX AI 聊天机器人")

if "messages_history" not in st.session_state:
    st.session_state.messages_history = [
        {"role": "system", "content": system_message}
    ]

# 初始化界面的聊天列表
if "messages" not in st.session_state:
    # 初始化消息
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi，我是 JPX～ 很高兴遇见你！有问必答，专注于懂你的 AI 👋 "
        }
    ]

# 显示对话的历史列表
for message in st.session_state.messages:
    # 聊天窗口
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
user_query = st.chat_input("说点什么...")
if user_query:
    # 显示用户输入的内容到聊天窗口
    with st.chat_message("user"):
        st.write(user_query)
    # 在聊天窗口输出用户输入的问题
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query
        }
    )
    st.session_state.messages_history.append({
        "role": "user",
        "content": user_query
    })

    with st.chat_message("assistant"):
        # 转圈等待（提高用户体验）
        with st.spinner(""):
            # AI 的回复
            response = chat_stream()
            # 创建显示消息的容器
            message_placeholder = st.empty()
            # AI 的答案
            ai_response = ""
            for chunk in response:
                # 从流响应中获得AI的答案
                if chunk.choices and chunk.choices[0].delta.content:
                    ai_response += chunk.choices[0].delta.content
                    # 显示AI的答案
                    message_placeholder.markdown(ai_response + "▌")

            # 在聊天窗口输出完整的 AI 答案
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": ai_response
                }
            )
            st.session_state.messages_history.append({
                "role": "assistant",
                "content": ai_response
            })
