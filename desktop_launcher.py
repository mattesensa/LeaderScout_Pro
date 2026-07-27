import sys
import os
import time
import webbrowser
import threading

# Force stdout/stderr UTF-8 encoding on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Handle PyInstaller paths
if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

# Import Flask app
from app import app

# Configure template & static folders for PyInstaller bundle
app.template_folder = os.path.join(bundle_dir, 'templates')
app.static_folder = os.path.join(bundle_dir, 'static')

def open_browser():
    """Waits 1.5 seconds and opens the default browser to the app URL."""
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    print("--------------------------------------------------")
    print("  [LeadScout PRO] Avvio del Server Desktop...")
    print("  Il browser si aprira automaticamente su http://127.0.0.1:5000")
    print("  Non chiudere questa finestra per mantenere attivo il programma.")
    print("--------------------------------------------------")
    
    # Start browser opener thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run server
    app.run(host="127.0.0.1", port=5000, debug=False)
