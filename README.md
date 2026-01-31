# AutoREADME

Automatically generates and updates GitHub profile READMEs using AI.

## Setup

1. Install dependencies: `uv sync`
2. Create `.env` with:
   ```
   GH_TOKEN=your_github_token
   TOGETHER_API_KEY=your_together_api_key
   ```
3. Run: `python src/main.py`

## Features

- Fetches my public repositories from GitHub
- Generates profile README section using Together AI
- Auto-updates profile repository README

