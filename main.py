from flask import Flask
import os
import threading 
import webview
import socket

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True 

app.secret_key = os.environ.get('SECRET_KEY', 'dev-fallback-key')


from views import *


# ---- PyWebView ---- #

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('', 0))  
        return sock.getsockname()[1]

port = find_free_port()
class Api:
    def open_path_folder(self):
        result = webview.windows[0].create_file_dialog(webview.FOLDER_DIALOG)
        if result and len(result) > 0:
            return result[0]
        return None
    

def run_flask():
    app.run(port=port, debug=True, use_reloader=False)

if __name__ == "__main__":
    api = Api()
    thread = threading.Thread(target=run_flask)
    thread.daemon = True
    thread.start()

    webview.create_window(
        "WAVV",
        f"http://localhost:{port}",
        width=800,
        height=600,
        fullscreen=True,
        js_api=api
    )

    webview.start(debug=True)

# ---- PyWebView ---- #
