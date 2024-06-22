import os
import time
import requests
import subprocess

# URL to check the on/off status
status_url = 'https://raw.githubusercontent.com/rexzy69/Seawee/main/on-off.txt'

def get_remote_status():
    try:
        response = requests.get(status_url)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"Error fetching remote status: {e}")
        return None

def check_and_shutdown():
    while True:
        status = get_remote_status()
        if status == 'on':
            print("Shutdown signal received. Shutting down the computer...")
            subprocess.call(['shutdown', '/s', '/t', '0'])
        else:
            print("No shutdown signal. Checking again in 5 seconds...")
        time.sleep(5)

if __name__ == '__main__':
    check_and_shutdown()
