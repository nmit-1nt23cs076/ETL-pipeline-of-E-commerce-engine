import re
from datetime import datetime, timedelta

POSITIVE_WORDS = {
    "great", "excellent", "amazing", "unbelievable", "awesome", "stunning",
    "gorgeous", "best", "unmatched", "top", "outstanding", "solid", "glowing",
    "breathtaking", "fast", "love", "favorite", "superb", "perfect", "good"
}

NEGATIVE_WORDS = {
    "warm", "drain", "draining", "complaint", "complaining", "cheap", "smudge",
    "smudges", "poor", "dies", "bulky", "dig", "lag", "latency", "noise",
    "heating", "overheat", "worst", "slow", "bad", "creak", "creaking", "disappointed"
}

def analyze_sentiment(text: str) -> tuple[float, str]:
    """
    Computes a sentiment score between -1.0 and 1.0, and a label ('positive', 'neutral', 'negative').
    """
    if not text:
        return 0.0, "neutral"
        
    words = re.findall(r'\w+', text.lower())
    pos_count = sum(1 for w in words if w in POSITIVE_WORDS)
    neg_count = sum(1 for w in words if w in NEGATIVE_WORDS)
    
    total = pos_count + neg_count
    if total == 0:
        return 0.0, "neutral"
        
    score = (pos_count - neg_count) / total
    
    if score >= 0.2:
        label = "positive"
    elif score <= -0.2:
        label = "negative"
    else:
        label = "neutral"
        
    return round(score, 2), label


def transform_product_data(raw_products: list[dict]) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    """
    Cleans, normalizes, deduplicates product listings, calculates discount percentages,
    and extracts price history, stock status, and formatted reviews with sentiment scores.
    """
    seen_skus = set()
    cleaned_products = []
    price_histories = []
    stock_statuses = []
    all_reviews = []
    
    now = datetime.utcnow()
    
    for raw in raw_products:
        sku = raw.get("sku") or f"SKU-{raw.get('id')}"
        if sku in seen_skus:
            continue
        seen_skus.add(sku)
        
        cur_price = float(raw.get("current_price", 0.0))
        orig_price = float(raw.get("original_price", cur_price))
        if orig_price < cur_price:
            orig_price = cur_price
            
        discount_pct = 0.0
        if orig_price > 0:
            discount_pct = round(((orig_price - cur_price) / orig_price) * 100.0, 1)
            
        product_dict = {
            "id": str(raw.get("id")),
            "sku": sku,
            "title": str(raw.get("title", "")).strip(),
            "brand": str(raw.get("brand", "Generic")).strip(),
            "category": str(raw.get("category", "electronics")).lower().strip(),
            "description": str(raw.get("description", "")).strip(),
            "url": raw.get("url", ""),
            "image_url": raw.get("image_url", ""),
            "rating": float(raw.get("rating", 0.0)),
            "review_count": int(raw.get("review_count", 0)),
            "created_at": now
        }
        cleaned_products.append(product_dict)
        
        # Price History
        if "price_history_trend" in raw:
            for item in raw["price_history_trend"]:
                days_ago = item.get("days_ago", 0)
                item_price = float(item.get("price", cur_price))
                item_disc = round(((orig_price - item_price) / orig_price) * 100.0, 1) if orig_price > 0 else 0.0
                price_histories.append({
                    "product_id": product_dict["id"],
                    "price": item_price,
                    "original_price": orig_price,
                    "currency": "USD",
                    "discount_percent": max(0.0, item_disc),
                    "seller": raw.get("seller", "Retailer"),
                    "scraped_at": now - timedelta(days=days_ago)
                })
        else:
            price_histories.append({
                "product_id": product_dict["id"],
                "price": cur_price,
                "original_price": orig_price,
                "currency": "USD",
                "discount_percent": max(0.0, discount_pct),
                "seller": raw.get("seller", "Retailer"),
                "scraped_at": now
            })
            
        # Stock Status
        stock_statuses.append({
            "product_id": product_dict["id"],
            "is_in_stock": bool(raw.get("is_in_stock", True)),
            "stock_level": str(raw.get("stock_level", "In Stock")),
            "seller": raw.get("seller", "Retailer"),
            "scraped_at": now
        })
        
        # Reviews & Sentiment Analysis
        for rev in raw.get("reviews", []):
            content = str(rev.get("content", "")).strip()
            score, label = analyze_sentiment(content)
            rev_date = rev.get("date") or now
            
            all_reviews.append({
                "product_id": product_dict["id"],
                "review_id": rev.get("review_id") or f"rev_{product_dict['id']}_{len(all_reviews)}",
                "author": rev.get("author", "Anonymous"),
                "rating": float(rev.get("rating", 5.0)),
                "title": rev.get("title", ""),
                "content": content,
                "sentiment_score": score,
                "sentiment_label": label,
                "review_date": rev_date
            })
            
    return cleaned_products, price_histories, stock_statuses, all_reviews
