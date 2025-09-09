"""
Tools module for LangChain with Pydantic v2 compatibility.

This module demonstrates proper Pydantic v2 field annotation patterns
to avoid the "Field defined on a base class was overridden by a non-annotated attribute" error.
"""

from typing import Optional, Type, Any
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool


class EchoToolSchema(BaseModel):
    """Schema for the Echo tool input."""
    message: str = Field(..., description="The message to echo back")


class EchoTool(BaseTool):
    """A simple tool that echoes back the input message."""
    
    name: str = "echo"
    description: str = "Echo back the provided message. Useful for testing or confirming inputs."
    # CRITICAL: Properly type annotate the args_schema field for Pydantic v2 compatibility
    args_schema: Type[BaseModel] = EchoToolSchema
    
    def _run(
        self, 
        message: str,
        run_manager: Optional[Any] = None
    ) -> str:
        """Execute the echo tool."""
        return f"Echo: {message}"
    
    async def _arun(
        self, 
        message: str,
        run_manager: Optional[Any] = None
    ) -> str:
        """Execute the echo tool asynchronously."""
        return self._run(message, run_manager)


def get_default_tools() -> list[BaseTool]:
    """Return the list of default tools available to the agent."""
    return [EchoTool()]
