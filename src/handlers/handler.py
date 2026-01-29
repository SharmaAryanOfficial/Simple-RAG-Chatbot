from src.agents.chat_agent.graph import create_chat_agent_graph
from langchain.messages import HumanMessage
from src.agents.chat_agent.states.chat_agent_state import ChatAgentState
from typing import Iterator



def chat_agent_handler(thread_id: str, message : str) -> ChatAgentState:
    """
    """
    graph = create_chat_agent_graph()

    return graph.invoke(
        input = {
            'messages': [HumanMessage(content = message)]
        },
        config={
            'configurable':{
                'thread_id': thread_id
                }
        }
    ) #{'messages': answer from AI}

def chat_streaming_handler(thread_id : str, message : str) -> Iterator[str]:
    """
    Docstring for chat_streaming_handler
    
    :param thread_id: Description
    :type thread_id: str
    :param message: Description
    :type message: str
    :return: Description
    :rtype: Any
    """
    graph = create_chat_agent_graph()


    for chunk, metadata in graph.stream(
        input={
            'messages': [HumanMessage(content=message)]
        },
        config={
            'configurable':{
                'thread_id':thread_id
            }
        },
        stream_mode='messages'
    ):
        yield chunk.content



def get_all_threads_handler() ->list[str | None]:
    """
    Docstring for get_all_threads_handler

    """
    graph = create_chat_agent_graph()

    all_checkpoints =  graph.checkpointer.list(config={})

    threads = set()

    for checkpoint in all_checkpoints:
        threads.add(checkpoint.config['configurable']['thread_id'])

    return list (threads)

def chat_history_handler(thread_id: str) -> ChatAgentState | dict[None, None]:
    """
    Docstring for chat_history_handler
    """

    graph = create_chat_agent_graph()

    return graph.get_state(config={
        'configurable': {
            'thread_id': thread_id
        }
    })[0]