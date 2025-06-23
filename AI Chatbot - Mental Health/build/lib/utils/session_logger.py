import json
import os
from datetime import datetime
import pandas as pd

class SessionLogger:
    def __init__(self, log_file="logs/user_sessions.log"):
        self.log_file = log_file
        self.ensure_log_directory()
    
    def ensure_log_directory(self):
        """Ensure the logs directory exists"""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
    
    def log_interaction(self, session_id, speaker, message):
        """Log a single interaction"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'speaker': speaker,
            'message': message
        }
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def get_session_data(self, session_id):
        """Retrieve all interactions for a specific session"""
        interactions = []
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        if entry['session_id'] == session_id:
                            interactions.append(entry)
                    except json.JSONDecodeError:
                        continue
        return interactions
    
    def get_session_count(self):
        """Get total number of unique sessions"""
        sessions = set()
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        sessions.add(entry['session_id'])
                    except json.JSONDecodeError:
                        continue
        return len(sessions)
    
    def export_to_csv(self, output_file="logs/sessions_export.csv"):
        """Export session logs to CSV"""
        interactions = []
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        interactions.append(entry)
                    except json.JSONDecodeError:
                        continue
        
        if interactions:
            df = pd.DataFrame(interactions)
            df.to_csv(output_file, index=False)
            return output_file
        return None