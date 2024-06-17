import streamlit as st
import sys

# Get Python version information
python_version = sys.version
version_info = sys.version_info

# Streamlit app
st.title("Python Version Information")

st.write("**Python version:**")
st.text(python_version)

st.write("**Version info:**")
st.text(f"Major: {version_info.major}")
st.text(f"Minor: {version_info.minor}")
st.text(f"Micro: {version_info.micro}")
st.text(f"Release level: {version_info.releaselevel}")
st.text(f"Serial: {version_info.serial}")

"""
# Internal Modules
from utils.vectordb import to_db
from utils.search import chatbot
# External Modules
import streamlit as st
from time import sleep
from random import randint
import os

# Streamlit UI
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
            if output.lower() in ["quit", "exit", "ㅃㅃ"]:
                exit()
            sys.stdout = old_stdout
            
            # Display the output using an expander with a scrollbar
            st.write(output)
    else:
        st.warning("Please enter a question.")
"""