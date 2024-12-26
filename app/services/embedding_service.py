from openai import OpenAI
import os
import logging
from sqlalchemy.orm import Session
from .database_service import get_model_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def process_embedding(db: Session, text: str, model_name: str = "text-embedding-3-small"):
    """
    Process text to get embeddings using specified model
    
    Args:
        db (Session): Database session
        text (str): Text to be embedded
        model_name (str): Model name for embeddings, defaults to text-embedding-3-small
    """
    try:
        # Get model configuration
        model_config = get_model_config(db, model_name)
        if not model_config:
            raise ValueError(f"Model {model_name} not found or inactive")
        
        # Initialize OpenAI client with config
        client = OpenAI(
            api_key=model_config.api_key,
            base_url=model_config.base_url if model_config.base_url else None
        )
        
        # Get embeddings
        response = client.embeddings.create(
            input=text,
            model=model_name
        )
        
        return {
            "success": True,
            "embedding": response.data[0].embedding,
            "model": model_name
        }
        
    except Exception as e:
        logger.error(f"Error in process_embedding: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
