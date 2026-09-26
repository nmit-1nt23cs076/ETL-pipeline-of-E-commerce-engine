from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(String(50), primary_key=True)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    brand = Column(String(100), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    url = Column(String(500), nullable=True)
    image_url = Column(String(500), nullable=True)
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    price_history = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan")
    stock_statuses = relationship("StockStatus", back_populates="product", cascade="all, delete-orphan")
    reviews = relationship("ProductReview", back_populates="product", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product(id='{self.id}', brand='{self.brand}', title='{self.title[:30]}')>"


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String(50), ForeignKey("products.id"), nullable=False, index=True)
    price = Column(Float, nullable=False)
    original_price = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    discount_percent = Column(Float, default=0.0)
    seller = Column(String(100), nullable=True)
    scraped_at = Column(DateTime, default=datetime.utcnow, index=True)

    product = relationship("Product", back_populates="price_history")

    def __repr__(self):
        return f"<PriceHistory(product_id='{self.product_id}', price={self.price}, discount={self.discount_percent}%)>"


class StockStatus(Base):
    __tablename__ = "stock_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String(50), ForeignKey("products.id"), nullable=False, index=True)
    is_in_stock = Column(Boolean, default=True)
    stock_level = Column(String(50), default="In Stock")
    seller = Column(String(100), nullable=True)
    scraped_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="stock_statuses")

    def __repr__(self):
        return f"<StockStatus(product_id='{self.product_id}', status='{self.stock_level}')>"


class ProductReview(Base):
    __tablename__ = "product_reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String(50), ForeignKey("products.id"), nullable=False, index=True)
    review_id = Column(String(100), unique=True, nullable=True)
    author = Column(String(100), default="Anonymous")
    rating = Column(Float, nullable=False)
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    sentiment_score = Column(Float, default=0.0)
    sentiment_label = Column(String(20), default="neutral")
    review_date = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="reviews")

    def __repr__(self):
        return f"<ProductReview(product_id='{self.product_id}', rating={self.rating}, sentiment='{self.sentiment_label}')>"
