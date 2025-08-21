## QueryYourCSV

QueryYourCSV is a project that leverages **Text-to-SQL** technique to analyze `.csv` databases.  
It enables users to ask questions in natural language and explore their CSV files effortlessly, making it easier to extract meaningful insights from their data.

---

## 🔧 Tools and Techniques

This workflow was built with python as backend and streamlit as frontend. We are using a common **agentic AI framework** called **LangGraph**. We have a main node which is called 'db_analyser'. This main agent has access to a tool called 'generate_sql_query'. This tool is called whenever the agent needs an answer based on a SQL query.

For the database we are using SQLite, which means that the database will be saved locally.

For processing the .csv file we are using pandas python lib.

---

## 📝 Project Structure

| Folder / File | Description |
|---------------|-------------|
| `core/agents.py` | Defines the AI agents that process questions and interact with tools. |
| `core/tools.py` | Implements the tools available to agents, e.g., `generate_sql_query`. |
| `core/model.py` | Configuration of the LLM (Large Language Model) used by the agents. |
| `core/preprocess` | Scripts for processing and cleaning `.csv` files. |
| `core/prompts` | Prompts used by agents (organized for clean code). |
| `app.py` | Main **Streamlit** app that provides the user interface. |
| `logger.py` | Logging utility to help track the flow and debug steps. |

---
## 🚀 How to Use

### 1. Clone the repository
```bash
git clone https://github.com/thaismazzo/QueryYourCSV.git
cd QueryYourCSV
```
### 2. Insert .env with your OPENAI_API_KEY. Please be aware that you can change the model of your preference on the folder core/model.py
### 3. Open your Docker Engine
### 4. In the terminal of your project, inside TextToSql folder, run:
```bash
docker build -t meu_app_streamlit .
docker run -it --rm -p 8501:8501 meu_app_streamlit
```
### 5. Open the link for your localhost, usually: http://localhost:8501/
### 6. You will then see the frontend of our application. Input the provided .csv file and have fun asking questions and exploring your database with natural language :)
