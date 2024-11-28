# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import adafruit_dht

class DHT:
    def __init__(self):
        # set dht22 as gpio4
        self.dhtDevice = adafruit_dht.DHT22(board.D4)

    # return celsius temperature
    def read_temperature(self):
        try:
            return self.dhtDevice.temperature
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            return None
        except Exception as error:
            self.dhtDevice.exit()
            raise error
    
    
    # return humidity
    def read_humidity(self):
        try:
            return self.dhtDevice.humidity
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            return None
        except Exception as error:
            self.dhtDevice.exit()
            raise error