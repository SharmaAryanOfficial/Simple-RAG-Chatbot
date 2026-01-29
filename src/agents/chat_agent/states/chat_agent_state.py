from typing import TypedDict, Annotated
from langchain.messages import AnyMessage
import operator

class ChatAgentState(TypedDict):
    """
    This is a class
    """
    messages  : Annotated[list[AnyMessage], operator.add]