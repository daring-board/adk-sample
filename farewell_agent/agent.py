from utils.constants import *
from utils.tools import say_goodbye
from utils.prompts import *
from google.adk.agents import Agent # type: ignore
from google.adk.models.lite_llm import LiteLlm # type: ignore # For multi-model support


if MODEL_PROVIDER == 'ollama':
    model = LiteLlm(
        api_base=OPENAI_API_URL,
        model=f'openai/{MODEL_NAME}'
    )
else:
    model = MODEL_NAME
# --- Farewell Agent ---
root_agent = Agent(
    # Can use the same or a different model
    model=model, # Sticking with GPT for this example
    name="farewell_agent",
    instruction=farewell_agent_instruction,
    description=farewell_agent_description,
    tools=[say_goodbye],
)