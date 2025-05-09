import streamlit as st
from api_utils import upload_document, list_documents, delete_document
import time

def display_sidebar():
    # Sidebar: Model Selection
    model_options = ["gpt-4o", "gpt-4o-mini"]
    st.sidebar.selectbox("Select Model", options=model_options, key="model")

    # Sidebar: Upload Document
    st.sidebar.header("Upload Document")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "docx", "html", "txt", "csv", "json", "xlsx", "pptx"])
  
    # Lấy dept_id từ session state hoặc cấu hình
    dept_id = st.session_state.get("dept_id", 0)  # Default dept_id = 0 nếu không có
    

    # Thêm các trường nhập liệu cho upload_link và effective_date
    upload_link = st.sidebar.text_input("Link to File", placeholder="Enter the link")
    effective_date = st.sidebar.date_input("Effective Date")

    if uploaded_file is not None:
        cooldown = 10  # seconds
        now = time.time()
        last_upload = st.session_state.get("last_upload_time", 0)

        if now - last_upload < cooldown:
            st.sidebar.warning(f"⏳ Please wait {cooldown - int(now - last_upload)}s before uploading again.")
        else:
            if st.sidebar.button("Upload"):
                with st.spinner("Uploading..."):
                    upload_response = upload_document(uploaded_file, dept_id, upload_link, effective_date)
                    if upload_response:
                        st.session_state["last_upload_time"] = now
                        st.sidebar.success(f"File '{uploaded_file.name}' uploaded successfully with ID {upload_response['file_id']}.")
                        st.session_state.documents = list_documents(dept_id)  # Refresh the list

    # Sidebar: List Documents
    st.sidebar.header("Uploaded Documents")
    if st.sidebar.button("Refresh Document List"):
        with st.spinner("Refreshing..."):
            st.session_state.documents = list_documents(dept_id)

    # Initialize document list if not present
    if "documents" not in st.session_state:
        st.session_state.documents = list_documents(dept_id)

    documents = st.session_state.documents
    if documents:
        for doc in documents:
            st.sidebar.markdown(
                f"- **{doc['filename']}** (ID: {doc['id']}) - [Link]({doc.get('upload_link', 'N/A')}) | Effective: {doc.get('effective_date', 'N/A')}"
            )
        if (st.session_state.get("roles") == ["admin"]) or True:
            # Delete Document
            selected_file_id = st.sidebar.selectbox(
                "Select a document to delete",
                options=[doc['id'] for doc in documents],
                format_func=lambda x: next(doc['filename'] for doc in documents if doc['id'] == x)
            )
            if st.sidebar.button("Delete Selected Document"):
                with st.spinner("Deleting..."):
                    delete_response = delete_document(selected_file_id, dept_id)
                    if delete_response:
                        st.sidebar.success(f"Document with ID {selected_file_id} deleted successfully.")
                        st.session_state.documents = list_documents(dept_id)  # Refresh the list after deletion
                    else:
                        st.sidebar.error(f"Failed to delete document with ID {selected_file_id}.")