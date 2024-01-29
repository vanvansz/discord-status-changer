import os
import requests
import json
import time
import logging

logging.basicConfig(format='%(message)s', level=logging.INFO)

class Main:
    def __init__(self, token, statuses, delay):
        self.token = token
        self.statuses = statuses
        self.delay = delay
        self.rotating = False

        self.setup_status()

    def setup_status(self):
        while True:
            logging.info("Select status mode:\n")
            logging.info("1. One-by-one status")
            logging.info("2. Rotating status\n")
            logging.info("Press Ctrl+C again to exit")

            try:
                choice = input("Enter your choice (1 or 2): ")
                if choice == '1':
                    self.one_by_one_status()
                elif choice == '2':
                    self.rotating_status()
                else:
                    logging.error("Invalid choice. Please enter 1 or 2.")

            except KeyboardInterrupt:
                logging.info("Returning to options. Press Ctrl+C again to exit.")
                continue

    def set_status(self, status):
        response = requests.patch(
            "https://discord.com/api/v9/users/@me/settings",
            headers={"authorization": self.token, "content-type": "application/json"},
            data=json.dumps({"custom_status": {"text": status, "emoji_name": "👉"}})
        )

        if response.status_code != 200:
            logging.error(f"Failed to set status. Status code: {response.status_code}")

    def one_by_one_status(self):
        try:
            for status in self.statuses:
                i = 0
                while i < len(status):
                    string = status[0:i+1]
                    self.set_status(string)
                    i += 1
                    time.sleep(self.delay)
                    if i == len(status):
                        time.sleep(self.delay)

        except KeyboardInterrupt:
            logging.info("Returning to options. Press Ctrl+C again to exit.")
            return

    def rotating_status(self):
        i = 0
        try:
            while True:
                status = self.statuses[i % len(self.statuses)]
                self.set_status(status)
                i += 1
                time.sleep(self.delay)

        except KeyboardInterrupt:
            logging.info("Returning to options. Press Ctrl+C again to exit.")
            return

if __name__ == "__main__":
    token = input("Enter your Discord token: ")

    try:
        if requests.patch("https://discord.com/api/v9/users/@me", headers={"authorization": token, "content-type": "application/json"}).status_code == 400:
            statuses = [
                ".gg/plughub",
                "600+ Vouches",
                "Trusted Vendor"
            ]
            delay = float(input("Enter delay between status changes (in seconds): "))
            Main(token, statuses, delay)
        else:
            logging.error("Failed to connect to token")
            exit()
    except Exception as e:
        logging.exception(f"An error occurred: {e}")
