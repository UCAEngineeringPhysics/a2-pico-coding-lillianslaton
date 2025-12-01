# fade_in_fade_out.py
# Helped by ChatGPT (OpenAI).

from machine import Pin, PWM
import time


LED_PIN = 15   


FREQUENCY = 1000  # 1 kHz PWM

led_pwm = PWM(Pin(LED_PIN))
led_pwm.freq(FREQUENCY)

# Max duty cycle value in MicroPython (0..65535)
DUTY_MAX = 65535

#  Timing parameters 
# Ramp up in 2 seconds
# Ramp down in 1 second

STEP_TIME_UP = 0.01     # 10 ms between changes while ramping up
STEP_TIME_DOWN = 0.01   # 10 ms between changes while ramping down

STEPS_UP = int(2.0 / STEP_TIME_UP)       # number of steps in 2 seconds
STEPS_DOWN = int(1.0 / STEP_TIME_DOWN)   # number of steps in 1 second

# how much the duty changes each step
STEP_SIZE_UP = DUTY_MAX // STEPS_UP
STEP_SIZE_DOWN = DUTY_MAX // STEPS_DOWN

while True:
    # Fade IN: 0 -> DUTY_MAX in 2 seconds 
    duty = 0
    for _ in range(STEPS_UP):
        led_pwm.duty_u16(duty)
        duty += STEP_SIZE_UP
        if duty > DUTY_MAX:
            duty = DUTY_MAX
        time.sleep(STEP_TIME_UP)

    # Fade OUT: DUTY_MAX -> 0 in 1 second 
    duty = DUTY_MAX
    for _ in range(STEPS_DOWN):
        led_pwm.duty_u16(duty)
        duty -= STEP_SIZE_DOWN
        if duty < 0:
            duty = 0
        time.sleep(STEP_TIME_DOWN)

