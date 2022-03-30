import os
import threading
from playsound import playsound

class AudioManager(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AudioManager, cls).__new__(cls)
        return cls.instance

    def play_sound(self, sound):
        print(f"{os.getcwd()}\\Sounds\\{sound}")
        threading.Thread(target=playsound, args=(f"{os.getcwd()}\\Sounds\\{sound}", )).start()
