from flask import Flask, jsonify, request
import adafruit_pca9685
from busio import I2C
from board import SCL, SDA
from robot.motor import Motor, ENA, ENB, IN1, IN2, IN3, IN4
from robot.elevator import Elevator


app = Flask(__name__)

timestamp = 0


i2c = I2C(SCL, SDA)
pwm_board = adafruit_pca9685.PCA9685(i2c_bus=i2c)
pwm_board.frequency = 1600

MotorA = Motor(ENA, IN1, IN2, pwm_board)
MotorB = Motor(ENB, IN3, IN4, pwm_board)

ElevatorA = Elevator(pwm_board)


@app.route('/')
def index():
    return 'Ok'


@app.route('/motor/move')
def motor_move():
    global timestamp
    left = int(request.args.get("left"))
    right = int(request.args.get("right"))
    l_timestamp = int(request.args.get("timestamp"))

    if timestamp > l_timestamp:
        return "Not ok"
    timestamp = l_timestamp
    MotorA.move(right)
    MotorB.move(left)
    return 'ok'


@app.route('/motor/emergency_stop')
def emergency_stop():
    MotorA.stop(emergency=True)
    MotorB.stop(emergency=True)
    return 'ok'


@app.route('/motor/emergency_clear')
def emergency_clear():
    MotorA.clearEmergency()
    MotorB.clearEmergency()
    return 'ok'


@app.route('/elevator/up')
def elevator_up():
    if ElevatorA.monter():
        return 'ok'
    return "error"


@app.route('/elevator/down')
def elevator_down():
    if ElevatorA.descendre():
        return 'ok'
    return "error"


@app.route('/state')
def state():
    state = {
        'emergency': MotorA.emergency or MotorB.emergency,
        'elevator': ElevatorA.step_counter,
    }
    return jsonify(state)


MotorA.move(0)
MotorB.move(0)
