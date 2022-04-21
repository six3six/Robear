import adafruit_pca9685


ENB = 15
ENA = 10
IN1 = 11
IN2 = 12
IN3 = 13
IN4 = 14


class Motor():
    MAX_POWER = 0xFFFF
    MIN_POWER = 0

    def __init__(self, en: int, in1: int, in2: int, pwm_board: adafruit_pca9685.PCA9685):
        self.en = en
        self.in1 = in1
        self.in2 = in2
        self.emergency = False
        self.pwm_board = pwm_board

    def setState(self, power: int, in1: bool, in2: bool) -> None:
        if self.emergency and power != 0:
            self.stop()
            return
        if power > self.MAX_POWER:
            power = self.MAX_POWER
        self.pwm_board.channels[self.in1].duty_cycle = self.MAX_POWER if in1 else 0
        self.pwm_board.channels[self.in2].duty_cycle = self.MAX_POWER if in2 else 0
        self.pwm_board.channels[self.en].duty_cycle = power

    def getState(self) -> tuple:
        return (self.pwm_board.channels[self.en].duty_cycle,
                False if self.pwm_board.channels[self.in1].duty_cycle == 0 else True,
                False if self.pwm_board.channels[self.in2].duty_cycle == 0 else True)

    def move(self, power: int) -> None:
        if power > 0:
            self.forward(power)
        elif power < 0:
            self.backward(-power)
        else:
            self.stop()

    def forward(self, power: int) -> None:
        self.setState(power, True, False)

    def backward(self, power: int) -> None:
        self.setState(power, False, True)

    def stop(self, emergency=False) -> None:
        if emergency:
            self.emergency = emergency
        self.setState(Motor.MAX_POWER, False, False)

    def clearEmergency(self) -> None:
        self.emergency = False
