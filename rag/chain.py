import os
import logging
import config
from rag.router import SmartQueryRouter
from rag.sql_agent import SQLExecutor
from rag.vector_search import VectorSearchRetriever

logger = logging.getLogger(__name__)

class RAGPipeline:
    """
    Unified RAG Chain integrating Smart Router, SQLite Agent, ChromaDB Vector Search,
    and xAI Grok LLM (ChatXAI) to answer natural language questions about competitor prices & reviews.
    """

    def __init__(self, api_key: str = None, model_name: str = None):
        self.api_key = api_key or config.XAI_API_KEY or os.getenv("XAI_API_KEY", "")
        self.model_name = model_name or config.GROK_MODEL or "grok-4"
        self.router = SmartQueryRouter()
        self.sql_executor = SQLExecutor()
        self.vector_retriever = VectorSearchRetriever()
        self._llm = None

    def _get_llm(self):
        if self._llm is not None:
            return self._llm

        if self.api_key and self.api_key != "your_xai_api_key_here":
            try:
                from langchain_xai import ChatXAI
                self._llm = ChatXAI(
                    xai_api_key=self.api_key,
                    model=self.model_name,
                    temperature=0.2
                )
                return self._llm
            except Exception as e:
                logger.warning(f"Failed to initialize ChatXAI with provided key: {e}")
                return None
        return None

    def answer_query(self, user_query: str) -> dict:
        """
        Processes user query through Smart Router, retrieves context from SQL/Vector stores,
        and generates an insightful response using Grok LLM or structured synthesis.
        """
        # Step 1: Smart Route Classification
        routing_info = self.router.route_query(user_query)
        route = routing_info["route"]

        sql_context = []
        executed_sql = ""
        vector_reviews = []

        # Step 2: Context Retrieval based on Route
        if routing_info["requires_sql"]:
            sql_res = self.sql_executor.run_natural_language_sql_query(user_query)
            sql_context = sql_res.get("results", [])
            executed_sql = sql_res.get("executed_sql", "")

        if routing_info["requires_vector"]:
            # Extract brand if present in query
            brand_filter = None
            query_lower = user_query.lower()
            if "samsung" in query_lower:
                brand_filter = "Samsung"
            elif "apple" in query_lower or "macbook" in query_lower or "iphone" in query_lower:
                brand_filter = "Apple"
            elif "dell" in query_lower:
                brand_filter = "Dell"

            vector_reviews = self.vector_retriever.search_reviews(
                query=user_query,
                brand=brand_filter,
                top_k=5
            )

        # Step 3: LLM Response Generation
        llm = self._get_llm()
        if llm:
            try:
                system_prompt = (
                    "You are an expert E-Commerce Market Intelligence AI Assistant powered by xAI Grok. "
                    "Analyze the provided structured database facts and customer reviews to answer the user's question accurately. "
                    "Be concise, use bullet points, highlight price drops, savings, and specific customer feedback points."
                )

                user_prompt = f"User Question: {user_query}\n\n"
                if sql_context:
                    user_prompt += f"--- STRUCTURED SQL DATABASE FACTS ---\n{sql_context}\n\n"
                if vector_reviews:
                    user_prompt += f"--- CHROMADB CUSTOMER REVIEWS ---\n"
                    for r in vector_reviews:
                        user_prompt += f"- {r['content']} (Score: {r.get('similarity_score')})\n"
                    user_prompt += "\n"

                response = llm.invoke([
                    ("system", system_prompt),
                    ("user", user_prompt)
                ])

                answer_text = response.content if hasattr(response, 'content') else str(response)

            except Exception as e:
                logger.error(f"Grok LLM API call error: {e}")
                answer_text = self._fallback_synthesis(user_query, route, sql_context, vector_reviews)
        else:
            answer_text = self._fallback_synthesis(user_query, route, sql_context, vector_reviews)

        return {
            "query": user_query,
            "route": route,
            "route_reason": routing_info["reason"],
            "executed_sql": executed_sql,
            "sql_context": sql_context,
            "vector_reviews": vector_reviews,
            "answer": answer_text
        }

    def _fallback_synthesis(self, query: str, route: str, sql_context: list, vector_reviews: list) -> str:
        """
        Provides high-quality, formatted answer synthesis when LLM API key is not present or offline.
        """
        lines = []
        query_lower = query.lower()

        if "dropped" in query_lower or "price" in query_lower or route == "sql":
            lines.append("### 📊 E-Commerce Price Drop & Discount Summary")
            if sql_context:
                for item in sql_context:
                    disc = item.get("discount_percent", 0.0)
                    cur = item.get("current_price", 0.0)
                    orig = item.get("original_price", cur)
                    title = item.get("title", "Product")
                    brand = item.get("brand", "")
                    stock = item.get("stock_level", "In Stock")

                    if disc > 0:
                        lines.append(f"- **{title}** ({brand}): Price dropped to **${cur:,.2f}** (was **${orig:,.2f}**, **-{disc}% OFF**). Stock status: *{stock}*.")
                    else:
                        lines.append(f"- **{title}** ({brand}): Currently listed at **${cur:,.2f}**. Stock status: *{stock}*.")
            else:
                lines.append("No price drop products matching the specified query were found.")

        if "complain" in query_lower or "samsung" in query_lower or "battery" in query_lower or route in ("vector", "hybrid"):
            lines.append("\n### 🗣️ Customer Review Insights & Sentiment")
            if vector_reviews:
                for r in vector_reviews:
                    meta = r.get("metadata", {})
                    rating = meta.get("rating", "N/A")
                    label = meta.get("sentiment_label", "neutral").upper()
                    lines.append(f"- **[{label} - Rating: {rating}/5]** {r['content']}")
            elif sql_context and not vector_reviews:
                lines.append("Structured metadata retrieved successfully. (Tip: Embed reviews to view deep sentiment points).")
            else:
                lines.append("No customer reviews matching this semantic search were retrieved.")

        if not lines:
            lines.append(f"Retrieved {len(sql_context)} structured database rows and {len(vector_reviews)} vector reviews matching your query.")

        return "\n".join(lines)
