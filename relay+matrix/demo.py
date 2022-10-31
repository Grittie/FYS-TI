import odroid_wiringpi as wpi
import time

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, LCD_FONT

wpi.wiringPiSetup()
wpi.pinMode(0, wpi.GPIO.OUTPUT)

serial = spi(port = 0, device = 0, gpio = noop())
device = max7219(serial, cascaded = 2, block_orientation = 90, 
                 rotate = 0, blocks_arranged_in_reverse_order= True)

print("Matrix / Relay demo")
while True:
    wpi.digitalWrite(0, 1)
    with canvas(device) as draw:
        text(draw, (4, 0), "+1", fill="white", font=proportional(LCD_FONT))
    print("Mole raised!")
    time.sleep(0.75)
    wpi.digitalWrite(0, 0)
    print("Mole whacked!")
    show_message(device, "BONK!", fill="white", font=proportional(LCD_FONT))
    time.sleep(1)