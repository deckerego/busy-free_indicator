import board
import simpleio
import time
import math
import random
import adafruit_lis3dh
from busio import I2C
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
from neopixel import NeoPixel

# NeoPixels
pixels = NeoPixel(board.NEOPIXEL, 10, brightness=1.0, auto_write=False)

# Light indicator
light = AnalogIn(board.LIGHT)

# Accelerometer
i2c = I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
int1 = DigitalInOut(board.ACCELEROMETER_INTERRUPT)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19, int1=int1)
lis3dh.range = adafruit_lis3dh.RANGE_8_G

# Toggle Switch
switch = DigitalInOut(board.SLIDE_SWITCH)
switch.direction = Direction.INPUT
switch.pull = Pull.UP
switch_state = switch.value

# Button A
button_a = DigitalInOut(board.BUTTON_A)
button_a.direction = Direction.INPUT
button_a.pull = Pull.DOWN
button_a_state = False

# Button B
button_b = DigitalInOut(board.BUTTON_B)
button_b.direction = Direction.INPUT
button_b.pull = Pull.DOWN
button_b_state = False

def elapsed_seconds():
    global last_time_seconds
    current_seconds = time.time()
    elapsed_seconds = current_seconds - last_time_seconds
    last_time_seconds = current_seconds
    return elapsed_seconds

def event_sleep(seconds):
    global timeout_seconds
    check_inputs(seconds)
    time.sleep(seconds)
    if timeout_seconds > 0: timeout_seconds -= elapsed_seconds()

def check_inputs(shake_delay=0.1):
    global switch_state, button_a_state, button_b_state
    global timeout_seconds

    if button_a.value is not button_a_state:
        button_a_state = button_a.value
        if button_a_state: press_a()
    if button_b.value is not button_b_state:
        button_b_state = button_b.value
        if button_b_state: press_b()
    if switch.value is not switch_state:
        switch_state = switch.value
        flip_switch()
    if lis3dh.shake(shake_threshold=15, avg_count=3, total_delay=shake_delay):
        shaken()
    if timeout_seconds < 0: timeout()

def shaken():
    if timeout_seconds > 0:
        timeout()

def press_a():
    global timeout_seconds

    timeout_seconds += SECONDS_PER_CLICK
    if timeout_seconds > SECONDS_PER_CLICK * 10:
        timeout_seconds = SECONDS_PER_CLICK * 10

def press_b():
    global timeout_seconds
    global shader_index
    autoset_brightness()

    if timeout_seconds > 0:
        timeout_seconds -= SECONDS_PER_CLICK
    else:
        shader_index = (shader_index + 1) % len(SHADERS)

def timeout():
    global timeout_seconds
    timeout_seconds = 0
    autoset_brightness()

def flip_switch():
    global power
    autoset_brightness()

    if switch_state:
        power = True
    else:
        if power:
            power = False
            pixels.fill((0, 0, 0))
            pixels.brightness = 0.0
            pixels.show()

def autoset_brightness():
    pixels.brightness = round(simpleio.map_range(light.value, 800, 60000, 5, 100) / 100.0, 2)

def show_timer(shader):
    timeout_segments = 0 if timeout_seconds < 0 else math.ceil(timeout_seconds / SECONDS_PER_CLICK)

    for frame in range(10):
        frame_sleep = shader(frame, timeout_segments)
        pixels.show()
        event_sleep(frame_sleep)

def shader_rotate(frame, timeout_segments):
    gamma_palette = (1, 0.05, 0) if timeout_segments > 0 else (0.05, 0.2, 1)
    for pixel in range(timeout_segments, 10):
        color = 55 + (pixel * 20)
        pixels[(pixel + frame) % 10] = list(map(lambda g: math.ceil(color * g), gamma_palette))
    for pixel in range(timeout_segments):
        pixels[pixel] = (204, 61, 61)
    return 0.05

def shader_breathe(frame, timeout_segments):
    color = (164, 12, 0) if timeout_segments > 0 else (8, 16, 128)
    idx = frame if frame < 5 else frame - ((frame - 5) << 1)
    gamma = LOG_10[idx] + 0.08

    for pixel in range(timeout_segments, 10):
        pixels[pixel] = list(map(lambda c: math.ceil(gamma * c), color))
    for pixel in range(timeout_segments):
        pixels[pixel] = (204, 61, 61)
    return 0.1

def shader_sparkle(frame, timeout_segments):
    for pixel in range(timeout_segments, 10):
        gamma_palette = (1, 0.05, 0) if timeout_segments > 0 else (round(random.random(), 2) / 3, round(random.random(), 2), 1.0)
        color = 15 + ((pixel & 3) * 80)
        pixels[random.randrange(10)] = list(map(lambda g: math.ceil(color * g), gamma_palette))
    for pixel in range(timeout_segments):
        pixels[pixel] = (204, 61, 61)
    return 0.05

def shader_rainbow(frame, timeout_segments):
    for pixel in range(timeout_segments, 10):
        if timeout_segments > 0:
            color = 55 + (pixel * 20)
            pixels[(pixel + frame) % 10] = list(map(lambda g: math.ceil(color * g), (1, 0.05, 0)))
        else:
            color = (0, 0, 0)
            base = (pixel % 3) * 60
            if pixel <= 2 or pixel == 9: color = (100 - int(base / 2), base, 0)
            elif pixel <= 5: color = (0, 200 - base, base)
            else: color = (base, 0, 200 - base)
            pixels[(pixel + frame) % 10] = color
    for pixel in range(timeout_segments):
        pixels[pixel] = (204, 61, 61)
    return 0.05

def shader_firework(frame, timeout_segments):
    color1 = (0, 0, 0)
    color2 = (0, 0, 0)

    if timeout_segments <= 0:
        color1 = (random.randrange(64), random.randrange(96), random.randrange(160))
        color2 = (random.randrange(64), random.randrange(96), random.randrange(160))
    else:
        color1 = (64 + random.randrange(164), random.randrange(24), random.randrange(64))
        color2 = (64 + random.randrange(164), random.randrange(24), random.randrange(64))

    if frame % 2 is 0:
        for pixel in range(timeout_segments, 10):
            if timeout_segments > 0 or frame > 2:
                gamma = 1 - LOG_10[frame - 1]
                color = color1 if pixel % 2 is 0 else color2
                pixels[pixel] = list(map(lambda c: math.ceil(gamma * c), color))
            else:
                pixels[pixel] = (0, 0, 0)
        for pixel in range(timeout_segments):
            pixels[pixel] = (248, 0, 0)
    return 0.05

# Constants
SECONDS_PER_CLICK = 900
LOG_10 = [0.0, 0.3010, 0.4771, 0.6021, 0.6990, 0.7782, 0.8451, 0.9031, 0.9542, 1.0]
SHADERS = [shader_rotate, shader_breathe, shader_sparkle, shader_rainbow, shader_firework]

# Default state
power = switch_state
last_time_seconds = time.time()
timeout_seconds = 0
shader_index = 0
autoset_brightness()

while True:
    if power:
        show_timer(SHADERS[shader_index])
    else:
        event_sleep(1.0)
