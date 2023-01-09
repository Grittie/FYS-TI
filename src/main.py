## Whack a mole game
import time

import keyboard

## Game variables
start_countdown = 3

duration = 60
cur_play_duration = 0
score = 0

result_duration = 10


def start():
    print("Booting... \n")

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
    # TODO: initialize sensors
    print("RESP: SUCCESS \n")


def initialize_speakers():
    print("Initialize speakers...")
    # TODO: initialize speakers
    print("RESP: SUCCESS \n")


def check_esp_connection(esp):
    print('Check ESP_{0} connection...'.format(esp))
    # TODO: check esp connection
    print("RESP: SUCCESS \n")


def start_game():
    print("Starting game logic...\n")
    set_idle_state()


def set_idle_state():
    print("[Game phase: IDLE]")
    play_audio('bg_idle', True)
    print("Press 's' to start")

    while True:
        try:
            if keyboard.is_pressed('s'):
                set_play_state()
                break
        except:
            break


def set_play_state():
    global cur_play_duration

    print("[Game phase: PLAY]")
    time.sleep(1)
    start_countdown()

    while True:
        try:
            cur_play_duration += 1
            if cur_play_duration >= duration:
                print('Game: Time left {0}'.format(duration - cur_play_duration))
                set_end_state()
                break
            time.sleep(1)
        except:
            break


def set_end_state():
    print("[Game phase: END]")
    play_audio('bg_end', True)
    print("Score: {0}".format(score))

    while True:
        time.sleep(result_duration)
        set_idle_state()

def start_countdown():
    print('Start countdown')
    for i in range(start_countdown, 0, -1):
        print(i)
        time.sleep(1)

    print('GO!')


def queue_matrix_text(text):
    print('Queue matrix text: {0}'.format(text))


def set_matrix_text():
    # TODO: Play all the queued text
    print('Set matrix text')


def play_audio(name, loop):
    print('Play audio, name: {0}, looping: {1}'.format(name, loop))


start()
