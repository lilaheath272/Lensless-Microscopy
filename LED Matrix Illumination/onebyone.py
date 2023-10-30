
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from time import sleep

# Initialize the MAX7219 LED matrix
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1, block_orientation=90, rotate=0)

# Number of rows and columns in the matrix
matrix_rows = 8
matrix_cols = 8

try:
    for x in range(matrix_cols):
        for y in range(matrix_rows):
            with canvas(device) as draw:
                draw.point((x, y), fill="white")  # Turn on the current LED

            # Sleep to control the timing of LED activation
            sleep(10)  # Adjust this value to control the speed

            with canvas(device) as draw:
                draw.point((x, y), fill="black")  # Turn off the current LED

except KeyboardInterrupt:
    pass

device.cleanup()

