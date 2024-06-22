import http.server
import socketserver
import subprocess

class ShutdownRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/shutdown_computer':
            self.send_response(200)
            self.end_headers()
            subprocess.call(['shutdown', '/s', '/t', '0'])

PORT = 8000  # Choose any port that is not being used

with socketserver.TCPServer(("", PORT), ShutdownRequestHandler) as httpd:
    print(f"Listening for shutdown requests on port {PORT}...")
    httpd.serve_forever()
