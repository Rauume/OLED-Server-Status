from machine import Pin, I2C
from utime import sleep
import ssd1306

#Setup Display
i2c = I2C(0, sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128,64,i2c)

display.text('Hello World', 0,0)
display.show()