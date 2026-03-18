import uvicorn
import webbrowser
import subprocess
import os

if __name__ == "__main__":
    subprocess.Popen(["docker", "start", "endee-server"])
    
    # Only open browser in main process, not reloader
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        print("\n🌐 Open this in your browser:")
        print("👉 http://localhost:8000/static/index.html\n")
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)