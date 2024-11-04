import random
from logger_config import logger
from session_config import session
from models.model import Device, Measurement
import datetime
import time
from shared import measurement_counter, increment_measurement_counter

def read_sensors(message_queue):

    logger.info("Starting the data generation loop...")
    device = session.query(Device).first()
    global measurement_counter  # Ensure the counter is global

    while True:
        try:
            temperature = random.randint(20, 50)
            logger.info(f"Temperature: {temperature}")

            # Add the measurement to the database
            current_time = datetime.datetime.now()

            measurement = Measurement(
                value=temperature, 
                date=current_time, 
                device=device)
            session.add(measurement)
            session.commit()

            data = {
                "device_id": f"{device.name}",
                "temperature": temperature,
                "edge_time_stamp": f"{current_time}"
            }

            message_queue.put(data)
            increment_measurement_counter()

            device = session.query(Device).filter_by(name="device1").first()
            time.sleep(device.measurement_interval)
        except Exception as e:
            logger.error(f"An error occurred while reading the sensors {e}")    
            continue

