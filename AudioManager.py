import os
import threading
from playsound import playsound

class AudioManager(object):
    is_on = False

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AudioManager, cls).__new__(cls)
        return cls.instance

    def play_sound(self, sound):
        if self.is_on:
            print(f"{os.getcwd()}\\Sounds\\{sound}")
            threading.Thread(target=playsound, args=(f"{os.getcwd()}\\Sounds\\{sound}", )).start()
