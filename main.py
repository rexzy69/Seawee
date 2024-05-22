import pyttsx3
import keyboard
import os
import platform
import requests
import shutil
import time
import zipfile
import sys

restart_confirmed = False
instruction_spoken = False

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

def check_for_updates():
    try:
        github_version_url = "https://raw.githubusercontent.com/rexzy69/Seawee/main/version.txt"
        response = requests.get(github_version_url)
        github_version = response.text.strip()

        with open("version.txt", "r") as file:
            local_version = file.read().strip()

        print("Local version:", local_version)
        print("GitHub version:", github_version)

        if local_version == github_version:
            speak("No update found.")
        else:
            speak("Update found. Updating files.")
            download_and_replace_files()
    except Exception as e:
        speak("Error checking for updates. Please try again later.")

def download_and_replace_files():
    try:
        github_url = "https://github.com/rexzy69/Seawee/archive/main.zip"
        response = requests.get(github_url)
        with open("update.zip", "wb") as file:
            file.write(response.content)

        with zipfile.ZipFile("update.zip", "r") as zip_ref:
            zip_ref.extractall("temp_folder")

        for file in os.listdir("temp_folder/Seawee-main"):
            shutil.move(os.path.join("temp_folder/Seawee-main", file), os.path.join(".", file))
        
        shutil.rmtree("temp_folder")
        os.remove("update.zip")

        speak("Files updated successfully.")
        sys.exit()  # Exit the script after updating files
    except Exception as e:
        speak("Error updating files. Please try again later.")

def on_home_press():
    global instruction_spoken
    if not restart_confirmed and not instruction_spoken:
        speak("Press the PyUp key on the keyboard to confirm restart. Press Alt to cancel.")
        instruction_spoken = True
    elif restart_confirmed:
        speak("Restart confirmed.")

def on_pyup_press():
    global restart_confirmed
    if not restart_confirmed:
        speak("Press Alt to cancel. Restart confirmed.")
        restart_confirmed = True
        restart_computer()

def on_alt_press():
    global instruction_spoken
    if not restart_confirmed:
        speak("Restart canceled.")
        instruction_spoken = False  # Reset the instruction spoken flag
        time.sleep(1)  # Add a delay after speaking cancellation message to ensure completion

def restart_computer():
    system_name = platform.system()
    if system_name == "Windows":
        os.system("shutdown /r /t 0")
    elif system_name == "Linux" or system_name == "Darwin":
        os.system("sudo shutdown -r now")
    else:
        speak("Unsupported operating system for restart command.")

if __name__ == "__main__":
    # Check for updates
    check_for_updates()

    # Define the keys to listen for
    home_key = 'home'
    pyup_key = 'page up'  # Using 'page up' as the PyUp key for this example
    alt_key = 'alt'

    # Set up event listeners
    keyboard.on_press_key(home_key, lambda e: on_home_press())
    keyboard.on_press_key(pyup_key, lambda e: on_pyup_press())
    keyboard.on_press_key(alt_key, lambda e: on_alt_press())

    # Keep the program running
    print("Listening for key presses. Press ESC to stop.")
    keyboard.wait('esc')
