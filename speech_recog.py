import re
import queue
import vosk
import json
import time

import sounddevice as sd

# очереди будут необходимы для быстрого добавления в них данных с микрофона
# и быстрого считывания
q = queue.Queue()


def callback(indata, *args):
        q.put(bytes(indata))


def wake_word_in(data: str):
    if re.findall('мира', ''.join(data)):
        print('wake word detected')
        return True
    return False


def recognize(model, wwactivate: bool = False):

    step_time_in_mins = 2
    device = [1, 3]    # sd.default.device
    samplerate = 44100 # int(sd.query_devices(device[0], 'input')['default_samplerate'])
    
    
    with sd.RawInputStream(samplerate=samplerate,
                    blocksize=8000,
                    device=device,
                    dtype='int16',
                    channels=1,
                    callback=callback):
    
        # инициализация расшифровщика

        rec = vosk.KaldiRecognizer(model, samplerate)
        print('recording started')
    
        if wwactivate is True:
            print('waiting for wake')
            start_time = time.time()
            while True:
                data = q.get()
                # сформировавшийся (полный) результат
                if rec.AcceptWaveform(data):
                    data = json.loads(rec.Result())['text'].split()
                    if wake_word_in(data):
                        return True
                    else:
                        if (start_time + step_time_in_mins * 60) <= time.time():
                            print('-' * 20)
                            print('reseting ...')
                            model = vosk.Model('vosk_model')
                            print('waiting for wake')
                            start_time = time.time()
                # промежуточный результат
                else:
                    data = json.loads(rec.PartialResult())['partial'].split()
                    if wake_word_in(data):
                        return True
                # проверка на наличие стоп слова
                
        else:
            print('waiting for data')
            while True:
                data = q.get()
                # берем только сформировавшийся результат
                if rec.AcceptWaveform(data):
                    data = json.loads(rec.PartialResult())['partial']
                    return data