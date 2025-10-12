import asyncio
import json
from agno.models.google import Gemini
from agno.agent import Agent
from instructions import post_gen_instructions, team_instructions, prompt_tuner_goal, prompt_tuner_instructions, team_success_criteria, research_agent_instructions
# from agno.tools.bravesearch import BraveSearchTools
from fix_brave_tool import BraveSearchTools

from agno.db.sqlite import SqliteDb
from agno.db.postgres import PostgresDb
from agno.memory import MemoryManager
import warnings
# from agno.tools.jina import JinaReaderTools
from JinaToolAsync import JinaReaderTools
from structured_models import PromptTunerResponse, ResearchFindings
from google.genai import types
from agno.team import Team
from dotenv import load_dotenv
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
import os
load_dotenv()


USE_NEONDB = os.getenv("USE_NEONDB")
if USE_NEONDB:
    NEONDB_URL = os.getenv("NEON_DB")
    db = PostgresDb(db_url=NEONDB_URL)
else: 
    db = SqliteDb(db_file='team_db/team_db.db')

memory_manager = MemoryManager(
        db=db,
        model=Gemini(id="gemini-2.0-flash"),
        debug_mode=True
    )


prompt_agent = Agent(
        name="Prompt Tuner Agent",
        role="Transforms the user's prompt into rich and well detailed instructions, with proper formatting",
        model=Gemini(id='gemini-2.5-flash',safety_settings=safety_settings,temperature=0.6),
        add_datetime_to_context=True,
        enable_agentic_memory=True,
        instructions=prompt_tuner_instructions,
        add_history_to_context=True,
        num_history_runs=8,
        db=db,
        memory_manager=memory_manager,
        cache_session=True,
        markdown=True,
        output_schema=PromptTunerResponse,
        parser_model=Gemini(id='gemini-2.5-flash-lite'),
        
    )
researcher_agent = Agent(
        name="Researcher Agent",
        role="Researches the web for context rich content using search and scraping tools ",
        model=Gemini(id='gemini-2.5-flash',safety_settings=safety_settings,temperature=0.6),
        add_datetime_to_context=True,
        db=db,
        memory_manager=memory_manager,
        enable_agentic_memory=True,
        instructions=research_agent_instructions,
        # goal=goal,
        tools=[
            JinaReaderTools(include_tools=['robust_read_urls_async'],cache_results=True), # Can use any one of the scrapin, by default uses Jina Reader API
            BraveSearchTools(fixed_max_results=10,cache_results=True),
        ],
        add_history_to_context=True,
        cache_session=True,
        num_history_runs=8,
        
        markdown=True,
        output_schema=ResearchFindings,
        parser_model=Gemini(id='gemini-2.5-flash-lite'),
        tool_call_limit=8,
    )

gemini_agent = Agent(
        name="Linkedin Post Generation Agent",
        role="Generates personalized content for user specific niche and targeted audience",
        model=Gemini(id='gemini-2.5-flash',safety_settings=safety_settings,temperature=0.6),
        add_datetime_to_context=True,
        db=db,
        memory_manager=memory_manager,
        enable_agentic_memory=True,
        instructions=post_gen_instructions,
        add_history_to_context=True,
        cache_session=True,
        num_history_runs=8,
        markdown=True,
        
    )
PostGenTeam = Team(
        # delegate_task_to_all_members=False,
        # respond_directly=True,
        model=Gemini('gemini-2.5-flash',safety_settings=safety_settings),
        description="A specialized team consisting of a prompt tuning expert and a research-focused agent that collaborates to generate high-quality content. The prompt agent optimizes content generation parameters while the Gemini agent gathers and synthesizes relevant information.",
        name="Narrative AI Team",
        db=db,
        memory_manager=memory_manager,
        instructions=team_instructions,
        debug_mode=True,
        add_history_to_context=True,
        num_history_runs=8,
        # debug_level=2,
        members=[prompt_agent,researcher_agent,gemini_agent],
        enable_agentic_memory=True,
        share_member_interactions=True,  # Share all member responses with subsequent member requests.
        show_members_responses=True,
        additional_context="Always return ready to post Linkedin content rather than conceptual details about the process.",
        cache_session=True,
        id="Narrative_AI_Team",
    )

# if __name__=="__main__":
#     prompt = """
#     Today I have a great and superb post idea.
#     ideas: Best CLI tools for vibe coders!
#     context: Vibe coders are growing and learning how to use chatgpt, gemini and claude but their UI makes slow progress and Windsurf
#     /Cursor are increasing their prices and restrictions day by day so recommend best CLI tools for AI Vibe Coding. Keep it cool and straight forward,
#     Grab the attentions of Vibe coders Quickly no confusion!
#     """
    
