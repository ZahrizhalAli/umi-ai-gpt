from openai import OpenAI
import streamlit as st
from langchain_experimental.agents import create_csv_agent
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import AgentExecutor

st.set_page_config(layout="wide", page_icon="💬", page_title="UMI | AI Report",initial_sidebar_state="collapsed" )
st.markdown(
            """
        <style>
            [data-testid="collapsedControl"] {
                display: none
            }
        </style>
        """,
            unsafe_allow_html=True,
        )
openai_api_key = st.secrets['OPENAI_API_KEY']

st.title("💬 UMI-GPT AI Report | Universitas Muslim Indonesia")
st.caption("🚀 UMI GPT Powered by Open AI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello saya UMI-AI Assistant! Silahkan masukkan pertanyaan kamu."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    agent = create_csv_agent(
        ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
        ["../vwDosen.csv", "../vwKaryawan.csv"],
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )
    # client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = agent.run(prompt)

    # agent_executor = AgentExecutor(
    #     agent=agent, tools=[], verbose=True, handle_parsing_errors=True
    # )
    # print(agent_executor.invoke(
    #     {"input": prompt}
    # ))

    # response = client.chat.completions.create(model="gpt-4-1106-preview", messages=st.session_state.messages)
    # msg = response.choices[0].message.content
    msg = response
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
