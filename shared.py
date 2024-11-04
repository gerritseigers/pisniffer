send_counter = 0
measurement_counter = 0

def increment_measurement_counter():
    global measurement_counter
    measurement_counter += 1

def increment_send_counter():
    global send_counter
    send_counter += 1

def get_send_counter():
    global send_counter
    return send_counter    

def get_measurement_counter():
    global measurement_counter
    return measurement_counter