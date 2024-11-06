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
    pulse_counter += 1
    if pulse_counter > 2147483647:  # Assuming 32-bit integer max value
        pulse_counter = 0

def read_sensors(message_queue):
    global pulse_counter

    logger.info("Starting the data generation loop...")
    device = session.query(Device).first()
    global measurement_counter  # Ensure the counter is global

    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    ads_49 = ADS.ADS1115(i2c, address=0x49)

    GPIO.add_event_detect(pulse_pin, GPIO.RISING, callback=count_pulse)

    while True:
        try:
            # Add the measurement to the database
            current_time = datetime.datetime.now()
            chan_0 = AnalogIn(ads, ADS.P0)
            chan_1 = AnalogIn(ads, ADS.P1)
            chan_2 = AnalogIn(ads, ADS.P2)
            chan_3 = AnalogIn(ads, ADS.P3)
            chan_4 = AnalogIn(ads_49, ADS.P0)
            chan_5 = AnalogIn(ads_49, ADS.P1)
            chan_6 = AnalogIn(ads_49, ADS.P2)
            chan_7 = AnalogIn(ads_49, ADS.P3)
            logger.info(f"Channel 0: {chan_0.voltage}V")
            logger.info(f"Channel 1: {chan_1.voltage}V")
            logger.info(f"Channel 2: {chan_2.voltage}V")
            logger.info(f"Channel 3: {chan_3.voltage}V")
            logger.info(f"Channel 4: {chan_4.voltage}V")
            logger.info(f"Channel 5: {chan_5.voltage}V")
            logger.info(f"Channel 6: {chan_6.voltage}V")
            logger.info(f"Channel 7: {chan_7.voltage}V")
            logger.info(f"Pulse counter: {pulse_counter}")
            measurement = Measurement(
                p0=chan_0.voltage,
                p1=chan_1.voltage,
                p2=chan_2.voltage,
                p3=chan_3.voltage,
                p4=chan_4.voltage,
                p5=chan_5.voltage,
                p6=chan_6.voltage,
                p7=chan_7.voltage,
                p8=None,
                p9=None,
                p10=None,
                p11=None,
                p12=None,
                p13=None,
                p14=None,
                p15=None,
                counter_0=pulse_counter,
                counter_1=None,                 
                date=current_time, 
                device=device)
            session.add(measurement)
            session.commit()

            data = {
                "device_id": f"{device.name}",
                "p_0": chan_0.voltage,
                "p_1": chan_1.voltage,
                "p_2": chan_2.voltage,
                "p_3": chan_3.voltage,
                "p_4": chan_4.voltage,
                "p_5": chan_5.voltage,
                "p_6": chan_6.voltage,
                "p_7": chan_7.voltage,
                "p_8": None,
                "p_9": None,
                "p_10": None,
                "p_11": None,
                "p_12": None,
                "p_13": None,
                "p_14": None,
                "p_15": None,
                "counter_0": pulse_counter,
                "counter_1": None,
                "edge_time_stamp": f"{current_time}"
            }

            message_queue.put(data)
            increment_measurement_counter()

            device = session.query(Device).filter_by(name="device1").first()
            time.sleep(device.measurement_interval)
        except Exception as e:
            logger.error(f"An error occurred while reading the sensors {e}")    
            continue

