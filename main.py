from azure.iot.device.aio import IoTHubDeviceClient
from logger_config import logger
from session_config import session
from measurement.measurement import read_sensors
from models.model import Device
from models.seed_database import seed_database
from flask import Flask
from flask_bootstrap import Bootstrap, Bootstrap5
from controllers.controllers import controllers
from shared import measurement_counter, increment_measurement_counter  # Import the shared variable and function
import time
import json
import asyncio
import threading
import queue

# Define connection string
connectionString = (
    "HostName=gs-demo-iothub.azure-devices.net;DeviceId=device1;SharedAccessKey=qTh81ZkJbgyLvbkcaWPpdGX6QR4neloJqOTdnsXho3g="
)
message_queue = queue.Queue()

app = Flask(__name__)
Bootstrap5(app)
app.register_blueprint(controllers)


@app.context_processor
def inject_measurement_counter():
    return dict(measurement_counter=measurement_counter)

def run_flask_app():
    app.run(host='0.0.0.0', port=5000)

def start_measurement_thread():
    global data_thread

    data_thread = threading.Thread(target=read_sensors, args=(message_queue,))
    data_thread.daemon = True 
    data_thread.start()

def start_flask_thread():

    global flask_thread

    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True 
    flask_thread.start()    

async def sendToIotHub(data):
    try:

        # Create an instance of the IoT Hub Client class
        device_client = IoTHubDeviceClient.create_from_connection_string(
            connectionString
        )

        # Connect the device client
        await device_client.connect()

        # Send the message
        await device_client.send_message(data)
        print("Message sent to IoT Hub:", data)

        # Shutdown the client
        await device_client.shutdown()
            
    except Exception as e:
        logger.error(f"An error occurred while sending the message to IoT Hub {e}")


def main():

    start_measurement_thread()
    start_flask_thread()

    # Run an infinite while loop to send data every 5 seconds
    logger.info("Starting the data generation loop...")

    logger.info("Seeding database if necessary...")
    if session.query(Device).count() == 0:
        logger.info("Seeding the database")
        seed_database()

    device = session.query(Device).filter_by(name="device1").first()

    while True:
        if not message_queue.empty():
            logger.warning("Sending data to IoT Hub")
            while not message_queue.empty():
                data = message_queue.get()
                asyncio.run(sendToIotHub(data=json.dumps(data)))

        if not data_thread.is_alive():
            logger.error("Data thread has stopped. Restarting...")
            start_measurement_thread()

        if not flask_thread.is_alive():
            logger.error("Flask thread has stopped. Restarting...")
            start_flask_thread()

        device = session.query(Device).filter_by(name="device1").first()
        time.sleep(device.send_interval)

if __name__ == '__main__':
    main()
