import streamlit as st
from rag import answer

st.title("📚 AI Study Assistant")

question = st.text_input("Ask a question about your notes")

if question:
    with st.spinner("Thinking..."):
        reply, sources = answer(question)
    st.markdown(reply)
    with st.expander("Sources"):
        for i, s in enumerate(sources):
            st.markdown(f"**[{i+1}] {s['source']} (p.{s['page']})**")
            st.caption(s["text"][:300] + "...")
