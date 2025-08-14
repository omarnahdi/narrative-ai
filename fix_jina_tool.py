# agno/tools/jina_reader_tools.py (REFACTORED AND PRODUCTION-READY)

from os import getenv
from typing import Any, Dict, List, Optional
import time  # <--- CHANGE 1: Import the time library for handling delays

import httpx
from pydantic import BaseModel, Field, HttpUrl

from agno.tools import Toolkit
from agno.utils.log import log_info, logger


class JinaReaderToolsConfig(BaseModel):
    api_key: Optional[str] = Field(None, description="API key for Jina Reader")
    base_url: HttpUrl = Field("https://r.jina.ai/", description="Base URL for Jina Reader API")  # type: ignore
    search_url: HttpUrl = Field("https://s.jina.ai/", description="Search URL for Jina Reader API")  # type: ignore
    max_content_length: int = Field(1000000, description="Maximum content length in characters")
    # <--- CHANGE 2: Set a sensible client-side timeout in seconds (e.g., 30s)
    timeout: int = Field(30, description="Timeout for individual httpx client requests in seconds")


class JinaReaderTools(Toolkit):
    def __init__(
        self,
        api_key: Optional[str] = getenv("JINA_API_KEY"),
        base_url: str = "https://r.jina.ai/",
        search_url: str = "https://s.jina.ai/",
        max_content_length: int = 1000000,
        timeout: int = 60, # <--- CHANGE 3: Updated default timeout
        read_url: bool = True,
        search_query: bool = True, # Assuming you want search to be robust too
        **kwargs,
    ):
        self.config: JinaReaderToolsConfig = JinaReaderToolsConfig(
            api_key=api_key,
            base_url=base_url,
            search_url=search_url,
            max_content_length=max_content_length,
            timeout=timeout,
        )

        tools: List[Any] = []
        if read_url:
            # <--- CHANGE 4: Expose the robust wrapper to the agent, not the raw tool
            tools.append(self.robust_read_url)
        if search_query:
            tools.append(self.robust_search_query)

        super().__init__(name="jina_reader_tools", tools=tools, **kwargs)

    def _read_url_once(self, url: str) -> str:
        """Internal function to attempt reading a URL one time. Raises exceptions on failure."""
        full_url = f"{self.config.base_url}{url}"
        log_info(f"Attempting to read URL: {full_url}")
        
        # <--- CHANGE 5: Apply the timeout directly to the httpx client call
        response = httpx.get(
            full_url,
            headers=self._get_headers(),
            timeout=self.config.timeout
        )
        response.raise_for_status()  # Will raise an exception for 4xx/5xx errors
        content = response.json()
        return self._truncate_content(str(content))

    def robust_read_url(self, url: str, ) -> str:
        """
        A robust wrapper for reading a URL that includes retries with exponential backoff.
        This function handles transient network errors and timeouts gracefully.
        It is the function that should be exposed to the agent as a tool.
        """
        max_retries: int = 5
        initial_delay: int = 3
        
        delay = initial_delay
        for attempt in range(max_retries):
            try:
                return self._read_url_once(url)
            # <--- CHANGE 6: Catch specific, meaningful exceptions for better logging
            except httpx.TimeoutException:
                logger.warning(f"WARN: Attempt {attempt + 1}/{max_retries} to read '{url}' timed out.")
            except httpx.RequestError as e:
                logger.warning(f"WARN: Attempt {attempt + 1}/{max_retries} for '{url}' failed with a network error: {e}")
            
            if attempt < max_retries - 1:
                logger.info(f"Waiting for {delay} seconds before retrying...")
                time.sleep(delay)
                delay *= 2  # Double the delay for the next attempt
            else:
                # <--- CHANGE 7: After all retries, return a structured error message for the agent
                final_error_message = f"Error: Tool 'read_url' failed to retrieve content from '{url}' after {max_retries} attempts."
                logger.error(final_error_message)
                return final_error_message

    def _search_query_once(self, query: str) -> str:
        """Internal function to attempt a search query one time. Raises exceptions on failure."""
        full_url = f"{self.config.search_url}{query}"
        log_info(f"Attempting search: {full_url}")
        
        response = httpx.get(
            full_url,
            headers=self._get_headers(),
            timeout=self.config.timeout
        )
        response.raise_for_status()
        content = response.json()
        return self._truncate_content(str(content))

    def robust_search_query(self, query: str, max_retries: int = 2, initial_delay: int = 3) -> str:
        """A robust wrapper for web search that includes retries with exponential backoff."""
        delay = initial_delay
        for attempt in range(max_retries):
            try:
                return self._search_query_once(query)
            except httpx.TimeoutException:
                logger.warning(f"WARN: Attempt {attempt + 1}/{max_retries} for search query '{query}' timed out.")
            except httpx.RequestError as e:
                logger.warning(f"WARN: Attempt {attempt + 1}/{max_retries} for search query '{query}' failed with a network error: {e}")
            
            if attempt < max_retries - 1:
                logger.info(f"Waiting for {delay} seconds before retrying...")
                time.sleep(delay)
                delay *= 2
            else:
                final_error_message = f"Error: Tool 'search_query' failed to get results for '{query}' after {max_retries} attempts."
                logger.error(final_error_message)
                return final_error_message

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Accept": "application/json",
            "X-With-Links-Summary": "true",
            "X-With-Images-Summary": "true",
        }
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        # The X-Timeout header is still useful to tell the Jina server how long IT should wait
        headers["X-Timeout"] = str(self.config.timeout)
        return headers

    def _truncate_content(self, content: str) -> str:
        """Truncate content to the maximum allowed length."""
        if len(content) > self.config.max_content_length:
            truncated = content[:self.config.max_content_length]
            return truncated + "... (content truncated)"
        return content