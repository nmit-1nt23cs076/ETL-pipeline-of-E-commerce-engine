import os
import sys
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="E-Commerce ETL & RAG Competitor Intelligence",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure project modules are importable
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import config
from db.database import init_db, SessionLocal
from db.models import Product, PriceHistory, StockStatus, ProductReview
from etl.runner import run_ecommerce_etl
from rag.chain import RAGPipeline
from rag.sql_agent import SQLExecutor

# Custom CSS for rich dark glassmorphism styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #9CA3AF;
        font-size: 1.0rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-title {
        color: #94A3B8;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-top: 0.2rem;
    }
    .badge-sql {
        background-color: #1E3A8A;
        color: #60A5FA;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #2563EB;
    }
    .badge-vector {
        background-color: #4C1D95;
        color: #C084FC;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #7C3AED;
    }
    .badge-hybrid {
        background-color: #064E3B;
        color: #34D399;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid #059669;
    }
</style>
""", unsafe_allow_html=True)

# Ensure Database & Default Data Exist on Startup
init_db()
session = SessionLocal()
product_count = session.query(Product).count()
session.close()

if product_count == 0:
    with st.spinner("Initializing Database with initial e-commerce tracking data..."):
        run_ecommerce_etl(use_mock=True)

# SIDEBAR CONFIGURATION
st.sidebar.image("https://img.icons8.com/isometric/100/shopping-cart.png", width=64)
st.sidebar.title("🛒 Control Panel")

st.sidebar.subheader("🔑 API Key Setup")
xai_key_input = st.sidebar.text_input("xAI Grok API Key", value=config.XAI_API_KEY, type="password", help="xAI API key from console.x.ai for Grok LLM")
serp_key_input = st.sidebar.text_input("SerpAPI Key (Optional)", value=config.SERPAPI_API_KEY, type="password", help="SerpAPI key from serpapi.com for real Google Shopping scraping")

grok_model = st.sidebar.selectbox("Grok Model Version", options=["grok-4", "grok-3", "grok-2-1212"], index=0)

data_mode = st.sidebar.radio("Data Source Mode", ["Mock Data Generator (Testing)", "Live SerpAPI Google Shopping"], index=0 if config.USE_MOCK_DATA else 1)
use_mock_flag = (data_mode == "Mock Data Generator (Testing)")

if st.sidebar.button("🚀 Run ETL Pipeline Now", type="primary"):
    with st.spinner("Executing 6-stage ETL pipeline..."):
        res = run_ecommerce_etl(use_mock=use_mock_flag)
        st.sidebar.success(f"ETL Complete! {res['products_count']} products updated.")
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("💡 **Dual Storage Architecture:**\n- **SQLite:** Structured prices, discounts, stock\n- **ChromaDB:** Unstructured customer reviews & sentiment")

# MAIN APP BODY
st.markdown("<div class='main-header'>E-Commerce Price & Review RAG Pipeline</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Real-Time Competitor Price Tracking, Review Sentiment Analysis & Smart Dual-Store RAG Q&A</div>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💬 Natural Language Q&A Chat", "📊 Competitor Price & Sentiment Dashboard", "⚙️ Airflow DAG & Database Inspector"])

# ---------------------------------------------------------
# TAB 1: NATURAL LANGUAGE RAG CHAT
# ---------------------------------------------------------
with tab1:
    st.markdown("### 🤖 Ask Natural Language Questions")
    st.write("Click any sample query or enter your own question below:")

    # Quick prompt buttons
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    q_clicked = None
    with col_p1:
        if st.button("💻 Laptop Price Drops"):
            q_clicked = "Which laptops dropped price this week?"
    with col_p2:
        if st.button("🗣️ Samsung Review Complaints"):
            q_clicked = "What are customers complaining about in Samsung reviews?"
    with col_p3:
        if st.button("📱 Budget Phones Reviews"):
            q_clicked = "Which budget phones have good reviews?"
    with col_p4:
        if st.button("🔋 Battery Life Opinions"):
            q_clicked = "What are people saying about Samsung battery life?"

    user_prompt = st.text_input("Enter your question:", value=q_clicked if q_clicked else "", placeholder="e.g. Which laptops are cheapest right now?")

    if user_prompt:
        rag = RAGPipeline(api_key=xai_key_input, model_name=grok_model)
        with st.spinner("Smart Router analyzing query & retrieving context..."):
            result = rag.answer_query(user_prompt)

        route = result["route"]
        route_reason = result["route_reason"]

        st.markdown("#### 🎯 Smart Router Decision")
        if route == "sql":
            st.markdown(f"<span class='badge-sql'>🔵 SQL ROUTE (Structured SQLite Database)</span> &nbsp; <small>{route_reason}</small>", unsafe_allow_html=True)
        elif route == "vector":
            st.markdown(f"<span class='badge-vector'>🟣 VECTOR ROUTE (ChromaDB Reviews Store)</span> &nbsp; <small>{route_reason}</small>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span class='badge-hybrid'>🟢 HYBRID ROUTE (SQLite + ChromaDB Combined)</span> &nbsp; <small>{route_reason}</small>", unsafe_allow_html=True)

        # Expander showing retrieved evidence
        with st.expander("🔍 View Retrieved Query Execution & Data Evidence"):
            if result.get("executed_sql"):
                st.markdown("**Executed SQL Query:**")
                st.code(result["executed_sql"], language="sql")
                if result.get("sql_context"):
                    st.markdown("**Structured SQL Database Rows:**")
                    st.dataframe(pd.DataFrame(result["sql_context"]))

            if result.get("vector_reviews"):
                st.markdown("**Top ChromaDB Semantic Vector Matches:**")
                for r in result["vector_reviews"]:
                    st.json(r)

        # Final Answer Box
        st.markdown("### 💡 Grok LLM Answer")
        st.info(result["answer"])

# ---------------------------------------------------------
# TAB 2: COMPETITOR PRICE & SENTIMENT DASHBOARD
# ---------------------------------------------------------
with tab2:
    st.markdown("### 📊 Market Intelligence & Competitor Analytics")
    session = SessionLocal()
    products = session.query(Product).all()
    price_histories = session.query(PriceHistory).all()
    stock_statuses = session.query(StockStatus).all()
    reviews = session.query(ProductReview).all()
    session.close()

    if products:
        df_prod = pd.DataFrame([{
            "id": p.id, "title": p.title, "brand": p.brand, "category": p.category, "rating": p.rating, "created_at": p.created_at
        } for p in products])

        df_price = pd.DataFrame([{
            "product_id": ph.product_id, "price": ph.price, "original_price": ph.original_price,
            "discount_percent": ph.discount_percent, "seller": ph.seller, "scraped_at": ph.scraped_at
        } for ph in price_histories])

        df_stock = pd.DataFrame([{
            "product_id": ss.product_id, "is_in_stock": ss.is_in_stock, "stock_level": ss.stock_level
        } for ss in stock_statuses])

        df_merged = df_prod.merge(df_price, left_on="id", right_on="product_id", how="inner")
        df_latest = df_merged.sort_values("scraped_at").groupby("id").last().reset_index()

        # Key Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"<div class='metric-card'><div class='metric-title'>Products Tracked</div><div class='metric-value'>{len(df_prod)}</div></div>", unsafe_allow_html=True)
        with m2:
            avg_disc = df_latest['discount_percent'].mean() if not df_latest.empty else 0.0
            st.markdown(f"<div class='metric-card'><div class='metric-title'>Avg Discount</div><div class='metric-value'>{avg_disc:.1f}%</div></div>", unsafe_allow_html=True)
        with m3:
            out_stock = sum(1 for s in stock_statuses if not s.is_in_stock)
            st.markdown(f"<div class='metric-card'><div class='metric-title'>Out of Stock Items</div><div class='metric-value'>{out_stock}</div></div>", unsafe_allow_html=True)
        with m4:
            st.markdown(f"<div class='metric-card'><div class='metric-title'>Reviews Analyzed</div><div class='metric-value'>{len(reviews)}</div></div>", unsafe_allow_html=True)

        st.markdown("---")

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("#### 🏷️ Current Price & Discount Matrix")
            fig_bar = px.bar(
                df_latest,
                x="title",
                y="price",
                color="brand",
                hover_data=["original_price", "discount_percent"],
                title="Current Market Prices by Product",
                template="plotly_dark"
            )
            fig_bar.update_layout(xaxis_showticklabels=False)
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_c2:
            st.markdown("#### 📈 Multi-Snapshot Price History Trend")
            fig_line = px.line(
                df_merged,
                x="scraped_at",
                y="price",
                color="title",
                markers=True,
                title="Price Movement Over Time",
                template="plotly_dark"
            )
            st.plotly_chart(fig_line, use_container_width=True)

        # Discount Alerts Table
        st.markdown("#### 🔥 Active Discount & Price Drop Alerts")
        df_discounts = df_latest[df_latest["discount_percent"] > 0][["title", "brand", "category", "price", "original_price", "discount_percent"]].sort_values("discount_percent", ascending=False)
        st.dataframe(df_discounts, use_container_width=True)

    else:
        st.warning("No products found in database. Run the ETL pipeline from sidebar to populate data!")

# ---------------------------------------------------------
# TAB 3: AIRFLOW DAG & DATABASE INSPECTOR
# ---------------------------------------------------------
with tab3:
    st.markdown("### ⚙️ Airflow 2.x ETL DAG & Storage Status")
    st.info("The Airflow DAG `dags/ecommerce_etl_dag.py` defines 6 modular, sequential pipeline tasks:")

    task_cols = st.columns(6)
    tasks_info = [
        ("1. Extract Raw Data", "SerpAPI / Mock"),
        ("2. Clean Products", "Normalize & Discount"),
        ("3. Clean Reviews", "Sentiment Scoring"),
        ("4. Load SQLite", "Relational Store"),
        ("5. Load Chroma", "HuggingFace Vector"),
        ("6. Summary", "Verification Report")
    ]
    for col, (t_name, t_sub) in zip(task_cols, tasks_info):
        with col:
            st.markdown(f"**{t_name}**")
            st.caption(f"Status: ✅ SUCCESS\n\n({t_sub})")

    st.markdown("---")
    st.markdown("#### 🗄️ Database Tables Inspector")

    db_choice = st.selectbox("Select Database Table to Inspect", ["products", "price_history", "stock_status", "product_reviews"])
    sql_engine = SQLExecutor()

    if db_choice == "products":
        df_tbl = sql_engine.execute_custom_sql("SELECT * FROM products")
    elif db_choice == "price_history":
        df_tbl = sql_engine.execute_custom_sql("SELECT * FROM price_history ORDER BY scraped_at DESC")
    elif db_choice == "stock_status":
        df_tbl = sql_engine.execute_custom_sql("SELECT * FROM stock_status")
    else:
        df_tbl = sql_engine.execute_custom_sql("SELECT * FROM product_reviews")

    st.dataframe(df_tbl, use_container_width=True)
