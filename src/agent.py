from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from .tools import get_default_tools
import uuid

load_dotenv()

_llm = ChatOpenAI(
    model="gpt-4.1",
    temperature=0.7
)

# Get the default tools (including echo)
_tools = get_default_tools()

# Create the prompt template for the agent
_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant with access to tools. Use the echo tool to confirm understanding or repeat back important information when helpful."),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# Create the agent with tools
_agent = create_tool_calling_agent(_llm, _tools, _prompt)
_agent_executor = AgentExecutor(agent=_agent, tools=_tools, verbose=True)

# In-memory store for conversation histories
_conversation_store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Get or create chat message history for a session."""
    if session_id not in _conversation_store:
        _conversation_store[session_id] = ChatMessageHistory()
    return _conversation_store[session_id]

# Wrap agent executor with message history
_agent_with_history = RunnableWithMessageHistory(
    _agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

def run_agent_query(query: str, conversation_id: str = None) -> tuple[str, str]:
    """Run a query through the agent and return the response and conversation_id."""
    try:
        # Generate a new conversation ID if none provided
        if conversation_id is None:
            conversation_id = str(uuid.uuid4())
        
        response = _agent_with_history.invoke(
            {"input": query},
            config={"configurable": {"session_id": conversation_id}}
        )
        return str(response.get("output", "No response")), conversation_id
    except Exception as e:
        return f"Error processing query: {str(e)}", conversation_id or str(uuid.uuid4())
