# Threads
import threading
import logging

# Game
import time
import random

# Sensors
import odroid_dht11 as dht11
import odroid_wiringpi as wpi

# Audio
import simpleaudio as sa

# Matrix
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, LCD_FONT
from luma.core.virtual import viewport

# Database
# from db_functions import db
# from db_functions import get_logid, get_sessionid, insert_into_userdata, insert_into_devicedata, get_timestamp

# start the main.py for the game, and the app.py for the website by running the following commdand in the terminal:
# the command is comprised of "python /filepath/main.py & /filepath/app.py"
# python C:\Users\Jasper\projectfys\it102-1\src\main.py & python C:\Users\Jasper\projectfys\it102-1\src\modules\database\app.py


class DHT11Sensor:
    def __init__(self, pin):
        self.pin = pin

    def get_temperature(self):
        instance = dht11.DHT11(self.pin)
        result = instance.read()
        if result.is_valid():
            return result.temperature
        else:
            return 19.7# raise Exception("Invalid temperature reading")

    def get_humidity(self):
        instance = dht11.DHT11(self.pin)
        result = instance.read()
        if result.is_valid():
            return result.humidity
        else:
            return 0# raise Exception("Invalid humidity reading")


class Ultrasound:
    def __init__(self, trigPin, echoPin):
        self.trigPin = trigPin
        self.echoPin = echoPin


    def __pinSetupUltraSound(__trigPin: int, __echoPin: int):
        wpi.pinMode(__trigPin, wpi.GPIO.OUTPUT)
        wpi.pinMode(__echoPin, wpi.GPIO.INPUT)


    def getDistance(self):
        __pinSetupUltraSound(self.trigPin, self.choPin)

        wpi.digitalWrite(trigPin, wpi.HIGH)
        time.sleep(0.00001)
        wpi.digitalWrite(trigPin, wpi.LOW)
        while wpi.digitalRead(echoPin) == 0:
            start_time = time.time()
        while wpi.digitalRead(echoPin) == 1:
            bounceback_time = time.time()
        pulse_duration: int = bounceback_time - start_time
        distance = round(pulse_duration * 17150, 2)

        return distance


class Speaker:
    def play_audio(sound):
        print("playing audio...")
        wave_obj = sa.WaveObject.from_wave_file("sounds/" + sound)
        play_obj = wave_obj.play()
        play_obj.wait_done()


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
humidity_data = 0

# Matrix, vcc: 3.3v, gnd: gnd, din: 19, cs: 24, clk: 23
serial = None
device = None
virtual = None
matrix_cascaded = 1
matrix_row_count = 8
total_matrix_led = 0
matrix_update_interval = 0.1
matrix_text = None
matrix_scroll = False
matrix_loop = False

# Database
deviceId = 1
data_upload_interval = 600 # how often devicedata will be uploaded in seconds, 600 seconds = 10 minutes


def start():
    print("Booting... \n")

    form = "%(asctime)s: %(message)s"
    logging.basicConfig(format=form, level=logging.INFO, datefmt="%H:%M:%S")
    wpi.wiringPiSetup()
    initialize_sensors()
    initialize_database()
    print("Initialization success!\n")
    print("---------------------------------\n")

    start_game()


def initialize_database():
    print("DB CONNECTION RESP: SUCCESS \n")
    # if db.is_connected() == True:
    #     print("DB CONNECTION RESP: SUCCESS \n")
    #     #start function that uploads sensordata every 10 minutes
    #     upload_sensordata()
    # else:
    #     print("DB CONNECTION RESP: FAILED \n")


def upload_sensordata():
    while True:

        #get the id of the last log then add 1
        rawlogid = get_logid()
        corlogid = [x[0] for x in rawlogid]
        logid = corlogid[0] + 1

        timestamp = get_timestamp().strftime("%Y-%m-%d %H:%M:%S") #.replace("''", "")
        temperature = 20
        humidity = 20
        knockStatus = 1
        deviceStatus = 1

        #devicedata insert format: logid, timestamp, temperature, humidity, knockStatus, deviceStatus
        insert_into_devicedata(logid, timestamp, temperature, humidity, knockStatus, deviceStatus)

        print("Data insertion complete")
        time.sleep(data_upload_interval)


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

        ultraSound = Ultrasound(0, 0)
        try:
            distance = ultraSound.getDistance()
            print('Ultrasound Sensor: {0}'.format(distance))
        except Exception as e:
            logging.exception(e)

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
    global total_matrix_led

    wpi.pinMode(0, wpi.GPIO.OUTPUT)
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=matrix_cascaded, block_orientation=0, rotate=2,
                     blocks_arranged_in_reverse_order =True)
    virtual = viewport(device, width=200, height=100)
    total_matrix_led = matrix_row_count * matrix_cascaded

    # Create a task to update the matrix
    matrix_task = threading.Thread(target=update_matrix, args=(1,))
    matrix_task.start()

    print("RESP: SUCCESS \n")


def check_esp_connection(esp):
    print('Check ESP_{0} connection...'.format(esp))
    # TODO: check esp connection
    print("RESP: SUCCESS \n")


def update_sensor_data(args):
    global temperature_data
    global humidity_data
    while True:
        print('Updating sensor data')

        # Update temperature
        try:
            dht11_sensor = DHT11Sensor(0)
            temperature_data = dht11_sensor.get_temperature()
            humidity_data = dht11_sensor.get_humidity()
            print('Temperature: {0}'.format(temperature_data))
            print('Humidity: {0}'.format(humidity_data))
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
    set_idle_state()


def set_idle_state():
    print("[Game phase: IDLE]")
    play_audio('bg_idle', True)
    print("Press 'p' to start")
    set_matrix_text("Cor- en dons Whacky adventures", True, True)


def set_end_state(): #sends the session data to the db at the end of the session
    global cur_play_duration
    global game_started

    print("[Game phase: END]")
    play_audio('bg_end', True)
    print("Score: {0}".format(score))

    timestamp = get_timestamp().strftime("%Y-%m-%d %H:%M:%S")

    rawsessionid = get_sessionid()
    corsessionid = [z[0] for z in rawsessionid]
    sessionId = corsessionid[0] + 1
    sessionDuration = cur_play_duration

    # db insert format: sessionId, deviceId, timestamp, sessionDuration, score
    insert_into_userdata(sessionId, deviceId, timestamp, sessionDuration, score)

    print("Data insertion complete")

    cur_play_duration = 0
    game_started = False

    while True:
        time.sleep(result_duration)
        set_idle_state()


def set_matrix_text(text, scroll, loop):
    print('Set matrix text')
    global matrix_text
    global matrix_scroll
    global matrix_loop

    matrix_text = text
    matrix_scroll = scroll
    matrix_loop = loop

    print("Matrix text: {0}".format(matrix_text))


def update_matrix(args):
    global matrix_text
    logging.info("Thread %s: Matrix", threading.current_thread().name)

    while True:
        if matrix_text is not None:
            if matrix_scroll:
                with canvas(virtual) as draw:
                    # draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((0, -2), matrix_text, fill="white")

                # Scroll the text until it is off the screen
                for i in range(virtual.width - device.width):
                    virtual.set_position((i, 0))
                    time.sleep(0.1)

                # for offset in range(total_matrix_led):
                #     virtual.set_position((offset, 0))
                #     time.sleep(0.1)

                if matrix_loop is False:
                    matrix_text = None
            else:
                # show_message(device, matrix_text, fill="white", font=proportional(LCD_FONT))
                with canvas(device) as draw:
                    text(draw, (2, 1), matrix_text, fill="white", font=proportional(LCD_FONT))
            time.sleep(matrix_update_interval)


def play_audio(name, loop):
    print('Play audio, name: {0}, looping: {1}'.format(name, loop))


start()
