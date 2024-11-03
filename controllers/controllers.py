from flask import Blueprint, jsonify, render_template_string, render_template
from flask import redirect, url_for
from flask import request

from models.model import Device
from logger_config import logger
from session_config import session

# Create a Blueprint for the controllers
controllers = Blueprint('controllers', __name__)

@controllers.route('/')
def home():
    try:
        return render_template('home.html')
    except Exception as e:
        logger.error(f"An error occurred while rendering the home page {e}")
        return jsonify({"message": "An error occurred while rendering the home page"})

# @controllers.route('/')
# def home():
#     # HTML template with an Edit button
#     html = '''
#     <html>
#         <body>
#             <h1>Welcome to the IoT Hub!</h1>
#             <button onclick="location.href='/edit_device'" type="button">Edit</button>
#         </body>
#     </html>
#     '''
#     return render_template_string(html)

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