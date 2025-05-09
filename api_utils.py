import os
from dotenv import load_dotenv
import requests
import streamlit as st

# Load environment variables from .env file
#load_dotenv()

#API_HOST = os.getenv("API_HOST", "http://localhost:8000")  # Default to localhost if not set
API_HOST = os.getenv('LANGCHAIN_API_URL', 'http://langchain-container:8000')

def get_api_response(question, session_id, model):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "question": question,
        "model": model,
    }
    if session_id:
        data["session_id"] = session_id

    try:
        response = requests.post(f"{API_HOST}/chat", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API request failed with status code {response.status_code}: {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def upload_document(file, dept_id, upload_link, effective_date):
    print(f"Uploading file... Dept ID: {dept_id}, Upload Link: {upload_link}, Effective Date: {effective_date}")
    try:
        files = {"file": (file.name, file, file.type)}
        data = {
            "dept_id": dept_id,
            "upload_link": upload_link,
            "effective_date": effective_date
        }

        response = requests.post(f"{API_HOST}/upload-doc", files=files, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to upload file. Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while uploading the file: {str(e)}")
        return None

def list_documents(dept_id):
    try:
        params = {"dept_id": dept_id}
        response = requests.get(f"{API_HOST}/list-docs", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch document list. Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        st.error(f"An error occurred while fetching the document list: {str(e)}")
        return []

def delete_document(file_id, dept_id):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {"file_id": file_id, "dept_id": dept_id}

    try:
        response = requests.post(f"{API_HOST}/delete-doc", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to delete document. Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occurred while deleting the document: {str(e)}")
        return None