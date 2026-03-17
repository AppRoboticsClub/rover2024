from flask import Flask, render_template
from flask_socketio import SocketIO
# Following two imports are just for more
#   informative debug prints with timestamps
from datetime import datetime
from zoneinfo import ZoneInfo

import motors

# Declare a global motion dictionary to keep track
#   of the current speed and turning value of the rover
#   at any given moment.
motion: dict[str, float] = {
    'speed': 0,
    'turn': 0
}


"""
Create the Flask webapp and use the SocketIO
  extension to handle use pressing keys.
"""
app = Flask(__name__)
socketio = SocketIO(app)

"""
Displays the main page
  - Flask will only search in the `templates` directory
      for anything passed to `render_template(...)`
"""
@app.route('/')
def index():
    return render_template('index.html')

"""
Handle any key being pressed
"""
@socketio.on('key-down')
def handle_key(data, m = 1):
    prev = motion.copy()
    if data == 'w':
        motion['speed'] = m
    if data == 's':
        motion['speed'] = -m
    if data == 'a':
        motion['turn'] = -m
    if data == 'd':
        motion['turn'] = m

    # Check if the motion was changed so we don't print
    #   any extra debug info while a key is being pressed.
    if motion != prev:
        timestamp = datetime.now(ZoneInfo("America/New_York")).strftime("%H:%M:%S.%f")
        action = "press" if m else "release"
        print(f"{timestamp} {f'[{action}]':9s} `{data}` | speed ={motion['speed']:>5.2f}  turn ={motion['turn']:>5.2f}    ")#, end='\r', flush=True)

        motors.move(motion['speed'], motion['turn'])

        socketio.emit('set-speed', motion)

"""
Handle any key being released
"""
@socketio.on('key-up')
def handle_key_up(data):
    handle_key(data, 0)

"""
Asks SocketIO to run the Flask webapp when this
  file (main.py) is run by python: `python main.py`
"""
if __name__ == '__main__':
    """
    `host="0.0.0.0"` Makes the Flask webapp available to the entire
      network, aka the hotspot that this pi is running.
    `debug=False` Disables the Flask debugger, which is a critical
       security vulnerability and allows for arbitrary code execution.
       This is still useful for development, but shouldn't be sent to the rover enabled.
    `port=5001` Tells Flask to host the webapp on port 5001 instead of the default
       of 5000 since that port is reserved by Apple devices for AirPlay.
    """
    socketio.run(app, debug=False, host="0.0.0.0", port=5001)
    # TODO: Make sure to turn off the debug flag.
