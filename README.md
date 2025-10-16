# BHAVESH GPT - AI Chatbot Application

A Flask-based web application that integrates with OpenAI's GPT models to create an intelligent chatbot.

## Features

- 🤖 Real-time chat interface with GPT-3.5-turbo
- 🎨 Modern dark-themed UI
- ⚡ Fast and responsive
- 🔒 Secure API key management
- 📱 Mobile-friendly design

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
1. Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Edit the `.env` file and replace `your_openai_api_key_here` with your actual API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

### 3. Run the Application
```bash
python app.py
```

### 4. Access the Application
Open your browser and navigate to: `http://localhost:5000`

## File Structure

```
BHAVESH GPT/
├── app.py              # Main Flask application
├── index.html          # Chat interface
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (API key)
└── __pycache__/       # Python cache files
```

## Customization

- **Change GPT Model**: Edit `app.py` line 29 to use `gpt-4` if you have access
- **Modify System Prompt**: Edit the system message in `app.py` line 31
- **Adjust Response Length**: Modify `max_tokens` in `app.py` line 34
- **UI Styling**: Edit the CSS in `index.html`

## Troubleshooting

- **API Key Error**: Make sure your API key is correctly set in the `.env` file
- **Connection Error**: Check if your internet connection allows API calls to OpenAI
- **Port Issues**: If port 5000 is busy, the app will show an error

## Security Note

Never commit your `.env` file to version control. It contains sensitive API keys.
