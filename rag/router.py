import re

class SmartQueryRouter:
    """
    Analyzes natural language user queries and routes them to SQL (structured database),
    Vector (ChromaDB review search), or Hybrid (both stores combined).
    """

    SQL_KEYWORDS = {
        "price", "prices", "dropped", "drop", "discount", "cheapest", "expensive",
        "cost", "costs", "dollar", "dollars", "$", "stock", "in stock", "out of stock",
        "history", "trend", "brand", "category", "how much", "under", "below", "cheaper", "budget"
    }

    VECTOR_KEYWORDS = {
        "review", "reviews", "complain", "complaining", "complaint", "complaints",
        "battery", "screen", "build", "quality", "opinion", "opinions", "customer",
        "customers", "saying", "hate", "love", "feel", "feedback", "rating", "heating",
        "sound", "issue", "issues", "problem", "problems", "experience"
    }

    def route_query(self, query: str) -> dict:
        """
        Classifies the query into 'sql', 'vector', or 'hybrid' along with confidence and explanation.
        """
        query_lower = query.lower()
        words = set(re.findall(r'\w+', query_lower))

        has_sql = bool(words & self.SQL_KEYWORDS) or "$" in query_lower or any(char.isdigit() for char in query_lower)
        has_vector = bool(words & self.VECTOR_KEYWORDS)

        # Explicit test pattern routing logic
        if has_sql and has_vector:
            route = "hybrid"
            reason = "Query combines structured criteria (price/budget/specs) with qualitative customer reviews (Requires SQLite + ChromaDB Hybrid search)."
        elif ("dropped" in query_lower or "cheapest" in query_lower or "price" in query_lower) and not has_vector:
            route = "sql"
            reason = "Query asks for price drops / structured numeric price data (Requires SQLite SQL query)."
        elif ("saying" in query_lower or "complain" in query_lower or "opinion" in query_lower or "hate" in query_lower or "battery" in query_lower or "review" in query_lower) and not has_sql:
            route = "vector"
            reason = "Query asks for qualitative customer feedback, opinions, or complaints (Requires ChromaDB Vector search)."
        elif has_sql:
            route = "sql"
            reason = "Query relates to structured attributes such as price, stock levels, or product specifications."
        elif has_vector:
            route = "vector"
            reason = "Query relates to semantic search over customer reviews, sentiment, and user experience."
        else:
            route = "hybrid"
            reason = "General query requiring comprehensive search across structured specifications and customer reviews."

        return {
            "route": route,
            "reason": reason,
            "requires_sql": route in ("sql", "hybrid"),
            "requires_vector": route in ("vector", "hybrid")
        }
