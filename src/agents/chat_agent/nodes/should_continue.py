from typing import Literal
from langgraph.graph import END
from src.agents.chat_agent.states.chat_agent_state import ChatAgentState
from langchain.messages import AIMessage


def should_continue(state: ChatAgentState) -> Literal['tool_executer_node', END]:
    """
    Docstring for should_continue

    Decide if we should continue the loop or stop based upon whether the LLM made a tool call
    
    :param state: Description
    :type state: ChatAgentState
    :return: Description
    :rtype: Any | Literal['tool_executer_node']
    """
    last_message = state["messages"][-1]

    # Only AI messages can have tool_calls
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tool_executer_node"

    return END