from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

_agent = ChatOpenAI(
    model="gpt-4.1",
    temperature=0.7
)

def run_agent_query(query: str) -> str:
    """Run a query through the agent and return the response."""
    try:
        from langchain.schema import SystemMessage, HumanMessage
        
        messages = [
            SystemMessage(content="You are a helpful assistant."),
            HumanMessage(content=query)
        ]
        response = _agent.invoke(messages)
        return str(response.content)
    except Exception as e:
        return f"Error processing query: {str(e)}"
