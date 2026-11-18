import http.server
import socketserver
import os
import sys
from pathlib import Path

PORT = 5555
BASE_DIR = Path(__file__).resolve().parent
DIST_DIR = BASE_DIR / "frontend" / "dist"

class SPAHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST_DIR), **kwargs)

    def do_GET(self):
        # Strip query parameters
        url_path = self.path.split("?")[0].lstrip("/")
        target_file = (DIST_DIR / url_path).resolve()

        # If file doesn't exist and isn't a static asset, rewrite to index.html for React Router SPA
        if not target_file.is_file() and not self.path.startswith("/assets/"):
            self.path = "/index.html"

        return super().do_GET()

if __name__ == "__main__":
    if not DIST_DIR.exists():
        print(f"Error: {DIST_DIR} not found. Please ensure frontend/dist exists.")
        sys.exit(1)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), SPAHTTPRequestHandler) as httpd:
        print("=" * 60)
        print(f"StressGuard AI - Python Static Frontend Server")
        print(f"Local URL: http://localhost:{PORT}")
        print(f"Network:   http://127.0.0.1:{PORT}")
        print("Running with Python standard library (No Node.js/npm required)")
        print("=" * 60)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down frontend server.")
            httpd.shutdown()
