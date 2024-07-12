import streamlit as st
import requests
import subprocess
import atexit
import os
import signal
import time
import pandas as pd
import plotly.express as px

def main():
    st.set_page_config(page_title="Multilingual RAG", page_icon="🌍", layout="wide")
    
    st.title("🌍 Not Free Multilingual RAG")

    with st.sidebar:
        st.header("ℹ️ About")
        st.info("This app allows you to upload documents and ask questions about them using RAG technology.")
        
        st.header("⚙️ Settings")
        language = st.selectbox("Select Language", ["English", "Türkçe", "Español", "Français", "Deutsch"])
        theme = st.radio("Theme", ["Light", "Dark"])
        if theme == "Dark":
            st.markdown('<style>body {background-color: #1E1E1E; color: white;}</style>', unsafe_allow_html=True)

    tabs = ["📤 Upload Document", "❓ Ask Question", "📊 Analytics"]
    active_tab = st.radio("Select Operation:", tabs)

    if active_tab == "📤 Upload Document":
        upload_document()
    elif active_tab == "❓ Ask Question":
        ask_question()
    else:
        show_analytics()

def upload_document():
    st.header("📤 Upload Document")
    st.write("Several files can be uploaded. Each upload overwrites the previous ones.")
    
    username = st.text_input("👤 Enter a username:", help="Choose a username that represents you")
    
    uploaded_files = st.file_uploader("📂 Upload your documents:", accept_multiple_files=True, 
                                      help="Supported formats: .txt, .pdf, .docx")
    
    if uploaded_files:
        st.write(f"Number of uploaded files: {len(uploaded_files)}")
        
        file_details = []
        for uploaded_file in uploaded_files:
            file_details.append({
                "File Name": uploaded_file.name,
                "File Type": uploaded_file.type,
                "File Size (KB)": round(uploaded_file.size / 1024, 2)
            })
        st.table(pd.DataFrame(file_details))
    
    upload_button = st.button("📤 Upload")
    
    if upload_button and uploaded_files:
        if not username:
            st.warning("⚠️ Please enter a username.")
        else:
            files = [("files", (uploaded_file.name, uploaded_file, uploaded_file.type)) for uploaded_file in uploaded_files]
            payload = {'username': username}
            
            with st.spinner('📊 Processing documents...'):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.2)
                    progress_bar.progress(i + 1)
                
                response = requests.post("http://localhost:8000/document-uploader/", files=files, data=payload)
            
            if response.status_code == 200:
                try:
                    response_json = response.json()
                    if isinstance(response_json, dict):
                        st.success(response_json.get("message", "Success"))
                    else:
                        st.success("Success")
                    st.balloons()
                except ValueError:
                    st.error("Failed to parse the response.")
            else:
                st.error(f"Error: {response.text}")
    elif upload_button and not uploaded_files:
        st.warning("⚠️ Please select files to upload.")

def ask_question():
    st.header("❓ Ask Question")
    
    username = st.text_input("👤 Enter a username:", help="Use the same username you used for uploading documents")
    api_key = st.text_input("🔑 OpenAI API key:", type="password", help="Your API key will be kept secure")
    
    question = st.text_area("🤔 Enter your question:", 
                            help="The more detailed your question, the more accurate the answer will be")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        ask_button = st.button("🚀 Ask")
    with col2:
        confidence = st.slider("Set confidence threshold:", 0.0, 1.0, 0.7, 0.1, 
                               help="Higher values will result in more focused but potentially less creative answers")
    
    if ask_button:
        if not question:
            st.warning("⚠️ Please enter a question.")
        elif not username:
            st.warning("⚠️ Please enter a username.")
        else:
            payload = {'username': username, 'question': question, 'api_key': api_key, 'confidence': confidence}
            with st.spinner('🧠 Thinking...'):
                response = requests.post("http://localhost:8000/question-answerer/", data=payload)
            
            if response.status_code == 200:
                try:
                    response_json = response.json()
                    if isinstance(response_json, dict):
                        answer = response_json.get('answer', 'No answer provided')
                        st.success(f"Answer: {answer}")
                    else:
                        st.success("Answer received")
                except ValueError:
                    st.error("Failed to parse the response.")
            else:
                st.error(f"Error: {response.text}")
def show_analytics():
    st.header("📊 Analytics")
    st.write("Here you can view analytics about your document uploads and questions.")

    upload_data = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', periods=10),
        'Uploads': [5, 7, 3, 8, 12, 6, 9, 11, 4, 7]
    })
    
    question_data = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', periods=10),
        'Questions': [10, 15, 8, 20, 25, 18, 22, 30, 12, 17]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Document Uploads Over Time")
        fig_uploads = px.line(upload_data, x='Date', y='Uploads', title='Document Uploads')
        st.plotly_chart(fig_uploads)
    
    with col2:
        st.subheader("Questions Asked Over Time")
        fig_questions = px.line(question_data, x='Date', y='Questions', title='Questions Asked')
        st.plotly_chart(fig_questions)

uvicorn_process = None

import streamlit as st
import requests
import subprocess
import atexit
import os
import signal
import time
import pandas as pd
import plotly.express as px

def main():
    st.set_page_config(page_title="Free Multilingual RAG", page_icon="🌍", layout="wide")
    
    st.title("🌍 Not Free Multilingual RAG")
    
    # Sidebar for additional info and settings
    with st.sidebar:
        st.header("ℹ️ About")
        st.info("This app allows you to upload documents and ask questions about them using RAG technology.")
        
        st.header("⚙️ Settings")
        language = st.selectbox("Select Language", ["English", "Türkçe", "Español", "Français", "Deutsch"])
        theme = st.radio("Theme", ["Light", "Dark"])
        if theme == "Dark":
            st.markdown('<style>body {background-color: #1E1E1E; color: white;}</style>', unsafe_allow_html=True)

    tabs = ["📤 Upload Document", "❓ Ask Question", "📊 Analytics"]
    active_tab = st.radio("Select Operation:", tabs)

    if active_tab == "📤 Upload Document":
        upload_document()
    elif active_tab == "❓ Ask Question":
        ask_question()
    else:
        show_analytics()

def upload_document():
    st.header("📤 Upload Document")
    st.write("Several files can be uploaded. Each upload overwrites the previous ones.")
    
    username = st.text_input("👤 Enter a username:", help="Choose a username that represents you")
    
    uploaded_files = st.file_uploader("📂 Upload your documents:", accept_multiple_files=True, 
                                      help="Supported formats: .txt, .pdf, .docx")
    
    if uploaded_files:
        st.write(f"Number of uploaded files: {len(uploaded_files)}")
        
        # Display file details in a table
        file_details = []
        for uploaded_file in uploaded_files:
            file_details.append({
                "File Name": uploaded_file.name,
                "File Type": uploaded_file.type,
                "File Size (KB)": round(uploaded_file.size / 1024, 2)
            })
        st.table(pd.DataFrame(file_details))
        
        files = [("files", (uploaded_file.name, uploaded_file, uploaded_file.type)) for uploaded_file in uploaded_files]
        payload = {'username': username}
        
        with st.spinner('📊 Processing documents...'):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.1)
                progress_bar.progress(i + 1)
            
            response = requests.post("http://localhost:8000/document-uploader/", files=files, data=payload)
        
        if response.status_code == 200:
            try:
                response_json = response.json()
                if isinstance(response_json, dict):
                    st.success(response_json.get("message", "Success"))
                else:
                    st.success("Success")
                st.balloons()
            except ValueError:
                st.error("Failed to parse the response.")
        else:
            st.error(f"Error: {response.text}")

def ask_question():
    st.header("❓ Ask Question")
    
    username = st.text_input("👤 Enter a username:", help="Use the same username you used for uploading documents")
    api_key = st.text_input("🔑 OpenAI API key:", type="password", help="Your API key will be kept secure")
    
    question = st.text_area("🤔 Enter your question:", 
                            help="The more detailed your question, the more accurate the answer will be")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        ask_button = st.button("🚀 Ask")
    with col2:
        confidence = st.slider("Set confidence threshold:", 0.0, 1.0, 0.7, 0.1)
    
    if ask_button:
        if not question:
            st.warning("⚠️ Please enter a question.")
        elif not username:
            st.warning("⚠️ Please enter a username.")
        else:
            payload = {'username': username, 'question': question, 'api_key': api_key, 'confidence': confidence}
            with st.spinner('🧠 Thinking...'):
                response = requests.post("http://localhost:8000/question-answerer/", data=payload)
            
            if response.status_code == 200:
                try:
                    response_json = response.json()
                    if isinstance(response_json, dict):
                        answer = response_json.get('answer', 'No answer provided')
                        st.success(f"Answer: {answer}")
                        
                        
                    else:
                        st.success("Answer received")
                except ValueError:
                    st.error("Failed to parse the response.")
            else:
                st.error(f"Error: {response.text}")

def show_analytics():
    st.header("📊 Analytics")
    st.write("Here you can view analytics about your document uploads and questions.")
    
    # Dummy data for demonstration
    upload_data = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', periods=10),
        'Uploads': [5, 7, 3, 8, 12, 6, 9, 11, 4, 7]
    })
    
    question_data = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', periods=10),
        'Questions': [10, 15, 8, 20, 25, 18, 22, 30, 12, 17]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Document Uploads Over Time")
        fig_uploads = px.line(upload_data, x='Date', y='Uploads', title='Document Uploads')
        st.plotly_chart(fig_uploads)
    
    with col2:
        st.subheader("Questions Asked Over Time")
        fig_questions = px.line(question_data, x='Date', y='Questions', title='Questions Asked')
        st.plotly_chart(fig_questions)

uvicorn_process = None

def run_fastapi():
    global uvicorn_process
    if uvicorn_process is None:
        uvicorn_process = subprocess.Popen(["uvicorn", "service:app", "--host", "127.0.0.1", "--port", "8000"])
        print("FastAPI server has been started.")

def cleanup():
    global uvicorn_process
    if uvicorn_process:
        os.kill(uvicorn_process.pid, signal.SIGTERM)
        uvicorn_process.wait()
        print("FastAPI server has been closed.")

if __name__ == "__main__":
    run_fastapi()
    atexit.register(cleanup)
    main()
