import speech_recognition as sr
import pyttsx3
import win32clipboard



class VoiceManager(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(VoiceManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()

        self.quitFlag = False

    def speechToText(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.recognizer.energy_threshold = 1000
            audio = self.recognizer.listen(source)

        response = {
            "success": True,
            "error": None,
            "transcription": None
        }
        try:
            response["transcription"] = self.recognizer.recognize_google(audio)
        except sr.RequestError:
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            response["success"] = False
            response["error"] = "Unable to recognize speech"

        return response

    def textToSpeech(self, myText):
        self.engine.say(myText)
        self.engine.runAndWait()

    def start(self):
        self.textToSpeech("Welcome back!")
        self.textToSpeech("You are in shopping list.")

        action = 'Listening'
        print(action)
        self.quitFlag = True
        while self.quitFlag:
            print("is on: ", self.quitFlag)
            text = self.speechToText()
            if not text["success"] and text["error"] == "API unavailable":
                print("ERROR: {}\nclose program".format(text["error"]))
                break
            while not text["success"]:
                if not self.quitFlag:
                    break
                print("I didn't catch that. What did you say?\n")
                text = self.speechToText()
            if not self.quitFlag:
                break

            if text["transcription"].lower() == "exit":
                self.quitFlag = False
            print(text["transcription"].lower())
            self.textToSpeech(text["transcription"].lower())

            if text["transcription"].lower() == "speak":
                self.readFromClipboard()

        self.textToSpeech("Goodbye")

    def readFromClipboard(self):
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        self.textToSpeech(data)
