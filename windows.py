import http.server
import socketserver
import subprocess

class ShutdownRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/shutdown_computer':
            self.send_response(200)
            self.end_headers()
            subprocess.call(['shutdown', '/s', '/t', '0'])

def run_server():
    PORT = 5500  # Public port number example
    with socketserver.TCPServer(("", PORT), ShutdownRequestHandler) as httpd:
        print(f"Listening for shutdown requests on port {PORT}...")
        httpd.serve_forever()

if __name__ == '__main__':
    run_server()
