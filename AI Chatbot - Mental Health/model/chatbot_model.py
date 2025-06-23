import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from utils.response_generator import ResponseGenerator
import json
import os

class MentalHealthChatbot:
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.response_generator = ResponseGenerator()
        self.load_model()
    
    def load_model(self):
        """Load the pre-trained model and tokenizer"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Add padding token if it doesn't exist
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def generate_response(self, user_input, conversation_history=None):
        """Generate response for user input"""
        try:
            # Prepare input with conversation context
            if conversation_history:
                context = self._build_context(conversation_history[-3:])  # Last 3 exchanges
                full_input = f"{context}{user_input}"
            else:
                full_input = user_input
            
            # Tokenize input
            input_ids = self.tokenizer.encode(
                full_input + self.tokenizer.eos_token,
                return_tensors='pt'
            )
            
            # Generate response
            with torch.no_grad():
                output = self.model.generate(
                    input_ids,
                    max_length=input_ids.shape[1] + 100,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    attention_mask=torch.ones(input_ids.shape, dtype=torch.long)
                )
            
            # Decode response
            response = self.tokenizer.decode(
                output[0][input_ids.shape[1]:],
                skip_special_tokens=True
            ).strip()
            
            # Post-process response for mental health context
            response = self.response_generator.enhance_response(response, user_input)
            
            return response if response else self.response_generator.get_default_response()
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return self.response_generator.get_default_response()
    
    def _build_context(self, history):
        """Build conversation context from history"""
        context = ""
        for exchange in history:
            context += f"User: {exchange['user']}\nBot: {exchange['bot']}\n"
        return context