from google.adk.tools.tool_context import ToolContext
from vertexai import rag
import re
from ..config import (
    DEFAULT_EMBEDDING_MODEL,
)

def create_corpus(corpus_name: str, tool_context:ToolContext) -> dict:
    """
    Create a text corpus file from a list of sentences.
    Args:
        corpus_name (str): The name of the corpus file to create.
        tool_context (ToolContext): The tool context for state management.
    Returns:
        dict: A dictionary containing the status and details of the corpus creation. 
    """
    try:
        # Sanitize corpus name for display
        display_name = re.sub(r"[^a-zA-Z0-9_-]", "_", corpus_name)

        # Configure embedding model
        embedding_model_config = rag.RagEmbeddingModelConfig(

            vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
                publisher_model=DEFAULT_EMBEDDING_MODEL
            )
        )

        # Create the corpus
        rag_corpus = rag.create_corpus(
            display_name=display_name,
            backend_config=rag.RagVectorDbConfig(
                rag_embedding_model_config=embedding_model_config
            ),
        )
        # Update state to track corpus existence
        tool_context.state[f"corpus_exists_{corpus_name}"] = True

        # Set this as the current corpus
        tool_context.state["current_corpus"] = corpus_name

        return {
            "status": "success",
            "message": f"Successfully created corpus '{corpus_name}'",
            "corpus_name": rag_corpus.name,
            "display_name": rag_corpus.display_name,
            "corpus_created": True,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error creating corpus: {str(e)}",
            "corpus_name": corpus_name,
            "corpus_created": False,
        }

