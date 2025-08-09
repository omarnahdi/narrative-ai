import json
from agno.models.google import Gemini
from agno.agent import Agent
from dotenv import load_dotenv
from instructions import agent_instructions, goal, prompt_tuner_goal, prompt_tuner_instructions
# from agno.tools.bravesearch import BraveSearchTools
from fix_brave_tool import BraveSearchTools
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.workflow.v2 import Workflow, Step, StepOutput, StepInput
from agno.tools.crawl4ai import Crawl4aiTools
from agno.tools.agentql import AgentQLTools
import warnings
from agno.tools.jina import JinaReaderTools
from structured_models import PromptTunerResponse, LinkedInPostResponseV2
from google.genai import types
from agno.run.v2.workflow import WorkflowRunResponse
# Disable all adjustable filters
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

db_file = "tmp/agent.db"
db_workflow_file = "tmp/workflow.db"

storage = SqliteStorage(table_name="agent_sessions", db_file=db_file)
workflow_storage = SqliteStorage(table_name="workflow_sessions", db_file=db_workflow_file,mode='workflow_v2')

memory = Memory(
    # Use any model for creating memories
    model=Gemini(id='gemini-2.5-flash'),
    db=SqliteMemoryDb(table_name="user_memories", db_file=db_file),
)

prompt_agent = Agent(
    model=Gemini(id='gemini-2.5-flash',safety_settings=safety_settings,temperature=0.7),
    add_datetime_to_instructions=True,
    memory=memory,
    enable_agentic_memory=True,
    instructions=prompt_tuner_instructions,
    goal=prompt_tuner_goal,
    add_history_to_messages=True,
    num_history_runs=5,
    storage=storage,
    cache_session=True,
    markdown=True,
    response_model=PromptTunerResponse,
    parser_model=Gemini(id='gemini-2.5-flash-lite'),
    show_tool_calls=True,
    
)

gemini_agent = Agent(
    model=Gemini(id='gemini-2.5-pro',safety_settings=safety_settings,temperature=0.6),
    add_datetime_to_instructions=True,
    memory=memory,
    enable_agentic_memory=True,
    instructions=agent_instructions,
    # goal=goal,
    tools=[
        JinaReaderTools(), # Can use any one of the scrapin, by default uses Jina Reader API
        BraveSearchTools(),
        
        # Crawl4aiTools(max_length=None,include_tools=['crawl']),
        # AgentQLTools(include_tools=['scrape_website']),
    ],
    add_history_to_messages=True,
    num_history_runs=5,
    storage=storage,
    show_tool_calls=True,
    cache_session=True,
    markdown=True,

    
    # response_model=LinkedInPostResponseV2,
    # use_json_mode=True,
    tool_call_limit=12,
)

#

prompt_step = Step(
    agent=prompt_agent,
    description="A prompt tuner that helps refine and optimize prompts for better results.",
    name="Prompt Tuner",
)

post_step = Step(
    agent=gemini_agent,
    description="Generates a LinkedIn post based on the given prompt.",
    name="LinkedInPost Generator",
)

PostGenWorkflow = Workflow(
    name = "LinkedIn Post Generator",
    debug_mode=True,
    steps=[prompt_step, post_step],
    storage=workflow_storage,
    description="A workflow that generates a LinkedIn post based on a given prompt.",
)

input_prompt = """
Write an educational LinkedIn post about 'Context Engineering' for LLMs, using insights from this article: https://www.philschmid.de/context-engineering. The post should: Start with a strong hook to grab attention. Simply define Context Engineering and explain its benefits, like improving accuracy and reducing costs compared to fine-tuning. Briefly mention a key technique, such as Retrieval Augmented Generation (RAG). Include a simple, practical example to illustrate the concept (e.g., a customer service bot). End with a question to engage the audience and include relevant hashtags like #AI, #ContextEngineering, #LLM, and #RAG.

Add a little bit of humor to the post as well, use few emojis too

"""
if __name__ == "__main__":
    PostGenWorkflow.print_response(
        message=input_prompt,
        markdown=True
    )

# result: WorkflowRunResponse = PostGenWorkflow.run(input_prompt, markdown=True)
# print(result.content)