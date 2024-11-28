import threading
import time
import sensors.spi as spi
import sensors.dht as dht

SOIL_MOISTURE = 0
ILLUMINANCE = 1
INTERVAL = 1

class PlantStatus:
    def __init__(self):
        self.id = 1
        self.soil_moisture = 0
        self.temperature = 0
        self.humidity = 0
        self.illuminance = 0

    def dict_data(self):
        return {
            "potId": self.id,
            "plantSoilMoisture": self.soil_moisture,
            "plantTemperature": self.temperature,
            "plantHumidity": self.humidity,
            "plantIlluminance": self.illuminance
            }

data = PlantStatus()

class Sensor(threading.Thread):

    def __init__(self):
        super().__init__()
        self.lastMillis = time.monotonic()
        self.dht_reader = dht.DHT()
        self.spi_reader = spi.Spi(0, 0, 1000000)

    def run(self):
        while(True):
            curMillis = time.monotonic()
            if(curMillis - self.lastMillis < INTERVAL):
                continue
            self.lastMillis = curMillis

            # map 1023~0 to 0~100
            data.soil_moisture = (1023 - self.spi_reader.analog_read(SOIL_MOISTURE)) * 100 /1024
            data.temperature = self.dht_reader.read_temperature()
            data.humidity = self.dht_reader.read_humidity()
            # map 0~600 to 0~100
            data.illuminance = self.spi_reader.analog_read(ILLUMINANCE) / 6

            # print("sm: {}\ttemp: {}\thum: {}\till: {}".format(data.soil_moisture, data.temperature, data.humidity, data.illuminance))