import streamlit as st
from agent import run_agent

st.set_page_config(page_title="LangGraph Agent", page_icon="🧠")

st.title("🧠 LangGraph Research Agent (Groq-Powered)")
st.markdown("Ask any question and get an answer from a planning agent using DuckDuckGo and LLaMA 3 (via Groq).")

question = st.text_input("Enter your research question:")

if st.button("Ask Agent") and question.strip():
    with st.spinner("Thinking..."):
        answer = run_agent(question)
    st.subheader("🔍 Agent Answer")
    st.write(answer)
