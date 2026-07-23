import machine
import neopixel
import time

# ---------------- Configuration ----------------
PIN = 26
NUM_LEDS = 21

BRIGHTNESS = 1      # 0.0 - 1.0
FRAME_DELAY = 20       # milliseconds
RAINBOW_SCALE = 5     # Larger = tighter rainbow bands
ANGLE = -20            # Direction of rainbow in degrees
# ------------------------------------------------

pin = machine.Pin(PIN, machine.Pin.OUT)
leds = neopixel.NeoPixel(pin, NUM_LEDS)

# -------------------------------------------------------------------
# Approximate physical LED coordinates (taken from PCB layout)
#
# Wiring order:
# LA2 LA1
# LB4 LB3 LB2 LB1
# LC4 LC3 LC2 LC1
# LD4 LD3 LD2 LD1
# LE2 LE1
# RB3 RB2 RB1
# RA2 RA1
#
# X increases left->right
# Y increases top->bottom
# -------------------------------------------------------------------

LED_POSITIONS = [
    (95, 125),   # LA2
    (35, 125),   # LA1

    (210, 235),  # LB4
    (150, 235),  # LB3
    (90, 235),   # LB2
    (30, 235),   # LB1

    (210, 355),  # LC4
    (150, 355),  # LC3
    (90, 355),   # LC2
    (30, 355),   # LC1

    (210, 475),  # LD4
    (150, 475),  # LD3
    (90, 475),   # LD2
    (30, 475),   # LD1

    (95, 595),   # LE2
    (35, 595),   # LE1

    (620, 235),  # RB3
    (560, 235),  # RB2
    (500, 235),  # RB1

    (560, 125),  # RA2
    (500, 125),  # RA1
]

# ------------------------------------------------


def wheel(pos):
    pos &= 255

    if pos < 85:
        return (
            255 - pos * 3,
            pos * 3,
            0
        )

    if pos < 170:
        pos -= 85
        return (
            0,
            255 - pos * 3,
            pos * 3
        )

    pos -= 170
    return (
        pos * 3,
        0,
        255 - pos * 3
    )


def scale(color, brightness):
    return (
        int(color[0] * brightness),
        int(color[1] * brightness),
        int(color[2] * brightness)
    )


# Precompute direction vector
theta = ANGLE * 3.14159265 / 180
dx = __import__("math").cos(theta)
dy = __import__("math").sin(theta)

offset = 0

while True:

    for i, (x, y) in enumerate(LED_POSITIONS):

        # Project coordinate onto rainbow direction.
        # This creates a smooth wave across the actual keyboard.
        position = x * dx + y * dy

        color_index = int(position / RAINBOW_SCALE + offset) & 255

        leds[i] = scale(wheel(color_index), BRIGHTNESS)

    leds.write()

    offset = (offset + 1) & 255

    time.sleep_ms(FRAME_DELAY)