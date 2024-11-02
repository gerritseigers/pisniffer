from flask import Blueprint, jsonify, render_template_string
from flask import request

from models.model import Device
from logger_config import logger
from session_config import session

# Create a Blueprint for the controllers
controllers = Blueprint('controllers', __name__)


@controllers.route('/')
def home():
    # HTML template with an Edit button
    html = '''
    <html>
        <body>
            <h1>Welcome to the IoT Hub!</h1>
            <button onclick="location.href='/edit_device'" type="button">Edit</button>
        </body>
    </html>
    '''
    return render_template_string(html)

@controllers.route('/edit_device', methods=['GET', 'POST'])
def edit_device():

    device = session.query(Device).filter_by(name="device1").first()

    if request.method == 'POST':
        # Handle the form submission to edit the device
        name = request.form['new_name']
        token = request.form['new_token']
        measurement_interval = request.form['new_measurement_interval']
        send_interval = request.form['new_send_interval']

        device.name = name
        device.token = token
        device.measurement_interval = measurement_interval
        device.send_interval = send_interval

        # Update the device in the database (implement your logic here)
        # ...
        return jsonify({"message": "Device updated successfully"})
    else:
        # Render the edit device form
        html = f'''
        <html>
            <body>
            <h1>Edit Device</h1>
            <form method="post">
                <label for="new_name">Device name:</label><br>
                <input type="text" id="new_name" name="new_name" value="{device.name}"><br><br>
                <label for="new_token">Token:</label><br>
                <input type="text" id="new_token" name="new_token" value="{device.token}"><br><br>
                <label for="new_measurement_interval">Measurement interval:</label><br>
                <input type="text" id="new_measurement_interval" name="new_measurement_interval" value="{device.measurement_interval}"><br><br>
                <label for="new_send_interval">Send interval:</label><br>
                <input type="text" id="new_send_interval" name="new_send_interval" value="{device.send_interval}"><br><br>
                <input type="submit" value="Submit">
            </form>
            </body>
        </html>
        '''
        return render_template_string(html)

