from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from src.handlers.handler import chat_agent_handler, get_all_threads_handler, chat_history_handler
from src.agents.chat_agent.states.chat_agent_state import ChatAgentState
from fastapi.responses import StreamingResponse
from src.handlers.handler import chat_streaming_handler
from src.routes.rag_route import router as rag_router



router = APIRouter()


@router.post("/chat/{thread_id}")
def chat_agent_route(thread_id: str, message: str)-> ChatAgentState:
    """
    """
    return chat_agent_handler(thread_id=thread_id, message=message)

@router.get("/chat/threads")
def get_all_threads() -> list[str | None]:
    """
    Docstring for get_all_threads
    """
    return get_all_threads_handler()

@router.post('/chat/{thread_id}')
def chat_stream_route(thread_id: str, message: str) ->ChatAgentState:
    """
    Docstring for chat_agent_route
    
    :param thread_id: Description
    :type thread_id: str
    :param message: Description
    :type message: str
    :return: Description
    :rtype: ChatAgentState
    """

    return chat_agent_handler(thread_id=thread_id, message=message)


@router.get('/chat/history/{thread_id}')
def get_chat_history(thread_id: str) -> ChatAgentState | dict[None, None]:
    """
    Docstring for get_chat_history
    
    :param thread_id: Description
    :type thread_id: str
    """
    return chat_history_handler(thread_id = thread_id)

@router.get("/chat/stream/{thread_id}")
def chat_stream(thread_id: str, message: str):
    return StreamingResponse(
        chat_streaming_handler(thread_id, message),
        media_type="text/plain"
    )

# ---- Include RAG routes ----
router.include_router(rag_router)
