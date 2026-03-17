


from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.rag_pipeline import RAGPipeline
import threading
import webbrowser

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
rag = RAGPipeline()


def open_browser():
    webbrowser.open("http://localhost:8000/static/index.html")


@app.on_event("startup")
async def startup_event():
    threading.Timer(1.5, open_browser).start()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>✅ Server is running</h2>
    <a href="/static/index.html">👉 Open App</a>
    """


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".txt", ".pdf")):
        return {"error": "Only TXT and PDF files are supported"}
    content = await file.read()
    return await rag.ingest_document(file.filename, content)


@app.post("/query")
async def query(data: dict):
    question = data.get("question", "").strip()
    if not question:
        return {"answer": "Please enter a valid question.", "sources": []}
    return await rag.query(question)


@app.get("/health")
async def health():
    return {"status": "ok"}