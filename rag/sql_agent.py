import sqlite3
import pandas as pd
import logging
import config

logger = logging.getLogger(__name__)

class SQLExecutor:
    """
    Executes structured queries against the SQLite e-commerce database.
    Provides targeted SQL execution for price drops, stock levels, product metadata, and custom SQL queries.
    """

    def __init__(self, db_path=None):
        self.db_path = db_path or config.SQLITE_DB_PATH

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def execute_custom_sql(self, sql_query: str, params=()) -> pd.DataFrame:
        """Executes a SELECT query and returns a pandas DataFrame."""
        try:
            with self.get_connection() as conn:
                df = pd.read_sql_query(sql_query, conn, params=params)
                return df
        except Exception as e:
            logger.error(f"SQL Execution Error: {e}")
            return pd.DataFrame()

    def query_price_drops(self, category=None, min_discount=5.0) -> list[dict]:
        """
        Finds products that have dropped in price, showing their latest price, original price, and discount %.
        """
        query = """
        SELECT 
            p.id, p.title, p.brand, p.category, 
            ph.price as current_price, ph.original_price, ph.discount_percent,
            ph.seller, ss.stock_level, ss.is_in_stock
        FROM products p
        JOIN price_history ph ON p.id = ph.product_id
        LEFT JOIN stock_status ss ON p.id = ss.product_id
        WHERE ph.id IN (
            SELECT MAX(id) FROM price_history GROUP BY product_id
        )
        AND ph.discount_percent >= ?
        """
        params = [min_discount]
        if category:
            query += " AND LOWER(p.category) = LOWER(?)"
            params.append(category)

        query += " ORDER BY ph.discount_percent DESC"

        df = self.execute_custom_sql(query, params)
        return df.to_dict(orient="records")

    def query_cheapest_products(self, category=None, limit=5) -> list[dict]:
        """
        Finds the cheapest products in a given category or overall.
        """
        query = """
        SELECT 
            p.id, p.title, p.brand, p.category, 
            ph.price as current_price, ph.original_price, ph.discount_percent,
            ss.stock_level, ss.is_in_stock
        FROM products p
        JOIN price_history ph ON p.id = ph.product_id
        LEFT JOIN stock_status ss ON p.id = ss.product_id
        WHERE ph.id IN (
            SELECT MAX(id) FROM price_history GROUP BY product_id
        )
        """
        params = []
        if category:
            query += " AND LOWER(p.category) LIKE ?"
            params.append(f"%{category.lower()}%")

        query += " ORDER BY ph.price ASC LIMIT ?"
        params.append(limit)

        df = self.execute_custom_sql(query, params)
        return df.to_dict(orient="records")

    def run_natural_language_sql_query(self, user_query: str) -> dict:
        """
        Translates intent into dynamic SQL execution and formats structured response context.
        """
        query_lower = user_query.lower()
        
        category = None
        for cat in ["laptop", "laptops", "phone", "phones", "smartphone", "smartphones", "headphone", "headphones", "watch", "smartwatches"]:
            if cat in query_lower:
                category = cat.replace("laptops", "laptop").replace("phones", "phone").replace("smartphones", "smartphone").replace("headphones", "headphone")
                break

        if "dropped" in query_lower or "discount" in query_lower or "deal" in query_lower:
            results = self.query_price_drops(category=category, min_discount=1.0)
            executed_sql = f"SELECT p.title, p.brand, ph.price, ph.original_price, ph.discount_percent FROM products p JOIN price_history ph... WHERE ph.discount_percent >= 1.0 ORDER BY discount_percent DESC"
        elif "cheap" in query_lower or "cheapest" in query_lower or "budget" in query_lower:
            results = self.query_cheapest_products(category=category, limit=6)
            executed_sql = f"SELECT p.title, p.brand, ph.price, ph.discount_percent FROM products p JOIN price_history ph... ORDER BY ph.price ASC LIMIT 6"
        else:
            # General product query with latest prices & stock
            query = """
            SELECT p.id, p.title, p.brand, p.category, ph.price as current_price, ph.original_price, ph.discount_percent, ss.stock_level
            FROM products p
            JOIN price_history ph ON p.id = ph.product_id
            LEFT JOIN stock_status ss ON p.id = ss.product_id
            WHERE ph.id IN (SELECT MAX(id) FROM price_history GROUP BY product_id)
            """
            params = []
            if category:
                query += " AND LOWER(p.category) LIKE ?"
                params.append(f"%{category}%")
            query += " ORDER BY p.rating DESC LIMIT 10"
            df = self.execute_custom_sql(query, params)
            results = df.to_dict(orient="records")
            executed_sql = query

        return {
            "results": results,
            "executed_sql": executed_sql,
            "count": len(results)
        }
