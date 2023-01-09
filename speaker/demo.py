import simpleaudio as sa

def hit():
    wave_obj = sa.WaveObject.from_wave_file("sounds/oof.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

def win():
    wave_obj = sa.WaveObject.from_wave_file("sounds/win.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

def buzz():
    wave_obj = sa.WaveObject.from_wave_file("sounds/buzzer.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()


while True:
    hit()
    win()
    buzz()