from langchain_core.messages import SystemMessage, HumanMessage
from core.prompts import SQL_PROMPT_TEMPLATE
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from core.preprocess import ENGINE
from sqlalchemy import text
from core.model import llm
from typing import List, Any

@tool
def generate_sql_query(db_name: str, db_description: str, user_question: str) -> List[Any]:
    """
    Generates and executes a SQL query based on a user's natural language question.

    Args:
        db_name (str): The name of the database to query.
        db_description (str): A description of the database schema and tables.
        user_question (str): The natural language question to be converted into SQL.

    Returns:
        List[Any]: A list of rows resulting from executing the generated SQL query on the database.
    """

    sql_prompt = SQL_PROMPT_TEMPLATE.format(
        db_description=db_description,
        db_name=db_name,
        user_question=user_question)
    
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=sql_prompt),
        HumanMessage(content=user_question)])

    messages = prompt.format_messages(user_question=user_question)
    response = llm.invoke(messages)
    sql_query = response.content
    sql_query = sql_query.strip().replace("```sql", "").replace("```", "").strip()

    with ENGINE.connect() as conn:
        result = conn.execute(text(sql_query))
        rows = result.fetchall()

    return rows

tools = [generate_sql_query]
llm_tools = llm.bind_tools(tools)