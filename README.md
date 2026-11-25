# Implementing a ChatGPT App with LangChain from Scratch

A hands-on Python project that demonstrates how to build a command-line chatbot using **LangChain** and **OpenAI chat models**. The notebook starts with a basic prompt-response application, then adds conversation memory and persistent chat-history storage.

## Project Overview

This project contains three implementations:

1. **Basic Chatbot** – Sends user prompts to an OpenAI chat model through a LangChain prompt/model/output-parser pipeline. The system prompt instructs the model to respond only in German.
2. **Chatbot with Conversation Memory** – Maintains conversation context during a session using `RunnableWithMessageHistory` and `InMemoryChatMessageHistory`.
3. **Chatbot with Saved Chat Sessions** – Persists messages between runs using `FileChatMessageHistory`, storing each session in a JSON file.

The examples use LangChain's modern Runnable / LCEL approach (`prompt | llm | parser`) rather than the older `LLMChain` pattern.

## Technologies Used

- Python
- LangChain
- `langchain-openai`
- `langchain-core`
- `langchain-community`
- OpenAI API
- `python-dotenv`
- Jupyter Notebook

## Project Structure

```text
.
├── project_custom_chatgpt_with_langchain_from_scratch.ipynb
├── .env
└── README.md
```

The notebook contains the code for all three chatbot implementations. Run the relevant notebook cells in order.

## Requirements

- Python 3.9 or later (a recent Python version is recommended).
- An OpenAI API key.
- Jupyter Notebook or JupyterLab.

## Installation

1. Clone or download this repository.

2. (Recommended) Create and activate a virtual environment:

   **Windows**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the packages used by the notebook:

   ```bash
   pip install langchain langchain-core langchain-openai langchain-community python-dotenv jupyter
   ```

4. Create a `.env` file in the project directory and add your OpenAI API key:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   Replace the placeholder with your own API key. Do not commit your `.env` file or share your API key.

## Run the Project

Start Jupyter Notebook:

```bash
jupyter notebook
```

Open:

```text
project_custom_chatgpt_with_langchain_from_scratch.ipynb
```

Run the notebook cells in order. The chatbot implementations use an interactive terminal input loop, so enter prompts in the environment running the notebook kernel.

To end a chatbot session, enter one of the exit commands supported by that implementation:

- Basic chatbot: `quit`, `q`, `exit`, or `bye`
- Memory and saved-session chatbots: `quit`, `exit`, or `bye`

## Implementation Details

### 1. Basic Chatbot

The first implementation uses:

- `ChatOpenAI` to connect to an OpenAI chat model.
- `ChatPromptTemplate` to define the prompt structure.
- `SystemMessage` to set the chatbot's behavior.
- `HumanMessagePromptTemplate` to insert the user's prompt.
- `StrOutputParser` to return the model response as text.

The chain is composed using LangChain Expression Language (LCEL):

```python
chain = prompt | llm | StrOutputParser()
```

The model is configured as `gpt-3.5-turbo` with a temperature of `1`. The system message instructs it to respond only in German.

### 2. Chatbot with Conversation Memory

The second implementation adds conversation history so the chatbot can use earlier messages in the current session.

It uses:

- `InMemoryChatMessageHistory` to store messages in memory.
- `RunnableWithMessageHistory` to connect the history to the runnable chain.
- `MessagesPlaceholder` to insert previous messages into the prompt.
- A session ID to identify the conversation.

The session history is managed through a Python dictionary:

```python
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]
```

The chain is invoked with a session ID:

```python
response = chain.invoke(
    {"content": content},
    config={"configurable": {"session_id": "default"}}
)
```

This implementation keeps history in memory. The history is not automatically preserved after the Python process ends.

### 3. Saving Chat Sessions

The third implementation stores conversation history in a JSON file using `FileChatMessageHistory`.

The history provider is defined as:

```python
def get_session_history(session_id: str):
    return FileChatMessageHistory(f"{session_id}.json")
```

The chain uses the same `RunnableWithMessageHistory` pattern, but messages are saved to a file rather than only held in memory.

The notebook uses the session ID `chat_history`, which creates or uses:

```text
chat_history.json
```

The final notebook cell displays the stored messages:

```python
print(get_session_history("chat_history").messages)
```

## Models Used

The notebook configures the following OpenAI model names in its examples:

| Implementation | Model | Temperature |
|---|---|---:|
| Basic chatbot | `gpt-3.5-turbo` | 1 |
| In-memory conversation memory | `gpt-5.2` | 0.5 |
| File-based chat history | `gpt-5-nano` | 0 |

Model availability can depend on your OpenAI account and API access. If a configured model is unavailable, replace its name with a model currently available to your account.

## Important Notes

- The three implementations are separate examples in the notebook; they are not combined into one application.
- The basic chatbot's system prompt specifies German-only responses. The later examples use a general conversational system prompt.
- In-memory history is temporary and is lost when the process ends.
- File-based history is persisted in JSON files named using the session ID.
- Keep API keys private. Add `.env` and generated chat-history files to `.gitignore` if they should not be committed.

## Learning Outcomes

After completing this project, you should understand how to:

- Connect an OpenAI chat model to a Python application using LangChain.
- Build prompt templates for chatbot interactions.
- Compose LangChain components using LCEL.
- Maintain conversation context with message history.
- Separate conversations using session IDs.
- Persist chat history in JSON files.

## License

Add a license to this project if you intend to distribute or reuse it publicly.
