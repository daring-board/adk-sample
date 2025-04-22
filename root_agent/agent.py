from google.adk.agents import Agent # type: ignore
from google.adk.models.lite_llm import LiteLlm # type: ignore
from google.adk.tools.base_tool import BaseTool # type: ignore
from google.adk.tools.tool_context import ToolContext # type: ignore
import dotenv
dotenv.load_dotenv()

from utils.tools import get_weather
from utils.constants import *
from utils.prompts import *
import farewell_agent
import greeting_agent

root_agent = None
runner_root = None # Initialize runner

if MODEL_PROVIDER == 'ollama':
    root_agent_model = LiteLlm(
        api_base=OPENAI_API_URL,
        model=f'openai/{MODEL_NAME}'
    )
else:
    root_agent_model = MODEL_NAME
root_agent = Agent(
    name="weather_agent_v2", # Give it a new version name
    model=root_agent_model,
    description=root_agent_description,
    instruction=root_agent_instruction,
    tools=[get_weather],
    sub_agents=[greeting_agent.agent.root_agent, farewell_agent.agent.root_agent],
    output_key="last_weather_report",
)