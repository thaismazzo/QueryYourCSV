from typing import TypedDict, Annotated, Sequence
import streamlit as st
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage, AIMessage
from core.tools import llm_tools, tools
from logger import get_logger

logger = get_logger(__name__)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

def db_analyser(state: AgentState) -> AgentState:
    """
    Main function of the agent that consumes the database and answers questions by calling tools.

    Parameters:
        state (AgentState): Dictionary with the agent's message history.

    Returns:
        AgentState: Updated state dictionary including the new response from the agent/LLM.
    """

    if not state["messages"]:
        return state

    all_messages = list(state["messages"])
    logger.debug(f"Mensagens enviadas ao LLM: {[m.content for m in all_messages]}")
    response = llm_tools.invoke(all_messages)
    logger.info(f"Resposta do LLM: {response.content if hasattr(response, 'content') else response}")

    return {"messages": list(state["messages"]) + [response]}

def should_continue(state: AgentState) -> str:
    """
    Decides if the agent should continue or stop based on the last message.

    Parameters:
        state (AgentState): Dictionary with the agent's message history.

    Returns:
        str: "continue" to keep going, "end" to stop.
    """

    last_msg = state["messages"][-1] if state["messages"] else None
    logger.info(f"Última mensagem tipo {type(last_msg).__name__} - decidindo continuar ou encerrar")
    
    if isinstance(last_msg, HumanMessage):
        return "continue"
    elif isinstance(last_msg, AIMessage):
        return "end"
    elif isinstance(last_msg, ToolMessage):
        return "continue"
    else:
        return "end"    

printed_tools = set()
printed_messages = set()

def print_messages(messages):
    """
    Displays messages in a chatbot style
    """

    if not messages:
        return
    
    for message in messages[-1:]:
        if id(message) in printed_messages:
            continue 
        printed_messages.add(id(message))

        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)

        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)
                if hasattr(message, "tool_calls") and message.tool_calls:
                    tool_names = [tc["name"] for tc in message.tool_calls]
                    st.info(f"🔧 USING TOOLS: {tool_names}")
                    logger.info(f"Ferramentas usadas: {tool_names}")

        elif isinstance(message, ToolMessage):
            with st.chat_message("assistant"):
                st.code(message.content, language="sql")

def answer_questions(user_question, db_information):
    """
    Handles user questions by sending them to the agent, maintains message history,
    streams responses from the LLM, displays them in a chatbot style, 
    and logs both user questions and agent answers.

    Parameters:
        user_question The question asked by the user.
        db_information: Context or description of the database for the agent.

    Returns:
        str or None: The agent's answer if available, otherwise None.
    """
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if not st.session_state["messages"]:
        st.session_state["messages"].append(SystemMessage(content=db_information))

    st.session_state["messages"].append(HumanMessage(content=user_question))
    logger.info(f"Pergunta do usuário: {user_question}")

    state = {"messages": st.session_state["messages"]}

    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])
            st.session_state["messages"] = step["messages"]

    last_msg = st.session_state["messages"][-1]
    if isinstance(last_msg, AIMessage):
        logger.info(f"Resposta final do agente: {last_msg.content}")
        return last_msg.content
    return None

graph = StateGraph(AgentState)
graph.add_node("agent", db_analyser)
graph.add_node("tools", ToolNode(tools))
graph.set_entry_point("agent")
graph.add_edge("agent", "tools")
graph.add_conditional_edges(
    "tools",
    should_continue,
    {
        "continue": "agent",
        "end": END,
    })
app = graph.compile()