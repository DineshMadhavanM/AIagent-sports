# 🏆 Sports AI Agent

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/DineshMadhavanM/AIagent-sports?style=social)](https://github.com/DineshMadhavanM/AIagent-sports/stargazers)

A professional, insightful, conversational sports analyst agent. Text-only responses. Handles cricket, football (soccer), basketball, tennis, and more using both rule-based responses and AI-powered analysis.

## ✨ Features

- **Multi-sport Support**: Cricket, Football, Basketball, Tennis, and more
- **Multiple AI Backends**: Rule-based, OpenAI, and Google Gemini integration
- **Web Interface**: Beautiful, responsive web interface for easy interaction
- **CLI Tool**: Command-line interface for quick queries and automation
- **Extensible Architecture**: Easy to add new sports and features
- **Smart Responses**: Context-aware, detailed, and accurate sports information

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/DineshMadhavanM/AIagent-sports.git
   cd AIagent-sports
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root and add your API keys:
   ```
   # For Gemini AI (required for AI features)
   GOOGLE_API_KEY=your_gemini_api_key_here
   
   # For OpenAI (optional)
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🖥️ Usage

### Web Interface (Recommended)
```bash
python app.py
```
Then open `http://localhost:5000` in your browser.

### Command Line Interface
```bash
# Basic usage
python cli.py -q "Explain T20 cricket rules"

# Specify provider (rule, openai, or gemini)
python cli.py -p gemini -q "Analyze Messi's playing style"

# Get help
python cli.py --help
```

## 🏗️ Project Structure

```
AIagent-sports/
├── app.py              # Flask web application
├── cli.py              # Command-line interface
├── requirements.txt    # Python dependencies
├── sports_agent/       # Core AI agent
│   ├── __init__.py
│   ├── agent.py        # Main agent class
│   ├── prompt.py       # System prompts
│   └── providers/      # Response providers
│       ├── __init__.py
│       ├── rule_based.py
│       └── gemini_provider.py
└── templates/          # Web templates
    └── index.html
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Good First Issues
- Add support for more sports
- Improve error handling
- Add unit tests
- Enhance the web interface

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for the powerful language model
- Flask for the web framework
- All contributors and supporters

## Notes

- The rule-based provider is fully offline and fast.
- The OpenAI provider responds using the system prompt to keep answers on-topic and text-only.
- If you need tailored summaries or stats, include teams/players, competition, and timeframe in your query.
