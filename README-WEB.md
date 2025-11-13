# Sports AI Agent - Web Interface

This adds a web interface to the Sports AI Agent using Flask.

## Setup

1. Install the required packages:
   ```bash
   pip install -r requirements-web.txt
   ```

2. Copy the example environment file and configure:
   ```bash
   copy .env.example .env
   ```
   - Edit `.env` and set `SPORTS_AGENT_PROVIDER` to `rule` (default) or `openai`
   - If using OpenAI, add your API key

## Running the Web App

```bash
python app.py
```

Then open your browser to: http://localhost:5000

## Features

- Clean, responsive web interface
- Example queries to get you started
- Loading indicators during API calls
- Error handling
- Works with both rule-based and OpenAI providers

## Development

- The web app uses Flask for the backend
- Frontend is vanilla HTML/CSS/JS (no build step required)
- Main files:
  - `app.py` - Flask application
  - `templates/index.html` - Web interface
  - `static/styles.css` - Styling (if needed)
  - `static/script.js` - Frontend logic (if needed)
