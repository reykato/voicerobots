from flask import Flask
from flask import render_template, request, redirect, jsonify, make_response
from flask_socketio import SocketIO
from motors import Motors

flask_instance = Flask(__name__)
socketio = SocketIO(flask_instance) # define websocket object
motors = Motors(20, 21, 16, 12, 1, 7) # initialize motors with GPIO pin numbers

@flask_instance.route('/control')
def control():
    return render_template('joystick.html')

# called when websocket data is sent from the joystick control page
@socketio.on('json')
def handle_message(json):
    # separate x and y from the json into two variables for easier use
    handle_data(json['x'], json['y'])

def handle_data(x, y):
    '''
    Normalizes x and y from [-100, 100] to the interval [-1, 1],
    then calls `Motors.set_duty_cycle(x, y)` to move the robot

    Parameters:
        - x (int): x position from joystick data
        - y (int): y position from joystick data
    '''
    x = float(x) / 100.0
    y = float(y) / 100.0

    motors.set_duty_cycle(x, y)

# this code is executed when the file is run 
if __name__ == '__main__':
    # socketio.run starts the websocket service and Flask server
    socketio.run(flask_instance, debug=True, host='0.0.0.0')

