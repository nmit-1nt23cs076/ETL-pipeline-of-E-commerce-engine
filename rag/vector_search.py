import logging
import chromadb
import config
from rag.embeddings import get_embedding_function

logger = logging.getLogger(__name__)

class VectorSearchRetriever:
    """
    Retriever for performing semantic search over e-commerce customer reviews and product descriptions in ChromaDB.
    """

    def __init__(self, vector_dir=None):
        self.vector_dir = vector_dir or config.VECTOR_STORE_DIR
        self.embedding_fn = get_embedding_function()
        self.client = chromadb.PersistentClient(path=self.vector_dir)

    def search_reviews(self, query: str, brand: str = None, category: str = None, top_k: int = 5) -> list[dict]:
        """
        Performs vector similarity search in ChromaDB with optional metadata filtering.
        """
        try:
            collection = self.client.get_collection(name=config.CHROMA_COLLECTION_NAME)
        except Exception as e:
            logger.warning(f"ChromaDB collection '{config.CHROMA_COLLECTION_NAME}' not found: {e}")
            return []

        query_embedding = self.embedding_fn.embed_query(query)

        where_clause = {}
        if brand:
            where_clause["brand"] = brand
        elif category:
            where_clause["category"] = category

        kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": top_k
        }
        if where_clause:
            kwargs["where"] = where_clause

        try:
            results = collection.query(**kwargs)
        except Exception as e:
            # Fallback without where filter if filter fails
            kwargs.pop("where", None)
            results = collection.query(**kwargs)

        retrieved = []
        if results and results.get("documents"):
            docs = results["documents"][0]
            metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
            distances = results["distances"][0] if results.get("distances") else [0.0] * len(docs)

            for doc, meta, dist in zip(docs, metas, distances):
                retrieved.append({
                    "content": doc,
                    "metadata": meta,
                    "similarity_score": round(1.0 - float(dist), 4) if dist is not None else 1.0
                })

        return retrieved
