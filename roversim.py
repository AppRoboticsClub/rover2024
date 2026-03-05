from flask_socketio import SocketIO
rasp: bool
import motors
try:
    import motors
    rasp = True
    print("Raspberry Pi")
except:
    rasp = False
    print("simulator")

socketio: SocketIO

def init(s: SocketIO):
    global socketio
    socketio = s


def set_motion(movement: dict[str, float]):
    print("MOVE")
    global socketio
    socketio.emit('set-speed', movement)

    if rasp:
#        motors.acc(movement['speed']) # type: ignore
        motors.acc(movement['speed']) # type: ignore
        motors.turn(movement['turn']) # type: ignore
#        motors.stop()
