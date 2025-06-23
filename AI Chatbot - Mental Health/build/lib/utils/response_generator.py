import random
import re

class ResponseGenerator:
    def __init__(self):
        self.supportive_phrases = [
            "I understand that must be difficult.",
            "Thank you for sharing that with me.",
            "It sounds like you're going through a lot.",
            "Your feelings are completely valid.",
            "I'm here to listen and support you."
        ]
        
        self.questions = [
            "How long have you been feeling this way?",
            "What do you think might have triggered these feelings?",
            "Have you talked to anyone else about this?",
            "What usually helps you feel better?",
            "Would you like to explore this feeling more?"
        ]
        
        self.coping_suggestions = [
            "Have you tried taking some deep breaths or doing a brief meditation?",
            "Sometimes going for a short walk can help clear your mind.",
            "Writing down your thoughts might help organize your feelings.",
            "Reaching out to a trusted friend or family member could provide support.",
            "Consider speaking with a mental health professional if these feelings persist."
        ]
    
    def enhance_response(self, generated_response, user_input):
        """Enhance the generated response for mental health context"""
        if not generated_response or len(generated_response.strip()) < 5:
            return self.get_default_response()
        
        # Check if response needs empathy boost
        if self._needs_empathy(user_input):
            supportive_phrase = random.choice(self.supportive_phrases)
            generated_response = f"{supportive_phrase} {generated_response}"
        
        # Add follow-up question occasionally
        if random.random() < 0.3:
            question = random.choice(self.questions)
            generated_response += f" {question}"
        
        return generated_response
    
    def _needs_empathy(self, user_input):
        """Check if user input indicates need for extra empathy"""
        empathy_triggers = [
            "sad", "depressed", "anxious", "worried", "scared",
            "lonely", "hopeless", "tired", "overwhelmed", "stressed"
        ]
        
        return any(trigger in user_input.lower() for trigger in empathy_triggers)
    
    def get_default_response(self):
        """Get a default supportive response"""
        defaults = [
            "I'm here to listen. How are you feeling right now?",
            "Thank you for reaching out. What's on your mind today?",
            "I want to support you. Can you tell me more about what you're experiencing?",
            "It's okay to take your time. I'm here when you're ready to share."
        ]
        return random.choice(defaults)