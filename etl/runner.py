import sys
import os
import logging

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import config
from etl.sources import fetch_serp_shopping_products, generate_mock_products
from etl.transform import transform_product_data
from etl.load import load_to_sqlite, load_to_chromadb

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("EcommerceETL")

def run_ecommerce_etl(use_mock=None, categories=None):
    """
    Executes the full ETL Pipeline:
    1. Extract: Scraping SerpAPI or Mock Data across categories
    2. Transform: Clean, normalize, discount calculation, sentiment scoring
    3. Load: Load into SQLite relational store & ChromaDB vector store
    """
    if use_mock is None:
        use_mock = config.USE_MOCK_DATA
        
    if categories is None:
        categories = ["laptops", "smartphones", "headphones"]
        
    logger.info("=== STARTING E-COMMERCE ETL PIPELINE ===")
    raw_all = []
    
    if use_mock or not config.SERPAPI_API_KEY:
        logger.info("Extracting data from Mock Generator...")
        raw_all = generate_mock_products()
    else:
        logger.info(f"Extracting live SerpAPI Google Shopping listings for categories: {categories}")
        for cat in categories:
            results = fetch_serp_shopping_products(query=cat, limit=10)
            raw_all.extend(results)
            
    logger.info(f"Extracted {len(raw_all)} raw items. Transforming and scoring data...")
    cleaned_products, price_histories, stock_statuses, reviews = transform_product_data(raw_all)
    
    logger.info("Loading transformed data to SQLite relational database...")
    load_to_sqlite(cleaned_products, price_histories, stock_statuses, reviews)
    
    logger.info("Embedding reviews and descriptions into ChromaDB vector store...")
    load_to_chromadb(cleaned_products, reviews)
    
    logger.info("=== ETL PIPELINE COMPLETED SUCCESSFULLY ===")
    return {
        "status": "success",
        "products_count": len(cleaned_products),
        "price_snapshots": len(price_histories),
        "reviews_count": len(reviews)
    }

if __name__ == "__main__":
    run_ecommerce_etl()
