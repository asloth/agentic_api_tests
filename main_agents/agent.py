from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from .tools import rag_query
from .prompts import return_instructions_root

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

root_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name='rag_agent',
    instruction=return_instructions_root(),
    tools=[
        rag_query,
    ],
)
