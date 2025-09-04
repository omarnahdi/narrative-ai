from agno.playground import Playground
from agent_team import PostGenTeam

playground = Playground(teams=[PostGenTeam])

app = playground.get_app()

if __name__ == "__main__":
    playground.serve("playground:app", reload=True)