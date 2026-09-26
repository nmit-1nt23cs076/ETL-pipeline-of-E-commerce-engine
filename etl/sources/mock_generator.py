import random
from datetime import datetime, timedelta

def generate_mock_products():
    """
    Generates realistic e-commerce product listings across categories,
    with realistic specs, pricing history, stock statuses, and detailed customer reviews.
    """
    now = datetime.utcnow()
    
    # 1. LAPTOPS
    products = [
        {
            "id": "prod_lap_01",
            "sku": "SKU-MACBOOK-AIR-M3",
            "title": "Apple MacBook Air 13-inch M3 16GB RAM 512GB SSD Midnight",
            "brand": "Apple",
            "category": "laptops",
            "description": "Ultra-thin Apple M3 laptop with liquid retina display, silent fanless cooling, 18-hour battery life, and MagSafe 3 charging.",
            "url": "https://shopping.google.com/product/macbook-air-m3",
            "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500",
            "current_price": 1049.00,
            "original_price": 1299.00,
            "seller": "BestBuy",
            "is_in_stock": True,
            "stock_level": "In Stock",
            "rating": 4.8,
            "review_count": 342,
            "price_history_trend": [
                {"days_ago": 14, "price": 1299.00},
                {"days_ago": 7, "price": 1199.00},
                {"days_ago": 0, "price": 1049.00},
            ],
            "reviews": [
                {
                    "review_id": "rev_mac_1",
                    "author": "TechEnthusiast99",
                    "rating": 5.0,
                    "title": "Unbelievable battery life and speed!",
                    "content": "The M3 chip handles video editing and multi-tasking effortlessly. The midnight finish looks gorgeous and battery easily lasts 15+ hours of continuous coding.",
                    "date": now - timedelta(days=3)
                },
                {
                    "review_id": "rev_mac_2",
                    "author": "Sarah Jenkins",
                    "rating": 4.5,
                    "title": "Great lightweight laptop for work",
                    "content": "Super thin and silent. Keyboard feels great to type on. Only minor complaint is fingerprint smudges on the midnight color.",
                    "date": now - timedelta(days=6)
                }
            ]
        },
        {
            "id": "prod_lap_02",
            "sku": "SKU-DELL-XPS-15",
            "title": "Dell XPS 15 9530 15.6-inch 3.5K OLED Intel i7 32GB 1TB RTX 4060",
            "brand": "Dell",
            "category": "laptops",
            "description": "High performance creator laptop with 3.5K touch OLED display, CNC aluminum chassis, and NVIDIA GeForce RTX 4060 graphics.",
            "url": "https://shopping.google.com/product/dell-xps-15",
            "image_url": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=500",
            "current_price": 1499.00,
            "original_price": 1899.00,
            "seller": "Dell Direct",
            "is_in_stock": True,
            "stock_level": "Only 4 Left",
            "rating": 4.3,
            "review_count": 189,
            "price_history_trend": [
                {"days_ago": 14, "price": 1899.00},
                {"days_ago": 7, "price": 1699.00},
                {"days_ago": 0, "price": 1499.00},
            ],
            "reviews": [
                {
                    "review_id": "rev_dell_1",
                    "author": "Mark R.",
                    "rating": 4.0,
                    "title": "Stunning screen, but gets warm under load",
                    "content": "The OLED panel is breathtaking with deep blacks. However, the palm rests get uncomfortably warm during heavy 3D rendering or gaming sessions.",
                    "date": now - timedelta(days=2)
                },
                {
                    "review_id": "rev_dell_2",
                    "author": "Alex Dev",
                    "rating": 4.5,
                    "title": "Powerhouse laptop with steep discount",
                    "content": "32GB RAM makes Docker and IDEs run like a charm. Trackpad is huge and smooth.",
                    "date": now - timedelta(days=10)
                }
            ]
        },
        {
            "id": "prod_lap_03",
            "sku": "SKU-LENOVO-X1-CARBON",
            "title": "Lenovo ThinkPad X1 Carbon Gen 11 14-inch Intel i7 16GB 512GB",
            "brand": "Lenovo",
            "category": "laptops",
            "description": "Enterprise business ultrabook with ultralight carbon fiber chassis, ergonomic keyboard, TrackPoint, and privacy shutter.",
            "url": "https://shopping.google.com/product/thinkpad-x1-carbon",
            "image_url": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500",
            "current_price": 1299.00,
            "original_price": 1649.00,
            "seller": "Lenovo Store",
            "is_in_stock": True,
            "stock_level": "In Stock",
            "rating": 4.7,
            "review_count": 210,
            "price_history_trend": [
                {"days_ago": 14, "price": 1649.00},
                {"days_ago": 7, "price": 1499.00},
                {"days_ago": 0, "price": 1299.00},
            ],
            "reviews": [
                {
                    "review_id": "rev_len_1",
                    "author": "CorporateIT",
                    "rating": 5.0,
                    "title": "Best business keyboard on the market",
                    "content": "The typing tactile response is unmatched. Weighs practically nothing in a briefcase. Great Linux compatibility too.",
                    "date": now - timedelta(days=5)
                }
            ]
        },
        {
            "id": "prod_lap_04",
            "sku": "SKU-ACER-ASPIRE-5",
            "title": "Acer Aspire 5 Slim Laptop 15.6-inch Full HD Ryzen 5 8GB 512GB",
            "brand": "Acer",
            "category": "laptops",
            "description": "Budget-friendly everyday laptop with AMD Ryzen 5 processor, Wi-Fi 6, and narrow bezel display.",
            "url": "https://shopping.google.com/product/acer-aspire-5",
            "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500",
            "current_price": 349.00,
            "original_price": 449.00,
            "seller": "Amazon",
            "is_in_stock": True,
            "stock_level": "In Stock",
            "rating": 4.2,
            "review_count": 512,
            "price_history_trend": [
                {"days_ago": 14, "price": 449.00},
                {"days_ago": 7, "price": 389.00},
                {"days_ago": 0, "price": 349.00},
            ],
            "reviews": [
                {
                    "review_id": "rev_acer_1",
                    "author": "StudentSaver",
                    "rating": 4.5,
                    "title": "Unbeatable value budget laptop!",
                    "content": "For $349 this is amazing. Boots up in seconds, handles web browsing and homework fine. Plastic chassis feels cheap but performance is solid.",
                    "date": now - timedelta(days=4)
                }
            ]
        },

        # 2. SMARTPHONES
        {
            "id": "prod_phone_01",
            "sku": "SKU-SAMSUNG-S24-ULTRA",
            "title": "Samsung Galaxy S24 Ultra 5G 256GB Titanium Gray",
            "brand": "Samsung",
            "category": "smartphones",
            "description": "Flagship Galaxy smartphone featuring Snapdragon 8 Gen 3, built-in S Pen, 200MP AI camera with 100x zoom, and flat QHD+ 120Hz screen.",
            "url": "https://shopping.google.com/product/galaxy-s24-ultra",
            "image_url": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=500",
            "current_price": 1149.00,
            "original_price": 1299.00,
            "seller": "Samsung Store",
            "is_in_stock": True,
            "stock_level": "In Stock",
            "rating": 4.4,
            "review_count": 650,
            "price_history_trend": [
                {"days_ago": 14, "price": 1299.00},
                {"days_ago": 7, "price": 1249.00},
                {"days_ago": 0, "price": 1149.00},
            ],
            "reviews": [
                {
                    "review_id": "rev_sam_1",
                    "author": "David K.",
                    "rating": 3.5,
                    "title": "Battery life drainage complaint after latest update",
                    "content": "The screen and zoom cameras are incredible, but customers are complaining about Samsung battery life draining rapidly after the August software update. Used to get 1.5 days, now barely lasts until evening.",
                    "date": now - timedelta(days=1)
                },
                {
                    "review_id": "rev_sam_2",
                    "author": "TechGuru",
                    "rating": 4.0,
                    "title": "Bulky phone with high price tag",
                    "content": "Sharp corners dig into hands. Battery drain is noticeable during 4K video recording. S Pen features are great though.",
                    "date": now - timedelta(days=5)
                },
                {
                    "review_id": "rev_sam_3",
                    "author": "PhotoPro",
                    "rating": 5.0,
                    "title": "Best mobile camera system bar none",
                    "content": "200MP lens captures shocking detail. Night mode photography is top tier.",
                    "date": now - timedelta(days=8)
                }
            ]
        },
        {
            "id": "prod_phone_02",
            "sku": "SKU-SAMSUNG-A54-5G",
            "title": "Samsung Galaxy A54 5G 128GB Awesome Graphite",
            "brand": "Samsung",
            "category": "smartphones",
            "description": "Mid-range budget Galaxy phone with Super AMOLED 120Hz display, 50MP main camera with OIS, and 5000mAh battery.",
            "url": "https://shopping.google.com/product/galaxy-a54",
            "image_url": "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=500",
            "current_price": 349.00,
            "original_price": 449.00,
            "seller": "Amazon",
            "is_in_stock": True,
            "stock_level": "In Stock",
            "rating": 4.6,
            "review_count": 890,
            "price_history_trend": [
                {"days_ago": 14, "price": 449.00},
                {"days_ago": 7, "price": 399.00},
                {"days_ago": 0, "price": 349.00},
            ],
            "reviews": [
                {
                    "review_id": "rev_sam_a54_1",
                    "author": "BudgetShopper",
                    "rating": 4.8,
                    "title": "Best budget phone with great reviews!",
                    "content": "Amazing phone for under $350. Screen looks flagship quality, battery lasts 2 full days easily! Great reviews everywhere are accurate.",
                    "date": now - timedelta(days=2)
                },
                {
                    "review_id": "rev_sam_a54_2",
                    "author": "Elena M.",
                    "rating": 4.5,
                    "title": "Solid performance and clean software",
                    "content": "Good reviews on Samsung A54 are well deserved. Camera is clean in daytime. Plastic build is fine with a case.",
                    "date": now - timedelta(days=7)
                }
            ]
        },
        {
            "id": "prod_phone_03",
            "sku": "SKU-PIXEL-8A",
            "title": "Google Pixel 8a 128GB Obsidian Black",
            "brand": "Google",
            "category": "smartphones",
            "description": "AI-powered budget smartphone with Google Tensor G3 chip, 64MP camera with Best Take, Magic Eraser, and 7 years of updates.",
            "url": "https://shopping.google.com/product/pixel-8a",
            "image_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500",
            "current_price": 449.00,
            "original_price": 499.00,
            "seller": "Google Store",
            "is_in_stock": True,
            "stock_level": "In Stock",
            "rating": 4.7,
            "review_count": 420,
            "price_history_trend": [
                {"days_ago": 14, "price": 499.00},
                {"days_ago": 7, "price": 479.00},
                {"days_ago": 0, "price": 449.00},
            ],
            "reviews": [
                {
                    "review_id": "rev_pix_1",
                    "author": "AndroidFanatic",
                    "rating": 5.0,
                    "title": "Outstanding budget phone with glowing reviews",
                    "content": "Google Pixel 8a is the king of budget smartphones. AI photography features blow away phones twice the price. Highly recommended in all reviews.",
                    "date": now - timedelta(days=4)
                }
            ]
        },

        # 3. HEADPHONES & ACCESSORIES
        {
            "id": "prod_head_01",
            "sku": "SKU-SONY-XM5",
            "title": "Sony WH-1000XM5 Wireless Noise Canceling Headphones Black",
            "brand": "Sony",
            "category": "headphones",
            "description": "Premium over-ear wireless headphones with industry-leading noise canceling, dual processors, auto NC optimizer, and 30-hour battery life.",
            "url": "https://shopping.google.com/product/sony-xm5",
            "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500",
            "current_price": 328.00,
            "original_price": 399.00,
            "seller": "Sony Direct",
            "is_in_stock": True,
            "stock_level": "In Stock",
            "rating": 4.7,
            "review_count": 1250,
            "price_history_trend": [
                {"days_ago": 14, "price": 399.00},
                {"days_ago": 7, "price": 348.00},
                {"days_ago": 0, "price": 328.00},
            ],
            "reviews": [
                {
                    "review_id": "rev_sony_1",
                    "author": "AudioPhile",
                    "rating": 5.0,
                    "title": "Silence plane noise completely!",
                    "content": "Active Noise Cancellation is black magic. Extremely comfortable during 10 hour long flights.",
                    "date": now - timedelta(days=3)
                }
            ]
        },
        {
            "id": "prod_watch_01",
            "sku": "SKU-SAMSUNG-WATCH-6",
            "title": "Samsung Galaxy Watch 6 44mm Bluetooth Smartwatch Graphite",
            "brand": "Samsung",
            "category": "smartwatches",
            "description": "Smartwatch with sleep coaching, BIA body composition analysis, heart rate monitor, and sapphire crystal glass.",
            "url": "https://shopping.google.com/product/galaxy-watch-6",
            "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500",
            "current_price": 229.00,
            "original_price": 299.00,
            "seller": "BestBuy",
            "is_in_stock": False,
            "stock_level": "Out of Stock",
            "rating": 4.1,
            "review_count": 310,
            "price_history_trend": [
                {"days_ago": 14, "price": 299.00},
                {"days_ago": 7, "price": 259.00},
                {"days_ago": 0, "price": 229.00},
            ],
            "reviews": [
                {
                    "review_id": "rev_sam_w6_1",
                    "author": "RunnerGuy",
                    "rating": 3.8,
                    "title": "Nice watch, but Samsung battery life is poor",
                    "content": "Sleek screen and fitness tracking are accurate, but Samsung watch battery life requires daily charging. If you turn on Always-On Display it dies in 18 hours.",
                    "date": now - timedelta(days=2)
                }
            ]
        }
    ]
    
    return products
