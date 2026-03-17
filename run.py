


import uvicorn
import webbrowser
import threading

def open_browser():
    webbrowser.open("http://localhost:8000/static/index.html")

if __name__ == "__main__":
    threading.Timer(3, open_browser).start()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)