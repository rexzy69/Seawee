import pyttsx3
import keyboard
import os
import platform
import time

restart_confirmed = False
instruction_spoken = False

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    engine.say(text)
    engine.runAndWait()

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
