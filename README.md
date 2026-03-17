# 🩺 MedScan AI — Medical Report Assistant

> An AI-powered RAG application that reads medical reports and explains them in plain language using **Endee** as the vector database.

[![Endee Vector DB](https://img.shields.io/badge/Vector%20DB-Endee-blue)](https://github.com/endee-io/endee)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)](https://fastapi.tiangolo.com)
[![LLaMA](https://img.shields.io/badge/LLM-LLaMA%203.3%2070B-orange)](https://groq.com)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow)](https://python.org)

---

## 📌 Project Overview

**MedScan AI** is an intelligent medical report assistant that allows patients to upload their lab reports (PDF or TXT) and ask plain-language questions about their health.

The system uses **Retrieval Augmented Generation (RAG)** with **Endee vector database** to:
1. Extract text from medical reports (including scanned PDFs via OCR)
2. Convert text chunks into vector embeddings (384 dimensions)
3. Store and retrieve vectors using **Endee** for fast semantic search
4. Generate AI-powered answers using LLaMA 3.3 70B via Groq API

**Key capabilities:**
- 🔍 Plain-language explanation of medical test results
- 🦠 Possible disease/condition identification
- 🚦 Severity rating — Mild / Moderate / Critical
- ✅ Practical next steps and suggestions
- 📄 Scanned PDF support via OCR (Tesseract)

---

## 🏗️ System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                        MedScan AI System                        │
└─────────────────────────────────────────────────────────────────┘

  User Browser (index.html)
       │
       │  HTTP (upload / query)
       ▼
  ┌─────────────┐
  │  FastAPI    │  ← app/main.py
  │  Server     │
  └──────┬──────┘
         │
         ▼
  ┌─────────────────────────────────────────────┐
  │           RAG Pipeline (rag_pipeline.py)    │
  │                                             │
  │  1. Document Ingestion                      │
  │     ├── PDF text extraction (pypdf)         │
  │     ├── OCR for scanned PDFs (Tesseract)    │
  │     └── Text chunking (300 words/chunk)     │
  │                                             │
  │  2. Embedding Generation                    │
  │     └── sentence-transformers              │
  │         (all-MiniLM-L6-v2, dim=384)        │
  │                                             │
  │  3. Vector Storage ──────────────────────► Endee
  │     └── Upsert chunks into Endee index      Vector DB
  │         (cosine similarity, INT8)           (port 8080)
  │                                             │
  │  4. Retrieval                               │
  │     └── Query Endee with question vector ◄──┘
  │         top-k similar chunks returned      │
  │                                             │
  │  5. Answer Generation                       │
  │     └── Groq API (LLaMA 3.3 70B)          │
  │         with retrieved context             │
  └─────────────────────────────────────────────┘
```

### Component Breakdown

| Component | Technology | Purpose |
|---|---|---|
| Web Server | FastAPI + Uvicorn | REST API endpoints |
| Frontend | HTML/CSS/JS | Upload UI + Q&A interface |
| Document Processor | pypdf + Tesseract OCR | Extract text from PDF/TXT |
| Embeddings | sentence-transformers | Convert text to 384-dim vectors |
| **Vector Database** | **Endee** | **Store and retrieve vectors** |
| LLM | Groq (LLaMA 3.3 70B) | Generate plain-language answers |

---

## 🔷 How Endee is Used

[Endee](https://github.com/endee-io/endee) is the **core vector database** for storing and retrieving medical report embeddings in this RAG pipeline.

### Why Endee?
- High-performance vector search built for RAG workloads
- Low latency retrieval even on modest hardware
- Clean Python SDK with cosine similarity and INT8 precision support
- Docker-based deployment — easy to run locally
- Designed for up to 1B vectors on a single node

### Endee Integration

**1. Connect and Create Index** (`app/rag_pipeline.py`):
```python
from endee import Endee, Precision

client = Endee()  # connects to localhost:8080

client.create_index(
    name="medical_reports",
    dimension=384,         # all-MiniLM-L6-v2 output dimension
    space_type="cosine",   # cosine similarity search
    precision=Precision.INT8
)
```

**2. Store Vectors (Document Upload)**:
```python
index = client.get_index("medical_reports")
index.upsert([
    {
        "id": "chunk_0",
        "vector": embedding.tolist(),  # 384-dim vector
        "meta": {"text": chunk_text, "index": 0}
    }
])
```

**3. Retrieve Vectors (Question Answering)**:
```python
results = index.query(
    vector=question_embedding.tolist(),
    top_k=5  # retrieve top 5 similar chunks
)
# Use retrieved chunks as context for LLM
```

### Full RAG Flow with Endee

```
User Question: "What is wrong with my report?"
       │
       ▼
Embed question using all-MiniLM-L6-v2
→ [0.23, -0.11, 0.45, ...] (384 dimensions)
       │
       ▼
Endee.query(vector, top_k=5)
→ Returns 5 most similar report chunks
       │
       ▼
Build context from top 3 chunks
       │
       ▼
Send to LLaMA 3.3 70B via Groq API
       │
       ▼
AI Answer with disease + severity + next steps
```

---

## 🗂️ Project Structure

```
medical-rag-endee/
│
├── app/
│   ├── main.py                # FastAPI routes (/upload, /query, /health)
│   ├── rag_pipeline.py        # RAG logic — Endee integration
│   ├── embeddings.py          # sentence-transformers (all-MiniLM-L6-v2)
│   ├── document_processor.py  # PDF/TXT extraction + OCR
│   ├── llm.py                 # Groq LLM (LLaMA 3.3 70B)
│   └── __init__.py
│
├── static/
│   └── index.html             # Full UI (landing + upload + results)
│
├── run.py                     # App start script (auto-opens browser)
├── docker-compose.yml         # Endee vector DB container
├── requirements.txt           # Python dependencies
├── .env                       # API keys (not committed to git)
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| **Vector Database** | **Endee (Docker)** |
| AI / LLM | Groq API — LLaMA 3.3 70B Versatile |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2, 384 dims) |
| PDF Processing | pypdf (text PDFs) + pytesseract (scanned PDFs) |
| OCR | Tesseract + Poppler |
| Frontend | HTML + CSS + JavaScript (single file, no framework) |

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- Docker Desktop (for running Endee)
- Tesseract OCR installed
- Poppler installed
- Groq API key — free at [console.groq.com](https://console.groq.com)

---

### Step 1 — Star & Fork Endee (Mandatory)

1. Go to: https://github.com/endee-io/endee
2. Click ⭐ **Star**
3. Click **Fork** → fork to your account

### Step 2 — Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/medical-rag-endee.git
cd medical-rag-endee
```

### Step 3 — Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 4 — Install Python Dependencies

```bash
pip install fastapi uvicorn pypdf python-multipart scikit-learn
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install sentence-transformers transformers groq python-dotenv
pip install pytesseract pdf2image pillow endee
```

### Step 5 — Install Tesseract OCR

**Windows:** Download from https://github.com/UB-Mannheim/tesseract/wiki

Install to default path: `C:\Program Files\Tesseract-OCR\`

### Step 6 — Install Poppler

**Windows:**
1. Download from: https://github.com/oschwartz10612/poppler-windows/releases
2. Extract the zip
3. Update the path in `app/document_processor.py`:
```python
POPPLER_PATH = r'C:\path\to\poppler\Library\bin'
```

### Step 7 — Set Up API Key

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

### Step 8 — Start Endee Vector Database

```bash
docker-compose up -d
```

Verify Endee is running — open in browser:
```
http://localhost:8080
```
You should see the Endee dashboard.

### Step 9 — Run the Application

```bash
python run.py
```

App opens automatically at:
```
http://localhost:8000/static/index.html
```

---

## 📋 How to Use

**Step 1 — Upload Report**
- Click **"Choose File"** or drag & drop
- Select your `.pdf` or `.txt` medical report
- Click **"Upload Report"**
- Wait for ✅ **"Document processed successfully"**

## 🧪 Sample Reports for Testing

Sample reports are available in the `samples/` folder:

| File | Description |
|---|---|
| `sample_report_1.txt` | Blood test with diabetes + high cholesterol |
| `sample_report_2.txt` | Real World report |
| `sample_report_3.txt` | Thyroid disorder report |
| `sample_report_4.txt` | Normal healthy report |

Upload any of these to test the app instantly!

**Step 2 — Ask Questions**

Use quick buttons or type your own:
- *"What is wrong with my report?"*
- *"Is my condition serious?"*
- *"What disease might I have?"*
- *"Explain my key values"*
- *"What should I do next?"*

**Step 3 — Read Your Results**

Each answer includes:
- 🔍 Plain-language explanation
- 🦠 Possible condition/disease name
- 🚦 Severity: 🟢 Mild / 🟡 Moderate / 🔴 Critical
- ✅ Suggested next steps

---

## ⏳ Important — Browser Popup Behaviour

When you run `python run.py`:
1. Server loads the AI model — takes **3–5 seconds**
2. Browser **automatically opens** with the app
3. It may open as a **new window** — this is normal

> ⚠️ **Do NOT close the browser when it first pops up.**
> The app is fully loaded and ready to use!

**Tip:** Bookmark `http://localhost:8000/static/index.html` with `CTRL+D` for quick access.

---

## 🔧 Troubleshooting

| Error | Fix |
|---|---|
| `No module named 'endee'` | `pip install endee` |
| `No module named 'fastapi'` | Activate venv first: `venv\Scripts\activate` |
| Endee connection failed | Run `docker-compose up -d` first |
| OCR gives wrong values | Type values into `.txt` file and upload that instead |
| Browser doesn't open | Go to `http://localhost:8000/static/index.html` manually |

---

## 🔒 Privacy

- Medical data is **never stored permanently** — cleared on server restart
- All processing runs **locally** on your machine
- Only text is sent to Groq API for AI generation — no files or images

---

## ⚠️ Medical Disclaimer

> This tool is for **informational purposes only**.
> It is **NOT** a substitute for professional medical advice, diagnosis, or treatment.
> Always consult a qualified doctor.

---

## 📬 Quick Command Reference

```bash
# Start Endee vector database
docker-compose up -d

# Activate venv + start app
venv\Scripts\activate
python run.py

# Open app in browser
http://localhost:8000/static/index.html

# Check server health
http://localhost:8000/health

# Endee dashboard
http://localhost:8080

# Stop app
CTRL+C

# Stop Endee
docker-compose down
```

---

## 🔗 Links

- **Endee GitHub:** https://github.com/endee-io/endee
- **Endee Docs:** https://docs.endee.io
- **Groq API:** https://console.groq.com
- **This Project:** https://github.com/sanjana56789/medical-rag-endee
