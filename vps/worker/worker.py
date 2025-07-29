import os
import time
import requests

PLUTO = os.getenv("PLUTO_URL")
TOKEN = os.getenv("PLUTO_TOKEN", "")


def poll():
    r = requests.get(f"{PLUTO}/log", timeout=10)
    print("PLUTO LOG:", r.status_code, r.text[:200])


if __name__ == "__main__":
    while True:
        try:
            poll()
        except Exception as e:
            print("Error:", e)
        time.sleep(30)
