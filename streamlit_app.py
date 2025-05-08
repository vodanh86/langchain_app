import streamlit as st
from sidebar import display_sidebar
from chat_interface import display_chat_interface
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

#hashed_passwords = stauth.Hasher.hash_passwords(config['credentials'])
#print(hashed_passwords)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

try:
    authenticator.login()
except Exception as e:
    st.error(e)

if st.session_state.get('authentication_status'):
    user_info = config['credentials']['usernames'].get(st.session_state.username, {})
    st.session_state['dept_id'] = user_info.get('dept_id', 0)  # Default dept_id = 0 nếu không có
  
    authenticator.logout()
    st.title("Langchain RAG Chatbot")

    # Initialize session state variables
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "session_id" not in st.session_state:
        st.session_state.session_id = None

    # Display the sidebar
    display_sidebar()

    # Display the chat interface
    display_chat_interface()

elif st.session_state.get('authentication_status') is False:
    st.error('Username/password is incorrect')
elif st.session_state.get('authentication_status') is None:
    st.warning('Please enter your username and password')