from src.agents.chat_agent.states.chat_agent_state import ChatAgentState
from src.agents.chat_agent.tools.date_time import get_current_date_and_time
from src.agents.chat_agent.tools.web_search import search_the_web
from langchain.messages import ToolMessage

tools = [
    get_current_date_and_time,
    search_the_web
]

tools_by_name  = {tool.name : tool for tool in tools}

def tool_extractor(state : ChatAgentState) -> ChatAgentState:
    """
    Docstring for tool_extractor
    
    :param state: Description
    :type state: ChatAgentState
    :return: Description
    :rtype: ChatAgentState
    """

    result = []

    for tool_call in state['messages'][-1].tool_calls:
        tool = tools_by_name[tool_call['name']]
        observation = tool.invoke(tool_call['args'])

        result.append(
            ToolMessage(
                content=observation,
                tool_call_id = tool_call['id']
            )
        )

    return {'messages':result}