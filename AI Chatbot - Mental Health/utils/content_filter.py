import re
import nltk
from nltk.corpus import stopwords
import json

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class ContentFilter:
    def __init__(self):
        self.offensive_words = {
            "idiot", "stupid", "dumb", "hate", "kill", "suicide", 
            "depressed", "worthless", "useless", "failure", "loser",
            "die", "death", "hurt", "pain", "hopeless", "helpless"
        }
        
        self.mental_health_keywords = {
            "anxious", "anxiety", "depressed", "depression", "sad",
            "lonely", "overwhelmed", "stressed", "panic", "worry",
            "scared", "afraid", "hopeless", "tired", "exhausted"
        }
        
        self.empathetic_responses = [
            "I'm really sorry you're feeling this way. You're not alone—there are people who care about you.",
            "It sounds like you're going through a difficult time. I'm here to listen and support you.",
            "Your feelings are completely valid. It's okay to feel overwhelmed sometimes.",
            "Thank you for sharing that with me. It takes courage to express difficult emotions.",
            "I can hear that you're struggling right now. Would you like to talk more about what's going on?",
            "Remember that difficult times don't last forever. You've gotten through hard times before.",
            "It's important that you're reaching out. That shows real strength, even when you don't feel strong."
        ]
    
    def is_offensive(self, text):
        """Check if text contains offensive or concerning content"""
        cleaned = re.sub(r"[^a-zA-Z ]", "", text.lower())
        tokens = set(cleaned.split()) - set(stopwords.words('english'))
        return bool(tokens & self.offensive_words)
    
    def contains_mental_health_keywords(self, text):
        """Check if text contains mental health related keywords"""
        cleaned = re.sub(r"[^a-zA-Z ]", "", text.lower())
        tokens = set(cleaned.split())
        return bool(tokens & self.mental_health_keywords)
    
    def get_empathetic_response(self, step=0):
        """Get an empathetic response based on conversation step"""
        return self.empathetic_responses[step % len(self.empathetic_responses)]
