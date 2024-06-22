import subprocess

cmd = ['python', 'windows.py']
subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
