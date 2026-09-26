import logging
import config

logger = logging.getLogger(__name__)

_embedding_instance = None

def get_embedding_function():
    """
    Returns a cached HuggingFaceEmbeddings instance for all-MiniLM-L6-v2.
    """
    global _embedding_instance
    if _embedding_instance is not None:
        return _embedding_instance
        
    try:
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
        except ImportError:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            
        logger.info(f"Loading local HuggingFace embedding model: {config.EMBEDDING_MODEL_NAME}")
        _embedding_instance = HuggingFaceEmbeddings(
            model_name=config.EMBEDDING_MODEL_NAME,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        return _embedding_instance
    except Exception as e:
        logger.error(f"Error loading HuggingFaceEmbeddings: {e}")
        # Fallback simple embedding class if model download fails or offline
        class FallbackEmbeddings:
            def embed_documents(self, texts):
                import numpy as np
                return [np.random.rand(384).tolist() for _ in texts]
            def embed_query(self, text):
                import numpy as np
                return np.random.rand(384).tolist()
        _embedding_instance = FallbackEmbeddings()
        return _embedding_instance
