
import streamlit as st
# from agno.playground import Playground, serve_playground_app
from agno.agent import Agent
from agno.models.google import Gemini
from google.genai import types
from agno.memory.v2.memory import Memory
from post_gen_agent import PostGenWorkflow



# Safety settings 
safety_settings = [
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=types.HarmBlockThreshold.BLOCK_NONE),
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=types.HarmBlockThreshold.BLOCK_NONE),
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY, threshold=types.HarmBlockThreshold.BLOCK_NONE),
]



# Streamlit App
st.set_page_config(page_title="Post Generation Agent", page_icon="🧠")
st.title("💬Meet Linkedin Post Gen Agentic Workflow(Narrative AI)")
st.caption("🚀 Powered by Gemini, Agno, Crawl4AI, Pydantic, etc")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi there! What post ideas do you have today?"}]

# Render chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
if prompt := st.chat_input("Wanna create a Post? Go ahead!"):
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Narrative AI is thinking..."):
        reply = PostGenWorkflow.run(prompt).content

    st.chat_message("assistant").write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
