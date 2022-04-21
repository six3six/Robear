#!/usr/bin/env python
# -*- coding: utf-8 -*-

# libraries
import time
import adafruit_pca9685


class Elevator():
    STEP_PINS = [4, 5, 6, 7]
    # Define time delay between steps
    wait_time = 0.00009  # set speed

    MAX_STEPS = 34816*2

    step_counter = 0 #MAX_STEPS

    used = False

    # Define advanced half-step sequence
    STEP_COUNT = 8
    Seq = []
    Seq = [i for i in range(0, STEP_COUNT)]
    Seq[0] = [1, 0, 0, 0]
    Seq[1] = [1, 1, 0, 0]
    Seq[2] = [0, 1, 0, 0]
    Seq[3] = [0, 1, 1, 0]
    Seq[4] = [0, 0, 1, 0]
    Seq[5] = [0, 0, 1, 1]
    Seq[6] = [0, 0, 0, 1]
    Seq[7] = [1, 0, 0, 1]

    def __init__(self, pwm_board: adafruit_pca9685.PCA9685):
        self.pwm_board = pwm_board

    # Choose a sequence to use
    Seq = Seq
    STEP_COUNT = STEP_COUNT

    def _activePin(self, pin: int, active: bool):
        self.pwm_board.channels[pin].duty_cycle = 0xFFFF if active else 0

    def step(self, forward: bool):
        for pin in range(4):
            xpin = self.STEP_PINS[pin]
            if self.Seq[self.step_counter % self.STEP_COUNT][pin] != 0:
                self._activePin(xpin, True)
            else:
                self._activePin(xpin, False)
        self.step_counter = self.step_counter + (1 if forward else -1)

    def steps(self, nb: int) -> bool:
        if self.used is True:
            return False
        self.used = True
        print("nbsteps {}".format(nb))
        for i in range(abs(nb)):
            self.step(nb > 0)
            # If we reach the end of the sequence
            # start again
            # Wait before moving on
            time.sleep(self.wait_time)
        self.used = False
        return True

    def goTo(self, step: int) -> bool:
        return self.steps(step - self.step_counter)

    def monter(self) -> bool:
        # parcourt un tour dans le sens horaire
        return self.goTo(0)

    def descendre(self) -> bool:
        # parcourt un tour dans le sens horaire
        return self.goTo(self.MAX_STEPS)
