import streamlit as st
from agent.core import run_agent

st.set_page_config(page_title="Smart Research Assistant", page_icon="🔍", layout="wide")

st.title("🔍 Smart Research Assistant")
st.markdown("An AI agent that researches any topic using web search, Wikipedia, and summarization.")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Enter a research topic:", placeholder="e.g., Compare solar and wind energy")

if st.button("Research", type="primary"):
    if query.strip():
        with st.spinner("Agent is researching... This may take a minute."):
            result = run_agent(query)
            st.session_state.history.append({"query": query, "result": result})
    else:
        st.warning("Please enter a research topic.")

for i, item in enumerate(reversed(st.session_state.history)):
    with st.expander(f"Research: {item['query']}", expanded=(i == 0)):
        st.markdown(item["result"])

if st.session_state.history:
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()