# Mental Health AI Chatbot

A compassionate AI-powered chatbot designed to provide emotional support and mental health resources. Built with Flask, Transformers, and modern web technologies.

## 🌟 Features

- **AI-Powered Conversations**: Uses DialoGPT for natural, empathetic responses
- **Content Filtering**: Detects concerning content and provides appropriate responses
- **Session Logging**: Tracks user interactions for analysis and improvement
- **Crisis Resources**: Provides immediate access to mental health crisis resources
- **Multi-Interface**: Available as both Flask web app and Streamlit interface
- **Fine-tuning Ready**: Includes scripts for custom model training

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip package manager
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "AI Chatbot - Mental Health"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data**
   ```python
   import nltk
   nltk.download('stopwords')
   ```

## 🚀 Usage

### Flask Web Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - Start chatting with the AI assistant

### Streamlit Interface

1. **Run the Streamlit app**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Configure API endpoint**
   - Make sure Flask app is running on port 5000
   - Set API endpoint in sidebar if different

## 🧠 Model Fine-tuning

To fine-tune the model with your own mental health conversation data:

```python
from model.fine_tuning import MentalHealthFineTuner

# Initialize fine-tuner
fine_tuner = MentalHealthFineTuner()

# Prepare your dataset
dataset = fine_tuner.prepare_dataset('data/mental_health_conversations.json')

# Fine-tune the model
fine_tuner.fine_tune(dataset, output_dir='./custom_model')
```

## 📊 Session Logging

The chatbot automatically logs all interactions for analysis:

```python
from utils.session_logger import SessionLogger

logger = SessionLogger()

# Get session statistics
session_count = logger.get_session_count()

# Export to CSV for analysis
logger.export_to_csv('analysis/sessions.csv')
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
MODEL_NAME=microsoft/DialoGPT-medium
LOG_LEVEL=INFO
```

### Content Filtering
Customize offensive words and mental health keywords in `utils/content_filter.py`:

```python
self.offensive_words = {
    "your", "custom", "words", "here"
}

self.mental_health_keywords = {
    "anxiety", "depression", "custom", "keywords"
}
```

## 🌐 Deployment

### Render Deployment

1. **Connect your repository to Render**
2. **Set build command**: `pip install -r requirements.txt`
3. **Set start command**: `gunicorn app:app`
4. **Add environment variables** in Render dashboard

### Replit Deployment

1. **Import repository to Replit**
2. **Set run command**: `python app.py`
3. **Install dependencies** automatically handled

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## 🔒 Safety Features

- **Content Filtering**: Automatically detects concerning language
- **Crisis Detection**: Identifies crisis situations and provides resources
- **Empathetic Responses**: Provides supportive responses for difficult emotions
- **Resource Links**: Easy access to mental health crisis resources
- **Session Boundaries**: Clear disclaimers about AI limitations

## 📈 Monitoring and Analytics

### Session Analytics
- Track conversation patterns
- Monitor crisis interventions
- Analyze user engagement metrics
- Export data for research (anonymized)

### Model Performance
- Response quality assessment
- User satisfaction tracking
- Content filter effectiveness
- Response time monitoring

## 🙏 Acknowledgments

- Hugging Face Transformers for the AI models
- Microsoft for DialoGPT
- Mental health organizations for guidance and resources
- Open source community for tools and libraries
