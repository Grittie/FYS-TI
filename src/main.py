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
temperature_data = 0


def start():
    print("Booting... \n")
    wpi.wiringPiSetup()

    initialize_database()
    initialize_sensors()
    initialize_speakers()
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
        except:
            print('DHT11: ERROR')
            break

        success = True

    print("RESP: {0} \n".format(success and 'SUCCESS' or 'ERROR'))


def initialize_speakers():
    print("Initialize speakers...")
    # TODO: initialize speakers
    print("RESP: SUCCESS \n")


def check_esp_connection(esp):
    print('Check ESP_{0} connection...'.format(esp))
    # TODO: check esp connection
    print("RESP: SUCCESS \n")


def update_sensor_data():
    global temperature_data
    dht11_sensor = DHT11Sensor(0)

    print('Updating sensor data')
    temperature_data = dht11_sensor.get_temperature()


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

    form = "%(asctime)s: %(message)s"
    logging.basicConfig(format=form, level=logging.INFO, datefmt="%H:%M:%S")
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


def queue_matrix_text(text):
    print('Queue matrix text: {0}'.format(text))


def set_matrix_text():
    # TODO: Play all the queued text
    print('Set matrix text')


def play_audio(name, loop):
    print('Play audio, name: {0}, looping: {1}'.format(name, loop))


start()
