# 🩺 MedScan AI — Medical Report Assistant

> An AI-powered web app that reads your medical reports and explains them in plain, simple language. No medical degree required.

---

## 📸 What It Does

- Upload any medical report (PDF, scanned image, or TXT)
- Ask questions like *"What is wrong with my report?"* or *"Is my condition serious?"*
- Get instant AI-powered answers with:
  - 🔍 Plain-language explanation of your results
  - 🦠 Possible condition or disease names
  - 🚦 Severity rating — Mild / Moderate / Critical
  - ✅ Practical next steps and suggestions

---

## 🗂️ Project Structure

```
medical-rag/
│
├── app/
│   ├── main.py                # FastAPI server (routes)
│   ├── rag_pipeline.py        # Core RAG logic — embedding + retrieval + LLM
│   ├── embeddings.py          # Converts text chunks → vectors
│   ├── document_processor.py  # Extracts text from PDF/TXT (with OCR support)
│   ├── llm.py                 # Groq LLM integration (LLaMA 3.3 70B)
│   └── __init__.py
│
├── static/
│   ├── index.html             # Full UI (landing page + upload + results)
│   ├── style.css              # (legacy, styles now inside index.html)
│   └── script.js              # (legacy, JS now inside index.html)
│
├── run.py                     # ✅ Start the app with this
├── requirements.txt           # Python dependencies
├── .env                       # Your Groq API key (never share this!)
└── README.md                  # This file
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| AI Model | Groq API — LLaMA 3.3 70B Versatile |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Search | scikit-learn cosine similarity |
| PDF Reading | pypdf (text PDFs) + pytesseract OCR (scanned PDFs) |
| OCR Engine | Tesseract + Poppler |
| Frontend | Pure HTML/CSS/JS (no framework needed) |

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- Tesseract OCR installed
- Poppler installed
- Groq API key (free at [console.groq.com](https://console.groq.com))

---

### Step 1 — Clone / Navigate to Project
```bash
cd medical-rag
```

### Step 2 — Create Virtual Environment
```bash
python -m venv venv
```

### Step 3 — Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```
**Mac/Linux:**
```bash
source venv/bin/activate
```

> ⚠️ You will see `(venv)` at the start of your terminal. Always activate before running the app.

### Step 4 — Install Dependencies
```bash
pip install fastapi uvicorn pypdf python-multipart scikit-learn
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install sentence-transformers transformers groq python-dotenv
pip install pytesseract pdf2image pillow
```

### Step 5 — Install Tesseract OCR (for scanned PDFs)

**Windows:**
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to: `C:\Program Files\Tesseract-OCR\`

### Step 6 — Install Poppler (for scanned PDFs)

**Windows:**
1. Download from: https://github.com/oschwartz10612/poppler-windows/releases
2. Extract the zip
3. Note the path to the `bin` folder (e.g. `C:\Users\YourName\Downloads\poppler\poppler-25.12.0\Library\bin`)
4. Update this path in `app/document_processor.py`:
```python
POPPLER_PATH = r'C:\Users\YourName\Downloads\poppler\poppler-25.12.0\Library\bin'
```

### Step 7 — Set Up API Key
```bash
# Windows
echo GROQ_API_KEY=your_groq_key_here > .env
```
Get your free key from: https://console.groq.com

---

## ▶️ Running the App

```bash
# Always activate venv first!
venv\Scripts\activate

# Then run
python run.py
```

---

## ⏳ Important — Browser Popup Behaviour

> **Please read this before using the app!**

When you run `python run.py`, the following happens:

1. The terminal loads the AI model — this takes **3–5 seconds**
2. After loading, the browser **automatically opens** with the app
3. The browser may open as a **new window or new tab** — this is normal Windows behaviour and cannot be changed easily

**⚠️ Do NOT close the browser immediately when it opens.**
The app is fully loaded and ready to use. Take a moment to look at it before deciding to close.

**If the browser opens but the page looks blank:**
- Wait 2–3 seconds and refresh with `CTRL + R`
- The server may still be finishing startup

**Recommended:** Bookmark the URL for quick access:
```
http://localhost:8000/static/index.html
```
Press `CTRL + D` in Chrome to save the bookmark. Then just click it after starting the server.

---

## 📋 How to Use

### Step 1 — Upload Your Report
- Click **"Choose File"** or drag & drop your file
- Supported: `.pdf` (text or scanned) and `.txt`
- Wait for the ✅ **"Document processed successfully"** message

### Step 2 — Ask Questions
Use the quick-question buttons or type your own:
- *"What is wrong with my report?"*
- *"Is my condition serious?"*
- *"What disease might I have?"*
- *"Explain my haemoglobin level"*
- *"What should I do next?"*

### Step 3 — Read Your Results
Each answer includes:
- 🔍 What the report shows (in simple language)
- 🦠 Possible condition name(s)
- 🚦 Severity: 🟢 Mild / 🟡 Moderate / 🔴 Critical
- ✅ Suggested next steps

---

## 📄 Supported File Types

| Type | Support |
|---|---|
| Text-based PDF | ✅ Full support |
| Scanned PDF (photo of report) | ✅ Via OCR |
| TXT file | ✅ Full support |
| JPG / PNG image | ✅ Via OCR |

> **Tip:** If your scanned PDF gives incomplete results, type the values manually into a `.txt` file and upload that instead. OCR accuracy depends on image quality.

---

## 🔧 Troubleshooting

### `ModuleNotFoundError: No module named 'fastapi'`
You forgot to activate the virtual environment:
```bash
venv\Scripts\activate
python run.py
```

### `ModuleNotFoundError: No module named 'pdf2image'`
```bash
pip install pdf2image pytesseract pillow
```

### `❌ Could not extract text from PDF`
Your PDF is a scanned image. Make sure:
- Tesseract is installed at `C:\Program Files\Tesseract-OCR\tesseract.exe`
- Poppler path in `document_processor.py` is correct
- Or just type the values into a `.txt` file and upload that

### App opens in the wrong browser
This is normal — Python's `webbrowser` module opens your system's default browser.
To fix: set Chrome as your default browser in Windows Settings, or manually go to:
```
http://localhost:8000/static/index.html
```

### OCR gives incomplete/wrong values
The scanned report image quality may be low. Best solution:
- Create a `.txt` file with the values manually typed in
- Upload the `.txt` instead of the scanned PDF

---

## 🔒 Privacy

- Your medical data is **never stored permanently**
- All processing happens **locally on your machine**
- The only external service used is **Groq API** for AI text generation
- No data is saved after you close the server

---

## ⚠️ Medical Disclaimer

> This tool is for **informational purposes only**.
> It is **NOT** a substitute for professional medical advice, diagnosis, or treatment.
> Always consult a qualified doctor for proper medical guidance.

---

## 👩‍💻 Built By

**Sanjana Madi**
Medical Report Assistant — AI Final Year Project
Alva's Health Centre Report Testing ✅

---

## 📬 Quick Command Reference

```bash
# Start app
venv\Scripts\activate
python run.py

# Open in browser
http://localhost:8000/static/index.html

# Stop server
CTRL + C

# Check server health
http://localhost:8000/health
```
