import spidev

class Spi:

    def __init__(self, bus, device, frequency):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = frequency

    def analog_read(self, channel):
        r = self.spi.xfer2([1, (8 + channel) << 4, 0])
        adc_value = ((r[1] & 3) << 8) + r[2]
        return adc_value