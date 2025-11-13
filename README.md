# Sports Text-Only AI Agent

A professional, insightful, conversational sports analyst agent. Text-only responses. Handles cricket, football (soccer), basketball, tennis, and more.

## Features

- Explains rules, formats, and scoring systems
- Provides match summaries and analysis
- Discusses player statistics and trends
- Generates commentary-style text or reports
- Offers news-style briefs and hypothetical predictions (no real-time data)
- General sports knowledge Q&A

## Quickstart

1) Create a virtual environment and install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2) Run the CLI (rule-based provider by default)

```bash
python cli.py -q "Explain T20 cricket rules"
python cli.py -q "Match summary: Team A vs Team B in football"
python cli.py -q "Basketball stats to compare two guards"
python cli.py -q "Commentary style for a tennis game"
python cli.py -q "News brief preview: two IPL teams clash"
```

3) Optional: Use OpenAI provider

- Set environment variables and run with provider `openai`

```bash
set OPENAI_API_KEY=your_key_here
python cli.py -p openai -q "Explain offside rule in football"
```

You can also control the model with `-m` or `OPENAI_MODEL`.

## Programmatic usage

```python
from sports_agent import SportsAgent
agent = SportsAgent(provider="rule")
print(agent.respond("Explain basketball scoring"))
```

## Notes

- The rule-based provider is fully offline and fast.
- The OpenAI provider responds using the system prompt to keep answers on-topic and text-only.
- If you need tailored summaries or stats, include teams/players, competition, and timeframe in your query.
