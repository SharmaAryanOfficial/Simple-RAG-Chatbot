from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.agents.chat_agent.states.chat_agent_state import ChatAgentState
from src.agents.chat_agent.tools.date_time import get_current_date_and_time
from src.agents.chat_agent.tools.web_search import search_the_web
from dotenv import load_dotenv
import os
from src.services.rag_service import rag_service



load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

template = """
You are a helpful assistant.

Use the following context ONLY if it is relevant to the user's question.
If the context is not relevant, answer normally.

Context:
{context}

Conversation History:
{message_history}

User Question:
{question}
"""



def chat(state: ChatAgentState) -> ChatAgentState:
    """
    """

    prompt_template = ChatPromptTemplate.from_template(template = template)
    model = ChatGroq(
        model='openai/gpt-oss-120b',
        api_key=GROQ_API_KEY
    )

    state["messages"] = state["messages"][-4:]
    # Extract latest user message
    last_message = state["messages"][-1].content

    # Retrieve RAG context (safe even if index not built)
    context = rag_service.retrieve_context(last_message)

    chain = prompt_template | model

    answer = chain.invoke({
    "message_history": state["messages"],
    "context": context,
    "question": last_message
    })


    state["messages"].append(answer)
    return state



