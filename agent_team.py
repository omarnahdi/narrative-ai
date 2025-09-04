import json
from agno.models.google import Gemini
from agno.agent import Agent
from dotenv import load_dotenv
from instructions import post_gen_instructions, team_instructions, prompt_tuner_goal, prompt_tuner_instructions, team_success_criteria, research_agent_instructions
# from agno.tools.bravesearch import BraveSearchTools
from fix_brave_tool import BraveSearchTools
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.models.groq import Groq
from agno.tools.crawl4ai import Crawl4aiTools
from agno.tools.agentql import AgentQLTools
import warnings
# from agno.tools.jina import JinaReaderTools
from fix_jina_tool import JinaReaderTools
from structured_models import PromptTunerResponse, ResearchFindings
from google.genai import types
from agno.team import Team
from agno.media import Image



safety_settings = [
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE),
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE),
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE),
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE),
    types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
                        threshold=types.HarmBlockThreshold.BLOCK_NONE),
]
warnings.filterwarnings("ignore", category=ResourceWarning)
load_dotenv()


db_file_team_storage = "tmp/team_storage.db"

db_file_team_mem = "tmp/team_memories.db"

storage = SqliteStorage(table_name="team_sessions", db_file=db_file_team_storage,mode='team',auto_upgrade_schema=True)

memory = Memory(
    # Use any model for creating memories
    model=Gemini(id='gemini-2.5-flash'),
    debug_mode=True,
    db=SqliteMemoryDb(table_name="team_memories", db_file=db_file_team_mem),
)

prompt_agent = Agent(
    name="Prompt Tuner Agent",
    role="Transforms the user's prompt into rich and well detailed instructions, with proper formatting",
    model=Gemini(id='gemini-2.5-flash',safety_settings=safety_settings,temperature=0.6),
    add_datetime_to_instructions=True,

    enable_agentic_memory=True,
    instructions=prompt_tuner_instructions,
    goal=prompt_tuner_goal,
    add_history_to_messages=True,
    num_history_runs=8,

    cache_session=True,
    markdown=True,
    response_model=PromptTunerResponse,
    parser_model=Gemini(id='gemini-2.5-flash-lite'),
    show_tool_calls=True,
    
)
researcher_agent = Agent(
    name="Researcher Agent",
    role="Researches the web for context rich content using search and scraping tools ",
    model=Gemini(id='gemini-2.5-flash',safety_settings=safety_settings,temperature=0.5),
    add_datetime_to_instructions=True,
   
    enable_agentic_memory=True,
    instructions=research_agent_instructions,
    # goal=goal,
    tools=[
        JinaReaderTools(include_tools=['robust_read_url'],cache_results=True), # Can use any one of the scrapin, by default uses Jina Reader API
        BraveSearchTools(fixed_max_results=5,cache_results=True),
    ],
    add_history_to_messages=True,
    cache_session=True,
    num_history_runs=8,
    show_tool_calls=True,
    markdown=True,
    response_model=ResearchFindings,
    parser_model=Gemini(id='gemini-2.5-flash'),
    tool_call_limit=8,
)

gemini_agent = Agent(
    name="Linkedin Post Generation Agent",
    role="Generates personalized content for user specific niche and targeted audience",
    model=Gemini(id='gemini-2.5-flash',safety_settings=safety_settings,temperature=0.6),
    add_datetime_to_instructions=True,
   
    enable_agentic_memory=True,
    instructions=post_gen_instructions,

    add_history_to_messages=True,
    cache_session=True,
    num_history_runs=8,
    show_tool_calls=True,
    
    markdown=True,
    
)

PostGenTeam = Team(
    model=Gemini('gemini-2.5-flash',safety_settings=safety_settings),
    description="A specialized team consisting of a prompt tuning expert and a research-focused agent that collaborates to generate high-quality content. The prompt agent optimizes content generation parameters while the Gemini agent gathers and synthesizes relevant information.",
    name="Narrative AI Team",
    success_criteria=team_success_criteria,
    instructions=team_instructions,
    debug_mode=True,
    add_history_to_messages=True,
    num_history_runs=8,
    # debug_level=2,
    members=[prompt_agent,researcher_agent,gemini_agent],
    mode="coordinate",
    enable_agentic_context=True,
    enable_agentic_memory=True,
    share_member_interactions=True,  # Share all member responses with subsequent member requests.
    show_members_responses=True,
    additional_context="Always return ready to post Linkedin content rather than conceptual details about the process.",
    cache_session=True,
    memory=memory,
    storage=storage,
    team_id="Narrative_AI_Team",
    # stream=False,
    
)

if __name__=="__main__":
    prompt = """
    
    Research the current state of AI in healthcare and write a post about breakthrough applications that are actually being deployed in 2025."
    
    """
    
    # researcher_agent.print_response(prompt)
    PostGenTeam.print_response(prompt)