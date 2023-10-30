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
    for i in range(min(matrix_rows, matrix_cols) // 2 + 1):
        for x in range(i, matrix_cols - i):
            for y in range(i, matrix_rows - i):
                with canvas(device) as draw:
                    draw.point((x, y), fill="white")  # Turn on the current LED

                # Sleep to control the timing of LED activation
                sleep(0.1)  # Adjust this value to control the speed

except KeyboardInterrupt:
    pass

device.cleanup()


