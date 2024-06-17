__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# Internal Modules
from utils.vectordb import to_db
from utils.search import chatbot
# External Modules
import streamlit as st
from time import sleep
from random import randint
import warnings
import os

#Ignore warning
warnings.filterwarnings('ignore')
# Streamlit UI
st.set_page_config(
    page_title='유해 위험 가이드 챗봇',
    page_icon='https://i.namu.wiki/i/NgVoid2KU7eIGUnYVeZKBcfdydT9zq9_l69cYGpP1LwOFKn4nnbHe_OhsE3MWPcDtt6jqST_9tUSjyuNw3lNzw.svg',
    initial_sidebar_state='collapsed'
)
st.title("유해 위험 가이드 챗봇")
# Sidebar for setting up the database
st.sidebar.header("Database Setup")
if st.sidebar.button("Build Database"):
    with st.spinner("Building database..."):
        to_db(r"src\법규")
        st.sidebar.success("Database built successfully!")
# Main area for asking questions
with st.form(key="question_form"):
    question = st.text_input("Enter your question:")
    submit_button = st.form_submit_button(label="Get Answer")

if submit_button:
    if question:
        with st.spinner("Retrieving answer..."):
            db_directory = "db/chroma_db"
            # Temporarily redirect stdout to capture the print output
            from io import StringIO
            import sys
            
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            chatbot(db_directory=db_directory, question=question)
            
            output = sys.stdout.getvalue()
            if output.lower() in ["quit", "exit", "ㅃㅃ", "ㅂㅇ"]:
                exit()
            sys.stdout = old_stdout
            
            # Display the output using an expander with a scrollbar
            st.write(output)
    else:
        st.warning("Please enter a question.")
