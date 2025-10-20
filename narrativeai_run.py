from agno.os import AgentOS
from agent_team import PostGenTeam
from fastapi.middleware.cors import CORSMiddleware

# Create AgentOS with teams
agno_os = AgentOS(
    teams=[PostGenTeam],
    description="Narrative AI Team AgentOS",
)

# Get the app and add CORS before serve() is called
app = agno_os.get_app()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://os.agno.com",
        "http://localhost:3000",
        "http://localhost:7777",
        "https://skinly-ashen.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    # Important: Pass the app object directly, not a string
    agno_os.serve(app="narrativeai_run:app", reload=True,host="0.0.0.0")
