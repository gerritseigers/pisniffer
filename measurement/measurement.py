import random
from logger_config import logger
from session_config import session
from models.model import Device, Measurement
import datetime
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
import RPi.GPIO as GPIO
from adafruit_ads1x15.analog_in import AnalogIn
from shared import measurement_counter, increment_measurement_counter


pulse_pin=18
GPIO.setmode(GPIO.BCM)
GPIO.setup(pulse_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


pulse_counter = 0

def count_pulse(channel):
    global pulse_counter
    pulse_counter+=1

def read_sensors(message_queue):
    global pulse_counter

    logger.info("Starting the data generation loop...")
    device = session.query(Device).first()
    global measurement_counter  # Ensure the counter is global

    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)

    GPIO.add_event_detect(pulse_pin, GPIO.RISING, callback=count_pulse)

    while True:
        try:


            # Add the measurement to the database
            current_time = datetime.datetime.now()
            chan = AnalogIn(ads, ADS.P0)
            logger.info(f"Channel 0: {chan.voltage}V")
            logger.info(f"Pulse counter: {pulse_counter}")
            measurement = Measurement(
                value=chan.voltage, 
                date=current_time, 
                device=device)
            session.add(measurement)
            session.commit()

            data = {
                "device_id": f"{device.name}",
                "temperature": chan.voltage,
                "edge_time_stamp": f"{current_time}"
            }

            message_queue.put(data)
            increment_measurement_counter()

            device = session.query(Device).filter_by(name="device1").first()
            time.sleep(device.measurement_interval)
        except Exception as e:
            logger.error(f"An error occurred while reading the sensors {e}")    
            continue

