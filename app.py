import streamlit as st
from core.preprocess import consume_db
from core.agents import answer_questions
from logger import get_logger

logger = get_logger(__name__)

st.set_page_config(page_title="CSV Q&A Agent", page_icon="📊")
st.title("📈 Ask questions on your database")

if st.button("🔄 Restart"):
    st.session_state.clear()
    logger.info("Session restarted by user")
    st.rerun()

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
with st.form(key="schema_form"):
    schema_description = st.text_input("Enter your database schema description")
    submit_schema = st.form_submit_button("Submit")

if "chat" not in st.session_state:
    st.session_state["chat"] = []

if uploaded_file and schema_description and submit_schema:
    if "db_information" not in st.session_state:
        try:
            df, table, db_information = consume_db(uploaded_file, schema_description)
            st.session_state["df"] = df
            st.session_state["table"] = table
            st.session_state["db_information"] = db_information
            st.success(f"✅ Database successfully created! Table available as '{table.name}'")
            logger.info(f"Database successfully created: {table.name}")
        except Exception as e:
            st.error(f"Error consuming database: {e}")
            logger.error(f"Error consuming database: {e}", exc_info=True)

if uploaded_file and schema_description:
    if "df" in st.session_state:
        st.write("📄 Data preview:")
        st.dataframe(st.session_state["df"].head())

        for role, msg in st.session_state["chat"]:
            with st.chat_message(role):
                st.markdown(msg)

        if prompt := st.chat_input("Type your question..."):

            try:
                st.session_state["chat"].append(("user", prompt))
                with st.spinner("Thinking..."):
                    response = answer_questions(prompt, st.session_state["db_information"])
                logger.info(f"Agent response: {response}")

                st.session_state["chat"].append(("assistant", response))
            except Exception as e:
                st.error(f"Error generating response: {e}")
                logger.error(f"Error answering question: {e}", exc_info=True)
