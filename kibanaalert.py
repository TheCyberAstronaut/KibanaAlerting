import time
import requests
from dotenv import load_dotenv
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import json
import signal

# === Function to send alert to Discord ===
def send_discord_alert(alert):
    try:
        # JSON of Alert Description
        data = {
            "content": alert
        }

        # Send data
        response = requests.post(WEBHOOK_URL, json=data, headers= {"Content-Type": "application/json"})

        # Confirm POST request
        if response.status_code == 204:
            logging.warning("Alert sent to Discord successfully.")
        else:
            logging.warning(f"Failed to send alert. Status code: {response.status_code}, Response: {response.text}")
    
    except Exception as e:
        logging.warning(f"Error in function send_discord_alert(); {e}")

def handle_signal(signal_number, frame):
    logging.warning("Stopping log monitoring")
    observer.stop()

class LogFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == LOG_FILE_PATH:
            with open(LOG_FILE_PATH, "r") as file:
                # Read the last line of the file
                lines = file.readlines()
                if lines:
                    last_line = lines[-1].strip()

                    # Format string as json object
                    alert = json.loads(last_line)

                    if alert["log"]["logger"] == TARGET_MESSAGE:
                        
                        # Grab just the message
                        message = alert["message"]

                        # Cleanup alert string
                        if "Server log: " in message:
                            message = message.removeprefix("Server log: ")

                        # Log entry
                        logging.warning(f"Keyword detected: {message}")

                        # Send to discord
                        send_discord_alert(message)

# Main function
if __name__ == "__main__":
    load_dotenv("/opt/kibanaalerting/config.env") # Edit path to env here
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    LOG_FILE_PATH = os.getenv("LOG_FILE_PATH")
    TARGET_MESSAGE = os.getenv("TARGET_MESSAGE")
    APPLICATION_LOG_FILE_PATH = os.getenv("APPLICATION_LOG_FILE_PATH")

    try:
        logging.basicConfig(filename=APPLICATION_LOG_FILE_PATH, format="%(asctime)s %(message)s", level=logging.WARNING)

        event_handler = LogFileHandler()
        observer = Observer()
        observer.schedule(event_handler, path=LOG_FILE_PATH, recursive=False)

        # Register signal handlers for SIGTERM and SIGINT
        signal.signal(signal.SIGTERM, handle_signal)
        signal.signal(signal.SIGINT, handle_signal)

        logging.warning("Starting log monitoring")
        observer.start()
        logging.warning("Started log monitoring")

        while observer.is_alive():
            time.sleep(0.1)

    except Exception as e:
        handle_signal(None, None)
        logging.warning(f"Error: {e}")

    finally: 
        observer.join()
        logging.warning("Log monitoring stopped")
