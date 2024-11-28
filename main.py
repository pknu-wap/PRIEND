import communication
import plant_status_data as psd

sensor_thread = psd.Sensor()
communication_thread = communication.Communication()

sensor_thread.start()
communication_thread.start()