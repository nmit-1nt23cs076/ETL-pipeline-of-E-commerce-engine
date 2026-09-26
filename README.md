# 🛒 E-Commerce Competitor Price & Review Tracking RAG Pipeline

An end-to-end **ETL + RAG (Retrieval-Augmented Generation) Pipeline** that automatically tracks competitor product prices, stock availability, and customer reviews — and provides a natural language chat assistant powered by **xAI Grok LLM**, **SQLite**, and **ChromaDB**.

---

## 🏛️ Architecture Overview

```
                      ┌─────────────────────────────────────────┐
                      │    SerpAPI Google Shopping / Mock Data   │
                      └────────────────────┬────────────────────┘
                                           │
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │    Airflow 2.x ETL Pipeline (6 Tasks)   │
                      │  Clean, Normalize, Calculate Discounts, │
                      │  Compute VADER Sentiment & Embeddings   │
                      └────────────┬────────────────┬───────────┘
                                   │                │
                                   ▼                ▼
            ┌───────────────────────────┐      ┌──────────────────────────┐
            │   SQLite Database         │      │   ChromaDB Vector Store  │
            │ (Products, Prices, Stock) │      │ (Reviews, Descriptions)  │
            └─────────────┬─────────────┘      └────────────┬─────────────┘
                          │                                 │
                          └──────────────┐   ┌──────────────┘
                                         ▼   ▼
                      ┌─────────────────────────────────────────┐
                      │    Smart Query Router (LangChain)       │
                      │   (Routes to SQL, Vector, or Hybrid)    │
                      └────────────────────┬────────────────────┘
                                           │
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │  xAI Grok LLM RAG Chain (ChatXAI)       │
                      │  Synthesizes Evidence & Formats Answer  │
                      └────────────────────┬────────────────────┘
                                           │
                                           ▼
                      ┌─────────────────────────────────────────┐
                      │  Streamlit Dashboard & Interactive UI   │
                      └─────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Language** | Python 3.10+ |
| **Orchestration** | Apache Airflow 2.x (standalone 6-task DAG) |
| **Data Source** | SerpAPI Google Shopping + Built-in Realistic Mock Generator |
| **LLM** | xAI Grok via `langchain-xai` (`ChatXAI`) |
| **Embeddings** | HuggingFace `all-MiniLM-L6-v2` (free, local) |
| **Structured DB** | SQLite (SQLAlchemy ORM - products, price history, stock levels) |
| **Vector Store** | ChromaDB (reviews, product descriptions, sentiment) |
| **Framework** | LangChain |
| **UI** | Streamlit (Interactive analytics dashboard + Q&A chat) |

---

## 💡 Why Dual Storage?

- **Structured Queries (SQL):** Questions like *"Which laptop is cheapest?"* or *"Which laptops dropped price this week?"* require relational SQL aggregation, indexing, and sorting.
- **Unstructured Queries (Vector):** Questions like *"What are customers complaining about in Samsung reviews?"* require semantic search over unstructured customer review texts and sentiment embeddings.
- **Smart Query Router:** Automatically analyzes intent and routes query to **SQL**, **Vector**, or **Hybrid** execution paths.

---

## 📂 Project Structure

```
ecommerce-tracker/
├── .env.example              # API keys template
├── .gitignore
├── requirements.txt
├── README.md
├── config.py                 # Centralized configuration
│
├── dags/                     # Airflow DAGs
│   └── ecommerce_etl_dag.py  # 6-task Airflow DAG
│
├── etl/
│   ├── __init__.py
│   ├── sources/
│   │   ├── __init__.py
│   │   ├── serp_scraper.py   # SerpAPI Google Shopping scraper
│   │   └── mock_generator.py # Realistic fake data generator
│   ├── transform.py          # Clean, normalize, discount %, sentiment
│   ├── load.py               # Load to SQLite + ChromaDB
│   └── runner.py             # Standalone ETL pipeline runner
│
├── db/
│   ├── __init__.py
│   ├── models.py             # SQLAlchemy models (Product, PriceHistory, StockStatus, ProductReview)
│   └── database.py           # SQLite connection & session management
│
├── rag/
│   ├── __init__.py
│   ├── embeddings.py         # HuggingFace all-MiniLM-L6-v2 embeddings
│   ├── router.py             # Smart query router (SQL vs Vector vs Hybrid)
│   ├── sql_agent.py          # SQLite structured query executor
│   ├── vector_search.py      # ChromaDB retriever for review search
│   └── chain.py              # Combined RAG chain with xAI Grok LLM
│
├── app.py                    # Streamlit dashboard + chat UI
├── data/
│   └── ecommerce.db          # SQLite database
└── vectorstore/              # ChromaDB vector store
```

---

## ⚡ Quick Start & Setup

### 1. Environment Setup
```bash
# Navigate to project directory
cd ecommerce-tracker

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your keys:
```bash
cp .env.example .env
```
Key configuration parameters:
- `XAI_API_KEY`: API Key from [console.x.ai](https://console.x.ai/) for Grok LLM
- `SERPAPI_API_KEY`: Key from [serpapi.com](https://serpapi.com/) for Google Shopping data (optional, falls back to Mock Generator)
- `GROK_MODEL`: Defaults to `grok-4`

### 3. Launch Streamlit UI
```bash
streamlit run app.py
```

---

## 🧪 Testing Verification Scenarios

1. **Ask SQL Query:** *"Which laptops dropped price this week?"*  
   ➔ **Route:** `🔵 SQL ROUTE`  
   ➔ Returns products with recent price reductions and exact savings.

2. **Ask Vector Query:** *"What are customers complaining about in Samsung reviews?"*  
   ➔ **Route:** `🟣 VECTOR ROUTE`  
   ➔ Performs semantic search in ChromaDB and retrieves specific negative feedback and sentiment.

3. **Ask Hybrid Query:** *"Which budget phones have good reviews?"*  
   ➔ **Route:** `🟢 HYBRID ROUTE`  
   ➔ Filters phones under budget threshold in SQLite DB and evaluates positive review embeddings in ChromaDB.


