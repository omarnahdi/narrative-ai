from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class ResearchContext(BaseModel):
    """Comprehensive research data from a single source or iteration."""
    long_summary: str = Field(
        description="Detailed summary of the research findings and context"
    )
    scraped_content: List[str] = Field(
        description="Raw content collected from various sources"
    )
    key_points: List[str] = Field(
        description="Essential points extracted from the research"
    )
    sources: List[str] = Field(
        description="URLs of the sources used"
    )

class ResearchFindings(BaseModel):
    """Collection of research findings from multiple sources and iterations."""
    findings: List[ResearchContext] = Field(
        description="List of research contexts from different all sources and iterations"
    )

class PromptTunerResponse(BaseModel):
    """Expected output from the Prompt Tuner agent."""
    improved_and_detaild_prompt: str = Field(description="A well detailed and rich version of the prompt")
    reasoning: Optional[str] = None
    # suggestions: Optional[List[str]] = None
    


class LinkedInPostResponse(BaseModel):
    """Expected output from the LinkedIn Post Generator agent."""
    title: str
    body: str
    hashtags: Optional[List[str]] = None
    call_to_action: Optional[str] = None
    

class LinkedInPostResponseV2(BaseModel):
    """Expected output from the LinkedIn Post Generator agent."""
    post: str