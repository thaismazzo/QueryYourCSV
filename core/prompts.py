SQL_PROMPT_TEMPLATE = """You have access to a database with the following information:

{db_description}

The database name is {db_name}

Transform the following question into a SQL query:

{user_question}

Return ONLY the SQL
"""