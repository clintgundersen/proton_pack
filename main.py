from time import sleep
from adafruit_servokit import ServoKit

import board
import busio
import adafruit_pca9685

i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)
hat.frequency = 60
led_channel = hat.channels[0]

MAX_BRIGHT = 0xffff

def main():
    print("main starting up")
    led_channel.duty_cycle = 0


if __name__ == '__main__':
    main()
