import requests
import json
import time

print("vanvansz - discord\n")

token = 'TOKEN GOES HERE'
statuses = [
    "STATUS 1",
    "STATUS 2",
    "STATUS 3"
]
delay = 1


class Main:
    def __init__(self, token, statuses, delay):
        self.token = token
        self.statuses = statuses
        self.delay = delay
        self.rotating = False

        self.setup_status()

    def setup_status(self):
        print("Select status mode:")
        print("1. Letter-By-Letter status")
        print("2. Rotating status")
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            self.one_by_one_status()
        elif choice == '2':
            self.rotating_status()
        else:
            print("Invalid choice. Exiting.")
            exit()

    def set_status(self, status):
        requests.patch(
            "https://discord.com/api/v9/users/@me/settings",
            headers={"authorization": self.token, "content-type": "application/json"},
            data=json.dumps({"custom_status": {"text": status, "emoji_name": "👉"}})
        )

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
            print("Stopped auto status!")
            exit()

    def rotating_status(self):
        i = 0
        try:
            while True:
                status = self.statuses[i % len(self.statuses)]
                self.set_status(status)
                i += 1
                time.sleep(self.delay)

        except KeyboardInterrupt:
            print("Stopped auto status!")
            exit()


if __name__ == "__main__":
    if requests.patch("https://discord.com/api/v9/users/@me", headers={"authorization": token, "content-type": "application/json"}).status_code == 400:
        Main(token, statuses, delay)
    else:
        print("Failed to connect to token")
        exit()
