from utils.constants import *
from utils.tools import say_hello
from utils.prompts import *
from google.adk.agents import Agent # type: ignore
from google.adk.models.lite_llm import LiteLlm  # type: ignore


if MODEL_PROVIDER == 'ollama':
    model = LiteLlm(
        api_base=OPENAI_API_URL,
        model=f'openai/{MODEL_NAME}'
    )
else:
    model = MODEL_NAME

# --- Greeting Agent ---
root_agent = Agent(
    model=model,
    name="greeting_agent",
    instruction=greeting_agent_instruction,
    description=greeting_agent_description, # Crucial for delegation
    tools=[say_hello],
)