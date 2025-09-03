
# LangChain Starter

A simple LangChain starter with a **FastAPI backend** and **modern chat UI** interface.

## Quickstart

```bash
# 1) Create & activate venv
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Configure OpenAI
cp .env.example .env
# Edit .env and set OPENAI_API_KEY

# 4) Run the backend server
python -m src.backend

# 5) Open your browser
# Visit http://localhost:8000 to use the chat interface
```

## Project Structure

```
langchain-starter/
├── src/
│   ├── __init__.py
│   ├── agent.py          # LangChain agent
│   └── backend.py        # FastAPI server with chat endpoints
├── frontend/
│   ├── index.html        # Chat interface
│   ├── styles.css        # Modern UI styling
│   └── script.js         # Frontend chat logic

├── requirements.txt     # Python dependencies
└── README.md
```

## API Endpoints

- `GET /` - Serves the chat interface
- `POST /api/chat` - Chat with the LangChain agent
- `GET /api/health` - Health check endpoint

### Chat API Usage

```bash
# Send a message to the agent
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Who are you?"}'
```

## What's inside?

### Backend (`src/`)
- **`agent.py`** — LangChain agent
- **`backend.py`** — FastAPI server with:
  - Chat endpoint for processing messages
  - CORS middleware for frontend communication
  - Static file serving for the chat interface

### Frontend (`frontend/`)
- **Modern chat interface** with:
  - Real-time message exchange
  - Typing indicators
  - Responsive design
  - Keyboard shortcuts

## Extending the Agent

To add new tools to your agent, edit `src/agent.py`:

```python
from langchain.tools import tool

@tool
def your_custom_tool(input: str) -> str:
    """Description of what your tool does."""
    # Your tool logic here
    return "Tool result"

# Add your tool to the agent in build_agent()
agent = initialize_agent(
    tools=[your_custom_tool],  # Add here
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
```

## Development

### Running in Development Mode
```bash
# Backend with auto-reload
python -m src.backend

# Or using uvicorn directly
uvicorn src.backend:app --reload --host 0.0.0.0 --port 8000
```

## Learn More

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction) - Learn about LangChain
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Learn about FastAPI  
- [OpenAI API Documentation](https://platform.openai.com/docs) - Learn about OpenAI's API
- [BuildKit Documentation](https://buildkit.picaos.com/integrations) - Learn about BuildKit

## Notes
- Uses `langchain-openai` provider package (recommended modern setup)
- FastAPI provides automatic API documentation at `/docs`
- Frontend uses vanilla JavaScript (no framework dependencies)
- CORS enabled for development (configure for production)
