from google.adk.agents.llm_agent import Agent
from google.adk.agents import LlmAgent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)



# Create Database_Analyst_Agent
database_analyst_agent = LlmAgent(
    name = 'Database_Analyst_Agent',
    description = 'An agent that specializes in analyze database structure and the data within it.',
    model='gemini-2.5-flash',
    intruction="""You are an expert database analyst. You will help the user to understand the database structure and the data within it.
    
    
    
    """,
)