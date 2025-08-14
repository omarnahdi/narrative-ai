# Narrative AI: LinkedIn Post Generator with AI Agents 🤖

## Overview
An intelligent LinkedIn post generation system powered by AI agents, built to create engaging, research-backed professional content with a beautiful Agent UI interface.

## Table of Contents
- [Narrative AI: LinkedIn Post Generator with AI Agents 🤖](#narrative-ai-linkedin-post-generator-with-ai-agents-)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Project Structure](#project-structure)
  - [Usage](#usage)
  - [Configuration](#configuration)
  - [Technologies Used](#technologies-used)
  - [Contributing](#contributing)
  - [License](#license)
  - [Deprecated](#deprecated)
    - [Streamlit Interface (Deprecated)](#streamlit-interface-deprecated)

## Features
- 🎯 Research-backed content generation
- 🔍 Web scraping and data analysis
- 📝 Intelligent prompt engineering
- 🌐 Brave Search integration
- 📊 Structured output generation
- 🎨 Professional post formatting
- 🖥️ Beautiful Agent UI interface
- 💾 Conversation history and agent memory
- 🔄 Multi-agent interaction support

## Requirements

- Python 3.x
- Node.js 18+ (for Agent UI)
- Google AI API key (Gemini)
- Brave Search API key
- Required Python packages (defined in `pyproject.toml`)

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/omarnahdi/narrative-ai
cd narrative-ai
```

2. **Install Python dependencies**

**Recommended Method (using uv)**:

```bash
# Install uv if you haven't already
pip install uv

# Install dependencies using pyproject.toml (faster and more reliable)
uv sync

# Install and setup Playwright for web scraping
uv add playwright
playwright install
```

**Alternative Method (using pip)**:

```bash
# Install dependencies using requirements.txt
pip install -r requirements.txt

# Install and setup Playwright for web scraping
pip install playwright
playwright install
```

3. **Install Agno and additional dependencies**:

```bash
# Using uv (recommended)
uv add agno fastapi sqlalchemy

# Or using pip
pip install agno 'fastapi[standard]' sqlalchemy
```

4. **Create the Agent UI**:

```bash
# Create the Agent UI in a separate directory
npx create-agent-ui@latest
```
**NOTE:** for more info checkout [Ageno Agent UI](https://docs.agno.com/agent-ui/introduction#get-started-with-agent-ui)


5. **Setup environment variables**
```bash
# Create .env file from template
copy .example.env .env

# Add your API keys to .env
GOOGLE_API_KEY=your_gemini_api_key
BRAVE_API_KEY=your_brave_search_key
```

6. **Start the services**:

**Terminal 1 - Start the playground server:**
```bash
python playground.py
```

**Terminal 2 - Start the Agent UI:**
```bash
cd agent-ui
npm run dev
```

7. **Access the interface**:
- Open http://localhost:3000 
- Connect to the `localhost:7777` endpoint
- Start chatting with your LinkedIn Post Generator agent!

> **Note**: The `playground.py` file in this repository contains the pre-configured agent setup. Refer to this file for the specific agent configuration and any customizations needed for your use case.

## Project Structure
```plaintext
narrative-ai/
├── .venv/                  # Virtual environment
├── agent-ui/               # Agno Agent UI (locally generated, not in repo)
├── brave-api/              # Brave search API integration
├── tmp/                    # Agent storage directory (created after first run)
│   ├── team_storage.db     # Team agent storage database
│   └── team_memories.db    # Team agent memories database
├── .env                    # Environment variables
├── .example.env            # Environment variables template
├── .gitignore              # Git ignore rules
├── .python-version         # Python version specification
├── agent_team.py           # Main team agent implementation
├── fix_brave_tool.py       # Brave tool fixes/utilities
├── fix_jina_tool.py        # Jina tool fixes/utilities
├── instructions.py         # Agent instructions
├── LICENSE                 # License file
├── playground.py           # Agno playground server with agent configuration
├── post_gen_agent.py       # Individual post generation agent
├── post_gen_app.py         # Deprecated Streamlit application
├── post_gen_team_app.py    # Team-based post generation app
├── pyproject.toml          # Project dependencies and configuration
├── README.md               # This file
├── requirements.txt        # Python dependencies (alternative to pyproject.toml)
├── structured_models.py    # Pydantic data models
├── team_instructions.py    # Team-specific instructions
└── uv.lock                 # Lock file for dependencies
```

## Usage

1. **Start the playground server:**
```bash
python playground.py
```

2. **Start the Agent UI:**
```bash
cd agent-ui && npm run dev
```

3. **Open the UI and start chatting:**
   - Navigate to http://localhost:3000
   - Select the `localhost:7777` endpoint
   - Start chatting with your LinkedIn Post Generator agent!

4. **Available features:**
   - 💬 Natural conversation with your agent
   - 📊 View conversation history and agent memory
   - 🔄 Seamless multi-turn interactions
   - 🎨 Beautiful, responsive interface
   - 💾 Persistent chat sessions

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
  - Pydantic
  - Jina
  - Brave Search API

- **Agent UI**
  - Next.js
  - TypeScript
  - SQLite (for team memory)
  - FastAPI (playground server)

- **Development**
  - Python 3.11
  - Node.js 18+
  - uv (dependency management)
  - Environment variables

## Contributing
Feel free to submit issues and pull requests.

## License
Apache License - See LICENSE file

## Deprecated

### Streamlit Interface (Deprecated)
The original Streamlit interface (`post_gen_app.py`) has been deprecated in favor of the more feature-rich Agno Agent UI. The Streamlit version provided a chat-based interface but lacked conversation history, agent memory, and the enhanced user experience offered by the Agent UI.

If you need to use the deprecated Streamlit version for any reason, you can still run:
```bash
streamlit run post_gen_app.py
```

However, we strongly recommend migrating to the Agent UI for the best experience.