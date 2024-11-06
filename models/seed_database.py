from models.model import Device
from session_config import session


def seed_database():
    device = Device(
        name="device1",
        token="qTh81ZkJbgyLvbkcaWPpdGX6QR4neloJqOTdnsXho3g=",
        endpoint="gs-demo-iothub.azure-devices.net",
        location="room1",
        measurement_interval=2,
        send_interval=10)
    session.add(device)
    session.commit()
