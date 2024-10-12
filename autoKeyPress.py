import time
import pyautogui

def press_keys():
    try:
        while True:
            # Press Enter key
            pyautogui.press('enter')

            # Pause for a moment (adjust as needed)
            #time.sleep(.000000000001)

            # Press Down Arrow key
            pyautogui.press('down')
            # Pause for a moment (adjust as needed)
            #time.sleep(.000000000001)

    except KeyboardInterrupt:
        # Handle Ctrl+C to stop the script
        print("\nScript stopped.")

if __name__ == "__main__":
    press_keys()





















