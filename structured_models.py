from pydantic import BaseModel
from typing import Optional, List

class PromptTunerResponse(BaseModel):
    """Expected output from the Prompt Tuner agent."""
    improved_prompt: str
    reasoning: Optional[str] = None
    suggestions: Optional[List[str]] = None
    # agent_tools: List[str] = ['brave_search()','crawl()']


class LinkedInPostResponse(BaseModel):
    """Expected output from the LinkedIn Post Generator agent."""
    title: str
    body: str
    hashtags: Optional[List[str]] = None
    call_to_action: Optional[str] = None
    

class LinkedInPostResponseV2(BaseModel):
    """Expected output from the LinkedIn Post Generator agent."""
    post: str