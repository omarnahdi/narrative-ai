# v0.9.2

### What's New in v0.9.2
## Added Neon as a Databse provider
- Stores sessions and memory of Agents on NeonDB
- Set USE_NEONDB=True in .env to use NeonDB
- Defaults to local storage if USE_NEONDB is not set

## Added Supabase as a Database provider
- Stores sessions and memory of Agents on Supabase
- Set USE_SUPABASE=True in .env to use Supabase
- Defaults to local storage if USE_SUPABASE is not set

-----------------------------------------------------------------------------------------------------------------------------------------------
# v0.9.0

### What's New in v0.9.0 🎉
## Major Updates:

- 🚀 Agno v2.0.11 Integration: Complete migration from agno<2.0.0 to agno v2.0.11, leveraging the power of AgentOS with extended support. This update fundamentally changes how agents are defined and used in the project.
- 🔧 Fixed Brave Search API: Resolved issues with the Brave Search integration for more reliable web research.
- 🧹 Dependency Cleanup: Removed unwanted dependencies for a leaner installation (use uv sync to reflect changes).
- 📜 Commercial License Added: Introduced commercial licensing for organizational/commercial use while keeping the project completely free for individuals' personal and non-commercial use cases.
- ⚡ NEW Custom Async Jina Scraper: Implemented a more robust and faster async Jina scraper, replacing the old synchronous tool for improved performance.
- 📝 Enhanced System Standards: Updated context and instructions standards for better agent performance.
