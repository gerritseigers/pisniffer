import random
from logger_config import logger
from session_config import session
from models.model import Device, Measurement
import datetime
import time


def read_sensors(message_queue):

    logger.info("Starting the data generation loop...")
    device = session.query(Device).filter_by(name="device1").first()

    while True:
        temperature = random.randint(20, 50)
        logger.error(f"Temperature: {temperature}")

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

        device = session.query(Device).filter_by(name="device1").first()
        time.sleep(device.measurement_interval)
