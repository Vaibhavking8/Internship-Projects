import re
import torch
import nltk
from nltk.corpus import stopwords
from transformers import AutoModelForCausalLM, AutoTokenizer

nltk.download('stopwords')

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Store conversations for different users
user_histories = {}

OFFENSIVE_WORDS = {"idiot", "stupid", "dumb", "hate", "kill", "suicide", "worthless"}

def is_offensive(text):
    cleaned = re.sub(r"[^a-zA-Z ]", "", text.lower())
    tokens = set(cleaned.split()) - set(stopwords.words('english'))
    return bool(tokens & OFFENSIVE_WORDS)

def get_empathetic_response(step=0):
    responses = [
        "I'm really sorry you're feeling this way. You're not alone—there are people who care about you.",
        "It sounds like you're going through a difficult time. I'm here for you.",
        "Your emotions are valid. Let's talk more about what's going on.",
        "If you're feeling overwhelmed, it might help to talk to a mental health professional. You're not alone.",
    ]
    return responses[step % len(responses)]

def get_bot_response(user_input, user_id="default"):
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # Maintain chat history per user
    if user_id not in user_histories:
        user_histories[user_id] = None

    bot_input_ids = torch.cat([user_histories[user_id], new_input_ids], dim=-1) if user_histories[user_id] is not None else new_input_ids
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    user_histories[user_id] = chat_history_ids
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response
