import os
import time
import requests
import env
import plant_status_data as psd
import threading

INTERVAL = 5

class Communication(threading.Thread):
    def __init__(self):
        super().__init__()
        # HTTP request URL
        self.url = os.getenv("HTTP_REQ", env.HTTP_REQ) + env.UPDATE
        self.lastSec = time.monotonic()

    def run(self):
        while True:
            curSec = time.monotonic()
            if(curSec - self.lastSec < INTERVAL):
                continue
            self.lastSec = curSec

            try:
                # Make POST request
                response = requests.post(self.url, json=psd.data.dict_data())

                # check response
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        print("data transfer success:", psd.data.dict_data())
                        print("server response:", response_data)
                    except ValueError:
                        print("Server response missed.")
                        print("server response:", response.text)
                else:
                    print("data transfer fail:", response.status_code, response.text)

            except requests.exceptions.RequestException as e:
                # HTTP request error handling
                print("HTTP request error:", e)
                time.sleep(1)
            finally:
                pass