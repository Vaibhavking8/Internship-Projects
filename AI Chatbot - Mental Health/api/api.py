from flask import Flask, request, jsonify, render_template
from model.chatbot_model import MentalHealthChatbot
from utils.session_logger import SessionLogger
from utils.content_filter import ContentFilter
import json
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Initialize components
chatbot = MentalHealthChatbot()
session_logger = SessionLogger()
content_filter = ContentFilter()

# Store active sessions
active_sessions = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get('message', '').strip()
        session_id = data.get('session_id')
        
        if not user_input:
            return jsonify({'error': 'Empty message'}), 400
        
        # Create new session if needed
        if not session_id or session_id not in active_sessions:
            session_id = str(uuid.uuid4())
            active_sessions[session_id] = {
                'history': [],
                'created_at': datetime.now(),
                'step': 0
            }
        
        session = active_sessions[session_id]
        
        # Log user input
        session_logger.log_interaction(session_id, 'user', user_input)
        
        # Check for offensive content
        if content_filter.is_offensive(user_input):
            response = content_filter.get_empathetic_response(session['step'])
            session['step'] += 1
        else:
            # Generate response using the chatbot
            response = chatbot.generate_response(user_input, session['history'])
        
        # Update session history
        session['history'].append({'user': user_input, 'bot': response})
        
        # Log bot response
        session_logger.log_interaction(session_id, 'bot', response)
        
        return jsonify({
            'response': response,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    """Get session statistics for monitoring"""
    return jsonify({
        'active_sessions': len(active_sessions),
        'total_logged_sessions': session_logger.get_session_count()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
