from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer, 
    TrainingArguments, 
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import Dataset
import torch
import json

class MentalHealthFineTuner:
    def __init__(self, base_model="microsoft/DialoGPT-medium"):
        self.base_model = base_model
        self.tokenizer = AutoTokenizer.from_pretrained(base_model)
        self.model = AutoModelForCausalLM.from_pretrained(base_model)
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
    
    def prepare_dataset(self, data_path):
        """Prepare dataset for fine-tuning"""
        with open(data_path, 'r') as f:
            conversations = json.load(f)
        
        formatted_conversations = []
        for conv in conversations:
            text = ""
            for turn in conv['conversation']:
                if turn['speaker'] == 'user':
                    text += f"User: {turn['text']}"
                else:
                    text += f"Bot: {turn['text']}{self.tokenizer.eos_token}"
            formatted_conversations.append({'text': text})
        
        return Dataset.from_list(formatted_conversations)
    
    def tokenize_function(self, examples):
        """Tokenize the dataset"""
        return self.tokenizer(
            examples['text'],
            truncation=True,
            padding=True,
            max_length=512
        )
    
    def fine_tune(self, train_dataset, output_dir="./fine_tuned_model"):
        """Fine-tune the model"""
        tokenized_dataset = train_dataset.map(self.tokenize_function, batched=True)
        
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )
        
        training_args = TrainingArguments(
            output_dir=output_dir,
            overwrite_output_dir=True,
            num_train_epochs=3,
            per_device_train_batch_size=2,
            save_steps=500,
            save_total_limit=2,
            prediction_loss_only=True,
            learning_rate=5e-5,
            warmup_steps=100,
            logging_steps=100,
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=tokenized_dataset,
        )
        
        trainer.train()
        trainer.save_model()
        self.tokenizer.save_pretrained(output_dir)