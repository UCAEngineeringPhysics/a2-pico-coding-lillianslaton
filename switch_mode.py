# switch_mode.py
# LED fade / constant-on with mode switching using IRQ
# Generated with help from ChatGPT (OpenAI)

from machine import Pin, PWM
import time

# LED PWM SETUP
LED_PIN = 15       # GP15
FREQUENCY = 1000   # 1 kHz PWM

led_pwm = PWM(Pin(LED_PIN))
led_pwm.freq(FREQUENCY)

DUTY_MAX = 65535

# BUTTON SETUP 
BUTTON_PIN = 14    # GP14, wired to 3.3V with internal pull-down

button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)

#  GLOBAL STATE 
mode = 0        # 0 = fade mode, 1 = constant-on
brightness = 0  # current duty value
direction = 1   # 1 = up, -1 = down

last_irq_time = 0
DEBOUNCE_MS = 200

#  FADING TIMING 
# 4 seconds per full cycle (1/4 Hz):
# 2 seconds up, 2 seconds down
FADE_TOTAL_TIME = 4.0
HALF_CYCLE_TIME = FADE_TOTAL_TIME / 2.0   # 2 seconds

STEP_TIME = 0.02                           # 20 ms per step
STEPS_PER_HALF = int(HALF_CYCLE_TIME / STEP_TIME)
STEP_SIZE = DUTY_MAX // STEPS_PER_HALF


#  IRQ HANDLER 
def button_handler(pin):
    global mode, last_irq_time

    now = time.ticks_ms()

    # Debounce
    if time.ticks_diff(now, last_irq_time) < DEBOUNCE_MS:
        return

    last_irq_time = now

    # This handler is called on FALLING edge (button RELEASE)
    mode = 1 - mode   # toggle 0 -> 1, 1 -> 0
    print("IRQ: button released, mode changed to", mode)


# Attach interrupt: trigger when signal goes from 1 -> 0 (release)
button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)


#  MAIN LOOP 
last_step_time = time.ticks_ms()

print("Starting main loop. Initial mode =", mode)

while True:
    now = time.ticks_ms()

    # Update LED only every STEP_TIME milliseconds
    if time.ticks_diff(now, last_step_time) >= int(STEP_TIME * 1000):
        last_step_time = now

        if mode == 0:
            #  MODE 0: FADING 
            brightness += direction * STEP_SIZE

            # Reverse at limits
            if brightness >= DUTY_MAX:
                brightness = DUTY_MAX
                direction = -1
            elif brightness <= 0:
                brightness = 0
                direction = 1

            led_pwm.duty_u16(brightness)

        else:
            #  MODE 1: CONSTANT ON 
            brightness = DUTY_MAX
            led_pwm.duty_u16(brightness)

    # Short sleep 
    time.sleep(0.001)

