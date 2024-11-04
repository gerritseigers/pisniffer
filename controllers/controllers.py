from flask import Blueprint, jsonify, render_template_string, render_template
from flask import redirect, url_for
from flask import request

from models.model import Device, Measurement
from logger_config import logger, LogRecord
from session_config import session
from shared import get_send_counter, get_measurement_counter    


# Create a Blueprint for the controllers
controllers = Blueprint('controllers', __name__)

@controllers.route('/')
def home():
    try:
        return render_template('home.html')
    except Exception as e:
        logger.error(f"An error occurred while rendering the home page {e}")
        return jsonify({"message": "An error occurred while rendering the home page"})


@controllers.route('/edit_device', methods=['GET', 'POST'])
def edit_device():
    device = session.query(Device).filter_by(name="device1").first()
    if request.method == 'POST':
        device.name = request.form['new_name']
        device.token = request.form['new_token']
        device.measurement_interval = request.form['new_measurement_interval']
        device.send_interval = request.form['new_send_interval']
        session.commit()
        return redirect(url_for('controllers.home'))
    return render_template('edit_device.html', device=device)

@controllers.route('/get_counters', methods=['GET'])
def get_counters():
    try:
        device = session.query(Device).filter_by(name="device1").first()
        total_measurements = session.query(Measurement).count()
        total_errors = session.query(LogRecord).filter_by(level="ERROR").count()
        total_fatals = session.query(LogRecord).filter_by(level="CRITICAL").count()
        total_warnings = session.query(LogRecord).filter_by(level="WARNING").count()
        data = {
            "device_name": device.name,
            "send_interval": device.send_interval,
            "measurement_interval": device.measurement_interval,
            "send_counter": get_send_counter(),
            "measurement_counter": get_measurement_counter(),
            "total_errors": total_errors,
            "total_fatals": total_fatals,
            "total_warnings": total_warnings,
            "total_measurements": total_measurements,
        }
        return jsonify(data)
    except Exception as e:
        logger.error(f"An error occurred while fetching the counters {e}")
        return jsonify({"message": "An error occurred while fetching the counters"}), 500