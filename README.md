# Narrative AI: LinkedIn Post Generator with AI Agents 🤖

## Overview
An intelligent LinkedIn post generation system powered by AI agents, built to create engaging, research-backed professional content.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Configuration](#configuration)
- [Technologies Used](#technologies-used)

## Features
- 🎯 Research-backed content generation
- 🔍 Web scraping and data analysis
- 📝 Intelligent prompt engineering
- 🌐 Brave Search integration
- 📊 Structured output generation
- 🎨 Professional post formatting

## Requirements
- Python 3.x
- Google AI API key (Gemini)
- Brave Search API key
- Required Python packages (see `requirements.txt`)

## Installation
1. Clone the repository
```bash
git clone <repository-url>
cd narrative-ai
```

2. Install dependencies
```bash
pip install -r requirements.txt

# Install and setup Playwright for web scraping
pip install playwright
playwright install
```

3. Setup environment variables
```bash
# Create .env file from template
copy .example.env .env

# Add your API keys to .env
GOOGLE_API_KEY=your_gemini_api_key
BRAVE_API_KEY=your_brave_search_key
```

> **Note**: Playwright is required for web scraping functionality. Make sure to run both the install commands to set up the browser automation

## Project Structure
```
narrative-ai/
├── post_gen_app.py      # Main Streamlit application
├── post_gen_agent.py    # Agent workflow implementation
├── structured_models.py  # Pydantic data models
├── instructions.py      # Agent instructions
├── requirements.txt     # Project dependencies
└── .env                # Environment variables
```

## Usage
1. Start the Streamlit application:
```bash
streamlit run post_gen_app.py
```

2. Enter your prompt with the following details:
   - Topic/URL: Your main topic or URL to research
   - Target Audience: e.g., "tech professionals", "startup founders", "marketing managers"
   - Tone: e.g., "professional", "conversational", "thought-provoking"
   - Additional Context: Call to Action, Industry, experience level, post objective

   Example prompt:
   ```
   Write an educational LinkedIn post about 'Context Engineering' for LLMs,
   using insights from this article: https://www.philschmid.de/context-engineering. 
   The post should: Start with a strong hook to grab attention. 
   Simply define Context Engineering and explain its benefits, 
   like improving accuracy and reducing costs compared to fine-tuning. 
   Briefly mention a key technique, such as Retrieval Augmented Generation (RAG). 
   Include a simple, practical example to illustrate the concept (e.g., a customer service bot). 
   End with a question to engage the audience and include relevant hashtags like #AI, #ContextEngineering, #LLM, and #RAG.

   Add a little bit of humor to the post as well, use few emojis too

   ```

3. Press enter and let him cook!🔥

*Note: More details in the prompt = Better output 😉, so add as much details in the prompt as possible*

## Configuration
Key configuration options in `.env`:
```
GOOGLE_API_KEY =       # Your Gemini API key
BRAVE_API_KEY =        # Your Brave Search API key
```

## Technologies Used
- **AI**
  - Gemini AI
  - Agno Framework

- **Web & Data**
  - Streamlit
  - Pydantic
  - Jina
  - Brave Search API

- **Development**
  - Python 3.11
  - uv (dependency management)
  - Environment variables

## Contributing
Feel free to submit issues and pull requests.

## License
MIT License - See LICENSE file