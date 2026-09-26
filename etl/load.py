import logging
import chromadb
from chromadb.config import Settings
from sqlalchemy.orm import Session
import config
from db.database import init_db, SessionLocal
from db.models import Product, PriceHistory, StockStatus, ProductReview
from rag.embeddings import get_embedding_function

logger = logging.getLogger(__name__)

def load_to_sqlite(products: list[dict], price_histories: list[dict], stock_statuses: list[dict], reviews: list[dict]):
    """
    Upserts products and records new price history snapshots, stock levels, and product reviews in SQLite.
    """
    init_db()
    session: Session = SessionLocal()
    
    try:
        # 1. Upsert Products
        for prod in products:
            existing = session.query(Product).filter(Product.id == prod["id"]).first()
            if existing:
                existing.title = prod["title"]
                existing.brand = prod["brand"]
                existing.category = prod["category"]
                existing.description = prod["description"]
                existing.url = prod["url"]
                existing.image_url = prod["image_url"]
                existing.rating = prod["rating"]
                existing.review_count = prod["review_count"]
            else:
                db_product = Product(**prod)
                session.add(db_product)
        session.commit()
        
        # 2. Insert Price History Snapshots
        for ph in price_histories:
            db_ph = PriceHistory(**ph)
            session.add(db_ph)
            
        # 3. Insert Stock Statuses
        for ss in stock_statuses:
            db_ss = StockStatus(**ss)
            session.add(db_ss)
            
        # 4. Upsert Product Reviews
        for rev in reviews:
            existing_rev = session.query(ProductReview).filter(ProductReview.review_id == rev["review_id"]).first()
            if not existing_rev:
                db_rev = ProductReview(**rev)
                session.add(db_rev)
                
        session.commit()
        logger.info(f"SQLite Load Complete: {len(products)} products, {len(price_histories)} price snapshots, {len(reviews)} reviews.")
        
    except Exception as e:
        session.rollback()
        logger.error(f"Failed loading data to SQLite: {e}")
        raise e
    finally:
        session.close()


def load_to_chromadb(products: list[dict], reviews: list[dict]):
    """
    Embeds reviews and product descriptions into ChromaDB vector store.
    """
    client = chromadb.PersistentClient(path=config.VECTOR_STORE_DIR)
    
    # Get or create collection
    collection = client.get_or_create_collection(
        name=config.CHROMA_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )
    
    embedding_fn = get_embedding_function()
    
    documents = []
    metadatas = []
    ids = []
    
    # 1. Add Product Descriptions for Semantic Product Search
    for prod in products:
        doc_id = f"doc_prod_{prod['id']}"
        text_content = f"Product: {prod['title']}. Brand: {prod['brand']}. Category: {prod['category']}. Description: {prod['description']}"
        
        documents.append(text_content)
        metadatas.append({
            "type": "product_description",
            "product_id": prod["id"],
            "brand": prod["brand"],
            "category": prod["category"],
            "title": prod["title"],
            "rating": float(prod["rating"])
        })
        ids.append(doc_id)
        
    # 2. Add Customer Reviews
    prod_map = {p["id"]: p for p in products}
    for rev in reviews:
        doc_id = f"doc_rev_{rev['review_id']}"
        prod_info = prod_map.get(rev["product_id"], {})
        brand = prod_info.get("brand", "Unknown")
        category = prod_info.get("category", "General")
        prod_title = prod_info.get("title", "")
        
        text_content = f"Customer Review for {brand} {prod_title} (Rating: {rev['rating']}/5.0):\nTitle: {rev['title']}\nReview: {rev['content']}"
        
        documents.append(text_content)
        metadatas.append({
            "type": "review",
            "product_id": rev["product_id"],
            "review_id": rev["review_id"],
            "brand": brand,
            "category": category,
            "rating": float(rev["rating"]),
            "sentiment_score": float(rev["sentiment_score"]),
            "sentiment_label": str(rev["sentiment_label"])
        })
        ids.append(doc_id)
        
    if documents:
        embeddings = embedding_fn.embed_documents(documents)
        collection.upsert(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"ChromaDB Load Complete: Embedded {len(documents)} documents into collection '{config.CHROMA_COLLECTION_NAME}'.")
