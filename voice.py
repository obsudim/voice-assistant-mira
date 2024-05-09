import pyttsx3
import os

from playsound import playsound
from gtts import gTTS


class VoiceModule:
    def __init__(self, online_status: bool):

        # принимает переменную, обозначающую наличие подключения
        # необходимо, чтобы выбрать способ генерации голоса

        self.online_status = online_status


    def say(self, message: str, language: str = 'ru'):
        if self.online_status is True:

            # если человек в сети, то используем gTTS от гугл 
            # для воспроизведения звука будет временно создаваться файл со звуковой дорожкой
            # после чего он будет воспроизвдён и удален

            gTTS(text=message, lang=language).save('tts.mp3')
            playsound('tts.mp3')
            os.remove('tts.mp3')
        else:

            # инициализация движка для офлайн синтеза голоса

            engine = pyttsx3.init()
            engine.say(message)
            engine.runAndWait()


    def _save_file_with_gtts(message: str,
                             file_path: str,
                             lang: str = 'ru'):
        ### служебная функция ###
        gTTS(text=message, lang=lang).save(file_path)


    def play(self, file_path: str):
        playsound(file_path)