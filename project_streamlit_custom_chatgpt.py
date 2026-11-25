# install the required libraries
# pip install -q -r ./requirements.txt


'''
# CHANGE: ChatOpenAI moved from `langchain.chat_models` to the
# `langchain-openai` package (langchain>=0.2 split integrations into
# separate packages to keep the core library lightweight).
from langchain_openai import ChatOpenAI

# CHANGE: Message schema classes moved from `langchain.schema` to
# `langchain_core.messages`.  `langchain_core` is the stable, low-level
# foundation that all LangChain packages now build on top of.
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

import streamlit as st

# CHANGE: The third-party `streamlit_chat` package is no longer maintained
# and conflicts with recent Streamlit versions.  Streamlit 1.23+ ships
# st.chat_message() and st.chat_input() as first-class primitives that
# provide the same bubble-style UI natively — no extra dependency needed.
# The `from streamlit_chat import message` line has been removed.

# loading the OpenAI api key from .env (OPENAI_API_KEY="sk-********")
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

st.set_page_config(
    page_title='Your Custom Assistant',
    page_icon='🤖'
)
st.subheader('Your Custom ChatGPT 🤖')

chat = ChatOpenAI(model_name='gpt-5.2', temperature=0.5)

# creating the messages (chat history) in the Streamlit session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# creating the sidebar
with st.sidebar:
    # streamlit text input widget for the system message (role)
    system_message = st.text_input(label='System role')
    # streamlit text input widget for the user message
    user_prompt = st.text_input(label='Send a message')

    if system_message:
        if not any(isinstance(x, SystemMessage) for x in st.session_state.messages):
            st.session_state.messages.append(
                SystemMessage(content=system_message)
            )

    # if the user entered a question
    if user_prompt:
        st.session_state.messages.append(
            HumanMessage(content=user_prompt)
        )

        with st.spinner('Working on your request ...'):
            # CHANGE: Calling a chat model directly as `chat(messages)` is
            # deprecated.  The standard interface is now `.invoke(messages)`,
            # which works consistently across all LangChain runnables.
            response = chat.invoke(st.session_state.messages)

        # adding the response's content to the session state
        st.session_state.messages.append(AIMessage(content=response.content))

# adding a default SystemMessage if the user didn't enter one
if len(st.session_state.messages) >= 1:
    if not isinstance(st.session_state.messages[0], SystemMessage):
        st.session_state.messages.insert(0, SystemMessage(content='You are a helpful assistant.'))

# CHANGE: Replaced streamlit_chat's `message()` helper with Streamlit's
# built-in st.chat_message() context manager.
# - st.chat_message("human") renders a user bubble
# - st.chat_message("ai")    renders an assistant bubble
# The loop still skips index 0 (the SystemMessage) just as before.
for msg in st.session_state.messages[1:]:
    if isinstance(msg, HumanMessage):
        with st.chat_message("human"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("ai"):
            st.write(msg.content)

# run the app: streamlit run ./project_streamlit_custom_chatgpt.py 
  '''



import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

# Load environment variables
load_dotenv()

# Streamlit page configuration
st.set_page_config(
    page_title="Your Custom Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Your Custom ChatGPT")
st.caption("A personalized AI assistant powered by OpenAI and LangChain.")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(
            content="You are a helpful assistant."
        )
    ]

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = (
        "You are a helpful assistant."
    )

# Initialize the ChatOpenAI model
@st.cache_resource
def load_chat_model():
    return ChatOpenAI(
        model="gpt-5.2",
        temperature=0.5
    )

try:
    chat = load_chat_model()
except Exception as e:
    st.error(f"Error initializing OpenAI model: {e}")
    st.stop()

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")

    system_prompt = st.text_area(
        "System Prompt",
        value=st.session_state.system_prompt,
        height=150
    )

    if st.button("Update System Prompt"):
        st.session_state.system_prompt = system_prompt

        # Replace the existing system message
        st.session_state.messages = [
            SystemMessage(content=system_prompt)
        ]

        st.success("System prompt updated!")
        st.rerun()

    if st.button("Clear Chat History"):
        st.session_state.messages = [
            SystemMessage(
                content=st.session_state.system_prompt
            )
        ]
        st.rerun()

    st.divider()

    st.caption("Model: GPT-5.2")
    st.caption("Framework: LangChain + Streamlit")

# Display existing chat history
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)

    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# User chat input
user_prompt = st.chat_input("Ask me anything...")

if user_prompt:

    # Add user message to history
    st.session_state.messages.append(
        HumanMessage(content=user_prompt)
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                response = chat.invoke(
                    st.session_state.messages
                )

                assistant_response = response.content

                # Handle text response
                if isinstance(assistant_response, str):
                    st.markdown(assistant_response)

                else:
                    st.write(assistant_response)

                # Save AI response
                st.session_state.messages.append(
                    AIMessage(content=assistant_response)
                )

            except Exception as e:
                st.error(f"Something went wrong: {e}")
