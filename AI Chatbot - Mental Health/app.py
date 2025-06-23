import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Mental Health AI Chatbot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
    }
    
    .chat-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .user-message {
        background: #007bff;
        color: white;
        padding: 10px 15px;
        border-radius: 20px 20px 5px 20px;
        margin: 5px 0 5px auto;
        max-width: 70%;
        text-align: right;
    }
    
    .bot-message {
        background: #e9ecef;
        color: #333;
        padding: 10px 15px;
        border-radius: 20px 20px 20px 5px;
        margin: 5px auto 5px 0;
        max-width: 70%;
    }
    
    .crisis-info {
        background: #fff3cd;
        border: 1px solid #ffeeba;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = None

# Sidebar
with st.sidebar:
    st.header("🛠️ Settings")
    
    # API endpoint configuration
    api_url = st.text_input(
        "API Endpoint", 
        value="http://localhost:5000/api/chat",
        help="URL of the Flask API endpoint"
    )
    
    st.header("ℹ️ About")
    st.info("""
    This chatbot is designed to provide emotional support and a listening ear. 
    
    **Important:** This is not a replacement for professional mental health care. 
    If you're experiencing a crisis, please contact emergency services or a crisis hotline.
    """)
    
    # Crisis resources
    st.header("🆘 Crisis Resources")
    st.markdown("""
    - **National Suicide Prevention Lifeline**: 988
    - **Crisis Text Line**: Text HOME to 741741
    - **National Domestic Violence Hotline**: 1-800-799-7233
    """)
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.session_id = None
        st.rerun()

# Main content
st.markdown('<div class="main-header"><h1>🧠 Mental Health Support Chatbot</h1><p>A compassionate AI companion for emotional support</p></div>', unsafe_allow_html=True)

# Display chat messages
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Share what's on your mind...")

if user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Prepare API request
    payload = {
        "message": user_input,
        "session_id": st.session_state.session_id
    }
    
    try:
        # Make API request
        with st.spinner("Thinking..."):
            response = requests.post(api_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            bot_response = data.get('response', 'I apologize, but I had trouble generating a response.')
            st.session_state.session_id = data.get('session_id')
            
            # Add bot response to chat
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
        else:
            st.error(f"API Error: {response.status_code}")
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "I'm sorry, I'm having technical difficulties. Please try again."
            })
    
    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: {str(e)}")
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "I'm having trouble connecting right now. Please make sure the API is running and try again."
        })
    
    # Rerun to display new messages
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>This chatbot uses AI to provide emotional support. Remember that you're not alone, and professional help is available when needed.</p>
    <p><small>Built with ❤️ for mental health awareness</small></p>
</div>
""", unsafe_allow_html=True)