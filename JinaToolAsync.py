# agno/tools/jina_reader_tools.py (FINAL AND CORRECTED - Following Stable Pattern)

from os import getenv
from typing import Any, Dict, List, Optional
import asyncio
import httpx
from pydantic import BaseModel, Field, HttpUrl
from agno.tools import Toolkit
from agno.utils.log import log_info, logger

class JinaReaderToolsConfig(BaseModel):
    api_key: Optional[str] = Field(None, description="API key for Jina Reader")
    base_url: HttpUrl = Field("https://r.jina.ai/", description="Base URL for Jina Reader API")
    search_url: HttpUrl = Field("https://s.jina.ai/", description="Search URL for Jina Reader API")
    max_content_length: int = Field(1000000, description="Maximum content length in characters")
    timeout: int = Field(20, description="Timeout for httpx client requests in seconds")

class JinaReaderTools(Toolkit):
    def __init__(
        self,
        # Custom parameters for OUR tool
        api_key: Optional[str] = getenv("JINA_API_KEY"),
        base_url: str = "https://r.jina.ai/",
        search_url: str = "https://s.jina.ai/",
        max_content_length: int = 1000000,
        timeout: int = 20,
        # Optional control over which tools to include
        include_tools: Optional[List[str]] = None,
        **kwargs,  # Capture any other arguments that might be passed
    ):
        # Handle OUR tool's specific configuration FIRST
        self.config: JinaReaderToolsConfig = JinaReaderToolsConfig(
            api_key=api_key,
            base_url=base_url,
            search_url=search_url,
            max_content_length=max_content_length,
            timeout=timeout,
        )
        
        # Set up our tools list
        tools: List[Any] = []
        all_tools = [self.robust_read_urls_async]
        
        # If specific tools are requested, filter to only those
        if include_tools:
            tools = [tool for tool in all_tools if tool.__name__ in include_tools]
        else:
            tools = all_tools
        
        # Call parent constructor with ONLY the standard arguments it expects
        # Following the exact pattern from the stable code
        super().__init__(name="jina_reader_tools", tools=tools, **kwargs)
        
        # Lazy-loading setup
        self.async_client: Optional[httpx.AsyncClient] = None

    async def _get_or_create_async_client(self) -> httpx.AsyncClient:
        """Lazily creates the httpx.AsyncClient on its first async use."""
        if self.async_client is None or self.async_client.is_closed:
            log_info("--- Lazily creating new httpx.AsyncClient instance ---")
            headers = self._get_headers()
            timeout = httpx.Timeout(self.config.timeout)
            self.async_client = httpx.AsyncClient(headers=headers, timeout=timeout)
        return self.async_client

    async def robust_read_urls_async(self, urls: List[str]) -> List[str]:
        """Reads a list of URLs concurrently using the lazily-initialized client."""
        client = await self._get_or_create_async_client()
        
        async def read_with_retry(url: str):
            delay = 2
            for attempt in range(2):
                try:
                    full_url = f"{self.config.base_url}{url}"
                    response = await client.get(full_url)
                    response.raise_for_status()
                    return self._truncate_content(str(response.json()))
                except (httpx.TimeoutException, httpx.RequestError) as e:
                    logger.warning(f"WARN: URL '{url}' attempt {attempt + 1}/2 failed: {e}")
                    if attempt < 1: await asyncio.sleep(delay)
                    else: return f"Error: Failed to retrieve content from '{url}'."
            return f"Error: An unexpected issue occurred for url '{url}'"

        tasks = [read_with_retry(url) for url in urls]
        return await asyncio.gather(*tasks)

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Accept": "application/json",
            "X-With-Links-Summary": "true",
            "X-With-Images-Summary": "true",
        }
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        headers["X-Timeout"] = str(self.config.timeout)
        return headers

    def _truncate_content(self, content: str) -> str:
        if len(content) > self.config.max_content_length:
            return content[:self.config.max_content_length] + "... (content truncated)"
        return content