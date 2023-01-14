# Threads
import threading
import logging

# Game
import time
import keyboard
import random

# Sensors
import odroid_dht11 as dht11
import odroid_wiringpi as wpi

# Matrix
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, LCD_FONT
from luma.core.virtual import viewport


class DHT11Sensor:
    def __init__(self, pin):
        self.pin = pin

    def get_temperature(self):
        instance = dht11.DHT11(self.pin)
        result = instance.read()
        if result.is_valid():
            return result.temperature
        else:
            raise Exception("Invalid temperature reading")

    def get_humidity(self):
        instance = dht11.DHT11(self.pin)
        result = instance.read()
        if result.is_valid():
            return result.humidity
        else:
            raise Exception("Invalid humidity reading")


class Button:
    is_active = False
    interactable_time = 0
    is_pressed = False

    def __init__(self, button_pin, led_pin):
        self.pin = button_pin
        self.led_pin = led_pin

    def get_interactable(self):
        return self.is_active

    def set_interactable(self, state):
        self.is_active = state


# Game IDLE
start_countdown = 3  # countdown before starting the game

# Game PLAY
buttons = [
    Button(1, 0),
    Button(2, 0),
    Button(3, 0),
    Button(4, 0),
    Button(5, 0),
    Button(6, 0),
    Button(7, 0)
]  # Which buttons can be pressed
interactable_buttons = []
start_button_index = 3

game_started = False
button_enable_delay = 1  # How much time before another button will be turned on
button_on_time = 2  # How long a button will be active before turning off
session_duration = 60  # total game session duration
cur_play_duration = 0  # How long the player is already playing this session
score = 0  # Score of the player in this session

# Game RESULTS
result_duration = 10  # How long the result will be shown

# Sensor data
sensor_update_interval = 10  # How often the sensor data will be updated in seconds
temperature_data = 0

# Matrix
serial = None
device = None
virtual = None


def start():
    print("Booting... \n")

    form = "%(asctime)s: %(message)s"
    logging.basicConfig(format=form, level=logging.INFO, datefmt="%H:%M:%S")
    wpi.wiringPiSetup()

    initialize_database()
    initialize_sensors()
    initialize_speakers()
    initialize_matrix()
    check_esp_connection(0)
    check_esp_connection(1)
    print("Initialization success!\n")
    print("---------------------------------\n")

    start_game()


def initialize_database():
    print("Initializing database connection...")
    # TODO: initialize database
    print("RESP: SUCCESS \n")


def initialize_sensors():
    print("Initializing sensors...")
    success = False
    attempt = 0

    while success is False and attempt < 3:
        attempt += 1

        # Initialize humidity sensor
        dht11_sensor = DHT11Sensor(0)
        try:
            dht = dht11_sensor.get_temperature()
            print('DHT11 Sensor: {0}'.format(dht))
        except Exception as e:
            logging.exception(e)
            break

        success = True

    print("RESP: {0} \n".format(success and 'SUCCESS' or 'ERROR'))
    if success is True:
        sensor_data = threading.Thread(target=update_sensor_data, args=(1,))
        sensor_data.start()


def initialize_speakers():
    print("Initialize speakers...")
    # TODO: initialize speakers
    print("RESP: SUCCESS \n")


def initialize_matrix():
    print('Initialize matrix')
    global serial
    global device
    global virtual

    wpi.pinMode(0, wpi.GPIO.OUTPUT)
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=2, block_orientation=90, rotate=0, blocks_arranged_in_reverse_order=True)
    virtual = viewport(device, width=200, height=100)

    print("RESP: SUCCESS \n")


def check_esp_connection(esp):
    print('Check ESP_{0} connection...'.format(esp))
    # TODO: check esp connection
    print("RESP: SUCCESS \n")


def update_sensor_data():
    global temperature_data

    while True:
        print('Updating sensor data')

        # Update temperature
        try:
            dht11_sensor = DHT11Sensor(0)
            temperature_data = dht11_sensor.get_temperature()
            print('Temperature: {0}'.format(temperature_data))
        except Exception as e:
            logging.exception(e)
            temperature_data = -1

        time.sleep(sensor_update_interval)


def check_button_state(button):
    if keyboard.is_pressed(str(button.pin)) and button.is_pressed is False:
        button.is_pressed = True
        return True
    elif keyboard.is_pressed(str(button.pin)) is False and button.is_pressed is True:
        button.is_pressed = False

    return False


def check_input(args):
    global score
    logging.info("Thread %s: INPUT", threading.current_thread().name)

    while True:
        if game_started:
            # Check if the user is pressing an interactable button
            for button in get_interactable_buttons():
                if check_button_state(button):
                    logging.info('Button {0} pressed! SCORED'.format(button.pin))
                    score += 1
                    set_button_state(button, False)

            # Check if the user is pressing a not interactable button
            for button in buttons:
                if check_button_state(button):
                    logging.info('Button {0} pressed! MISSED'.format(button.pin))
                    score -= 1


def start_game():
    print("Starting game logic...\n")

    button_input = threading.Thread(target=check_input, args=(1,))
    button_input.start()

    set_idle_state()


def set_idle_state():
    print("[Game phase: IDLE]")
    play_audio('bg_idle', True)
    print("Press 'p' to start")
    set_play_state()
    # while True:
    #     try:
    #         if keyboard.is_pressed('p'):
    #             set_play_state()
    #             break
    #     except:
    #         break


def start_countdown():
    print('Start countdown')
    for i in range(3, 0, -1):
        set_matrix_text(str(i), False)
        print(i)
        time.sleep(1)

    print('GO!')


def get_interactable_buttons():
    return interactable_buttons


def set_button_state(button, state):
    print('Set button {0} state to {1}'.format(button.pin, state))

    if state:
        button.set_interactable(True)
        buttons.remove(button)
        interactable_buttons.append(button)
    else:
        button.set_interactable(False)
        buttons.append(button)
        interactable_buttons.remove(button)


def set_play_state():
    global cur_play_duration
    global game_started

    print("[Game phase: PLAY]")
    time.sleep(1)
    start_countdown()
    game_started = True

    while True:
        try:
            cur_play_duration += 1
            print("------------")

            # Check if a new button has to be turned on
            if cur_play_duration % button_enable_delay == 0:
                button = random.choice(buttons)
                set_button_state(button, True)

            # Check for all the buttons which are on if they have to be turned off again
            for button in interactable_buttons:
                button.interactable_time += 1

                if button.interactable_time >= button_on_time:
                    set_button_state(button, False)
                    button.interactable_time = 0

            # print('Game: Time left {0}'.format(duration - cur_play_duration))
            if cur_play_duration >= session_duration:
                set_end_state()
                break
            time.sleep(1)
        except:
            break


def set_end_state():
    global cur_play_duration
    global game_started

    print("[Game phase: END]")
    play_audio('bg_end', True)
    print("Score: {0}".format(score))

    cur_play_duration = 0
    game_started = False

    while True:
        time.sleep(result_duration)
        set_idle_state()


def set_matrix_text(text, scrolling):
    print('Set matrix text')
    if scrolling:
        with canvas(virtual) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((3, 3), text, fill="white")

        for offset in range(8):
            virtual.set_position((offset, offset))
            time.sleep(0.1)
    else:
        with canvas(device) as draw:
            text(draw, (4, 0), text, fill="white", font=proportional(LCD_FONT))


def play_audio(name, loop):
    print('Play audio, name: {0}, looping: {1}'.format(name, loop))


start()
