# Narrative AI: LinkedIn Post Generator with AI Agents 🤖

## What's New in v0.9.0 🎉

**Major Updates:**
- 🚀 **Agno v2.0.11 Integration**: Complete migration from agno<2.0.0 to agno v2.0.11, leveraging the power of AgentOS with extended support. This update fundamentally changes how agents are defined and used in the project.
- 🔧 **Fixed Brave Search API**: Resolved issues with the Brave Search integration for more reliable web research.
- 🧹 **Dependency Cleanup**: Removed unwanted dependencies for a leaner installation (use `uv sync` to reflect changes).
- 📜 **Commercial License Added**: Introduced commercial licensing for organizational/commercial use while keeping the project completely free for individuals' personal and non-commercial use cases.
- ⚡ **NEW Custom Async Jina Scraper**: Implemented a more robust and faster async Jina scraper, replacing the old synchronous tool for improved performance.
- 📝 **Enhanced System Standards**: Updated context and instructions standards for better agent performance.

## Overview
An intelligent LinkedIn post generation system powered by AI agents, built to create engaging, research-backed professional content with a beautiful Agent UI interface.

## Table of Contents
- [Narrative AI: LinkedIn Post Generator with AI Agents 🤖](#narrative-ai-linkedin-post-generator-with-ai-agents-)
  - [What's New in v0.9.0 🎉](#whats-new-in-v090-)
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

```

3. **Create the Agent UI**:

> **⚠️ IMPORTANT**: You MUST use the latest Agent UI for compatibility. The project will NOT work with older versions of the Agent UI.

**Automatic Installation (Recommended)**:

```bash
npx create-agent-ui@latest
```

**Manual Installation**:

1. Clone the repository:
```bash
git clone https://github.com/agno-agi/agent-ui.git
cd agent-ui
```

2. Install dependencies:
```bash
pnpm install
```

3. Start the development server:
```bash
pnpm dev
```

4. Open http://localhost:3000 with your browser to see the result.

**NOTE:** For more info checkout [Agno Agent UI](https://docs.agno.com/agent-ui/introduction#get-started-with-agent-ui)

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
├── brave-api/              # Brave search API integration
├── depreciated/            # Deprecated scripts
│   ├── post_gen_agent.py
│   ├── post_gen_app.py
│   └── post_gen_team_app.py
├── team_db/                # Database for agent teams
├── tmp/                    # Temporary file directory
├── .env                    # Environment variables
├── .example.env            # Environment variables template
├── .gitignore              # Git ignore rules
├── .python-version         # Python version specification
├── agent_team.py           # Main team agent implementation
├── fix_brave_tool.py       # Utility for Brave tool
├── fix_jina_tool.py        # Utility for Jina tool
├── hello.py                # Test/Example script
├── img_path_test.py        # Script for testing image paths
├── instructions.py         # Agent instructions
├── LICENSE                 # License file
├── narrativeai_run.py      # Main application runner
├── pyproject.toml          # Project configuration file
├── README.md               # Project README file
├── requirements.txt        # Python dependencies
├── structured_models.py    # Pydantic data models
└── uv.lock                 # Lock file for uv dependencies
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
  - Agno Framework v2.0.11

- **Web & Data**
  - Pydantic
  - Jina (Async Scraper)
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

**PolyForm Noncommercial License 1.0.0**

Copyright © Omar Nahdi (omarnahdi.ai@gmail.com)

This project is licensed under the PolyForm Noncommercial License 1.0.0.

**Key License Terms:**

✅ **FREE for Individuals**: This software is completely free for individuals to use for personal, non-commercial purposes including:
- Personal study and learning
- Hobby projects
- Research and experimentation
- Private entertainment
- Amateur pursuits

❌ **Commercial License Required**: Any use by organizations of any kind requires a separate commercial license. This includes:
- Corporations and businesses
- Non-profit organizations
- Educational institutions
- Government agencies
- Startups and partnerships
- Any organizational or commercial use

**Commercial Licensing:**
For commercial licensing inquiries, please contact: **omarnahdi.ai@gmail.com**

For full license terms, see the [LICENSE](LICENSE) file.

---

**Important**: This license explicitly prohibits any commercial entity from using this project/software without obtaining a commercial license. Individual users may use this project freely for personal and non-commercial purposes only.

## Deprecated

### Streamlit Interface (Deprecated)
The original Streamlit interface (`post_gen_app.py`) has been deprecated in favor of the more feature-rich Agno Agent UI. The Streamlit version provided a chat-based interface but lacked conversation history, agent memory, and the enhanced user experience offered by the Agent UI.

If you need to use the deprecated Streamlit version for any reason, you can still run:
```bash
streamlit run post_gen_app.py
```

However, we strongly recommend migrating to the Agent UI for the best experience.