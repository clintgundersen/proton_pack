from time import sleep
import board
import busio
import adafruit_pca9685
import RPi.GPIO as GPIO

# GPIO.setmode(GPIO.BOARD)
import threading
import multiprocessing

# --------------------------------------------------
#
#       Pi networking info:
#       router dhcp assigning 192.168.1.179 to the
#       pi wifi dongle
#       username: ecto
#       pass: test
#
# ---------------------------------------------------

from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

i2c = busio.I2C(board.SCL, board.SDA)
controler = adafruit_pca9685.PCA9685(i2c)
controler.frequency = 60

MAX_BRIGHT = 65535  # 0xffff
TOTAL_CHANNELS = 16

bright_vals = []

button_gpio_pin = 19

GPIO.setup(button_gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def init_channels():
    for i in range(TOTAL_CHANNELS):
        print(f'initializing: {i}')
        controler.channels[i].duty_cycle = 0

    for val in range(0, 101):
        bright = int((MAX_BRIGHT * val) / 100)
        print(f'adding {bright} to vals')
        bright_vals.append(bright)

    print(len(bright_vals))


# def cycle_cyclotron():
#     # 0 = greens
#     # 1 = brown
#     # 2 = orange
#     # 3 = blue
#
#     cyclotron = [controler.channels[8],
#                  controler.channels[9],
#                  controler.channels[10],
#                  controler.channels[11]
#                  ]
#
#     while True:
#         for led in cyclotron:
#             print(f'cycling {cyclotron.index(led)}')
#             for i in bright_vals:
#                 led.duty_cycle = i
#                 sleep(.004)
#             for i in reversed(bright_vals):
#                 led.duty_cycle = i
#                 sleep(.001)
#             led.duty_cycle = 0


# def blink_trap():
#     trap_led = controler.channels[12]
#
#     while True:
#         trap_led.duty_cycle = 0
#         sleep(.3)
#         trap_led.duty_cycle = MAX_BRIGHT
#         print('blinking the trap')


# def run_neutrona_wand():
#     throw_lights = [controler.channels[13]]
#
#     while True:
#         for led in run_lights:
#             led.duty_cycle = 0
#             sleep(.5)
#             led.duty_cycle = MAX_BRIGHT
#         print('blinking the wand')
#
#     # todo figure out the throwing and the switch


# def cycle_power_cell():
#     cells = [controler.channels[0], controler.channels[1], controler.channels[2], controler.channels[3],
#              controler.channels[4], controler.channels[5], controler.channels[6], controler.channels[7]]
#
#     cells[0].duty_cycle = MAX_BRIGHT
#     sleep_length = .08
#     while True:
#         for i in range(1, len(cells)):
#             print(f'powering cell {i}')
#             cells[i].duty_cycle = MAX_BRIGHT
#             sleep(sleep_length)
#         for i in range(1, len(cells)):
#             print('clearing cells')
#             cells[i].duty_cycle = 0
#         sleep(sleep_length)


# def light_0_on():
#     print('old way')
#     controler.channels[1].duty_cycle = MAX_BRIGHT

def test_cycle():
    for i in range(TOTAL_CHANNELS):
        controler.channels[i].duty_cycle = int(MAX_BRIGHT / 2)


def compromise():
    trap = controler.channels[12]
    bottom_cell = controler.channels[0]
    cells = [controler.channels[1], controler.channels[2], controler.channels[3],
             controler.channels[4], controler.channels[5], controler.channels[6], controler.channels[7]]
    cyclotron = [controler.channels[8],
                 controler.channels[9],
                 controler.channels[10],
                 controler.channels[11]
                 ]

    max_cycles = 20
    trap_cycles = 0
    trap_state = False
    max_trap_cycles = 20
    max_cell_cycles = 10
    current_cyclotron = 0
    bright = 0
    increment_up = int(MAX_BRIGHT / max_cycles)
    increment_down = int(MAX_BRIGHT / (max_cycles / 2))
    cyclotron_state = 1

    print('starting the base cell')
    bottom_cell.duty_cycle = MAX_BRIGHT
    cell_cycle = 0
    cell_index = 0

    while True:

        # print('-----------------------')
        # print('new loop')
        # toggle trap
        if trap_cycles > max_trap_cycles:
            trap_cycles = 0
            trap_state = not trap_state
            # print(f'toggling the trap to {trap_state}')
            if trap_state:
                trap.duty_cycle = MAX_BRIGHT
            else:
                trap.duty_cycle = 0
        else:
            trap_cycles += 1
            # print(trap_cycles)

        # take 4 cycles to iterate to max brightness
        cyclo = cyclotron[current_cyclotron]

        if bright == 0:
            print(f'cyclo done, clearing {current_cyclotron} rotating cyclo')
            cyclo.duty_cycle = 0
            current_cyclotron = current_cyclotron + 1
            if current_cyclotron > len(cyclotron) - 1:
                current_cyclotron = 0

        if cyclotron_state == 1:
            bright = bright + increment_up
        else:
            bright = bright - increment_down

        if bright > MAX_BRIGHT:
            bright = MAX_BRIGHT
        if bright < 0:
            bright = 0

        cyclo.duty_cycle = bright

        if bright == MAX_BRIGHT:
            cyclotron_state = 0
        if bright == 0:
            cyclotron_state = 1

        # take 2 cycles to light up another cell
        if cell_cycle == max_cell_cycles:
            cell_cycle = 0
            # print(f'iterating cells: {cell_index}')
            if cell_index > len(cells) - 1:
                cell_index = 0
                print('clearing cells')
                for i in cells:
                    i.duty_cycle = 0
            else:
                # print(f'lighting a cell {cell_index}')
                cells[cell_index].duty_cycle = MAX_BRIGHT
                cell_index = cell_index + 1
        else:
            # print('waiting for next cell cycle')
            cell_cycle = cell_cycle + 1

        sleep(.005)


def button():
    while True:
        button_state = GPIO.input(button_gpio_pin)

        if button_state == False:
            print('Button state is False')
        # else:
        #     print('Button state is True')


def main():

    #todo red wire broken, probably at solder point to led
    #todo rewire red and white wand lighs to be on the same channel
    #todo rewire wand barrel white light to take the now open channel
    #todo switch wires are wired incorreclty, neitehr are going to 3v power
    #todo one needs to be
    #todo then add code to control switch

    print("main starting up")
    init_channels()
    compromise()
    # button()
    # test_cycle()


if __name__ == '__main__':
    main()
