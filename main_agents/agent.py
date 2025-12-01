from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk import Agent, Runner
from google.adk.tools import AgentTool, FunctionTool
from google.adk.sessions import InMemorySessionService
from .tools import rag_query
from .prompts import return_instructions_root
import os
import sys
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Agregar el directorio padre al path para importar utils

from utils.connection_db import DatabaseConnection

load_dotenv()

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
    ],)


APP_NAME = "agents"  # Application - debe coincidir con el directorio
USER_ID = "default"  # User
SESSION = "default"  # Session
MODEL_NAME = "gemini-2.5-flash"  # Model name for responses

# Define helper functions that will be reused throughout the notebook
async def run_session(
    runner_instance: Runner,
    user_queries: list[str] | str = None,
    session_name: str = "default",
):
    print(f"\n ### Session: {session_name}")

    # Get app name from the Runner
    app_name = runner_instance.app_name

    # Attempt to create a new session or retrieve an existing one
    try:
        session = await session_service.create_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )
    except:
        session = await session_service.get_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )

    # Process queries if provided
    if user_queries:
        # Convert single query to list for uniform processing
        if type(user_queries) == str:
            user_queries = [user_queries]

        # Process each query in the list sequentially
        for query in user_queries:
            print(f"\n🙍User > {query}")

            # Convert the query string to the ADK Content format
            query = types.Content(role="user", parts=[types.Part(text=query)])

            # Stream the agent's response asynchronously
            async for event in runner_instance.run_async(
                user_id=USER_ID, session_id=session.id, new_message=query
            ):
                # Check if the event contains valid content
                if event.content and event.content.parts:
                    # Filter out empty or "None" responses before printing
                    if (
                        event.content.parts[0].text != "None"
                        and event.content.parts[0].text
                    ):
                        print(f"🤖 {MODEL_NAME} > ", event.content.parts[0].text)
    else:
        print("No queries!")
    

# ================================================ Herramienta para análisis de base de datos
def analyze_database(query: str = ""):
    """
    Herramienta para conectarse y analizar la base de datos SQLite.
    
    Args:
        query: Descripción de lo que se quiere analizar (opcional)
    
    Returns:
        str: Información de las tablas y datos de la base de datos
    """
    db = DatabaseConnection()
    try:
        if not db.connect():
            return "Error: No se pudo conectar a la base de datos"
        
        # Obtener información general
        tables = db.get_tables()
        foreign_keys = db.get_foreign_keys()
        
        result = {
            "tables": tables,
            "foreign_keys": foreign_keys,
            "schemas": {}
        }
        
        # Obtener esquemas de todas las tablas
        for table in tables:
            schema = db.get_table_schema(table)
            sample_data = db.execute_query(f"SELECT * FROM {table} LIMIT 3")
            
            result["schemas"][table] = {
                "columns": [{"name": col[1], "type": col[2]} for col in schema],
                "sample_data": [dict(row) for row in sample_data]
            }
        
        return str(result)
        
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        db.disconnect()

# Crear la herramienta
database_analysis_tool = FunctionTool(func=analyze_database)

# Create Database_Analyst_Agent
database_analyst_agent = LlmAgent(
    name = 'Database_Analyst_Agent',
    description = 'An agent that specializes in analyze database structure and the data within it.',
    model='gemini-2.5-flash',
    instruction="""You are an expert database analyst. You will help the user to understand the database structure and the data within it.
    
    Usa la clase DatabaseConnection para conectarte a la base de datos SQLite:

    1. Conéctate a la base de datos usando el método `connect()`.
    2. Revisa la base de datos. Busca todas las tablas usando el método `get_tables()`.
    

    3. Revisa el esquema de la tabla que te interese usando el método `get_table_schema(table_name: str)`.
    4. Obtén todas las relaciones entre las tablas, para ello revisa las claves foráneas usando `get_foreign_keys()`.
    5. Analiza las relaciones de la tabla que te interesa en específico y devuelve un objeto json como e.g. 
        `{
            "relationships": [
                {
                "from": "sales_details.sale_id",
                "to": "sales.sale_id",
                "type": "many_to_one"
                },...
            ]
        }`.  


    6. Obten sample_data de las tablas que encontraste relaciones, para ello usa `execute_query(query: str, params: Optional[Tuple] = None)` para ejecutar consultas SELECT.
    Deberás limitar los resultados a un máximo de 5 filas por consulta. Devuelve el objeto json como e.g.
        `{
            "sample_data": {
                "books": [
                    {"book_id": 1, "title": "Book Title 1", "author": "Author 1", "published_year": 2020, "genre": "Fiction"},
                    {"book_id": 2, "title": "Book Title 2", "author": "Author 2", "published_year": 2019, "genre": "Non-Fiction"}
                ]
            }
        }`.


    7. Desconéctate de la base de datos usando el método `disconnect()` cuando hayas terminado. O si algo falla tambien debes desconectarte.
    Siempre responde en formato JSON.
    """,
    tools=[database_analysis_tool],
)

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction="""Answer user questions to the best of your knowledge

    Tienes esta documentación de un enpoint:

    api: /api/customer (get,post,patch)
    body request: {"id","name"} 
    description: api related to manage customer of the store
    tables: none

    Usa al Agent Database_Analyst_Agent para preguntar que tablas de la base de datos están relacionadas con la api /api/customer y obtener ejemplos de datos de esas tablas.
    """,
    tools=[AgentTool(database_analyst_agent)],
)

session_service = InMemorySessionService()

runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
print("Session service configured.")
print(f"   - Application: {APP_NAME}")
print(f"   - User: {USER_ID}")
print(f"   - Using: {session_service.__class__.__name__}")


async def main():
    """Función principal para ejecutar el agente"""
    
    print("\n🚀 Iniciando prueba del agente con InMemorySessionService...")
    
    # Consultas de prueba
    queries = [
        "Hi, I am Sam! What is the capital of the United States?", 
        "Hello! What is my name?",
        "What database tables are related to the /api/customer endpoint? Please analyze the database structure."
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*60}")
        print(f"📝 CONSULTA {i}: {query}")
        print('='*60)
        
        try:
            await run_session(runner, user_queries=query, session_name="stateful-agentic-session")
            print(f"✅ Consulta {i} completada.")
            
        
        except Exception as e:
            print(f"❌ Error en consulta {i}: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())