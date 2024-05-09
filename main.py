# ИМпорт библиотек 
import vosk
import time

from app_internet_check import internet_connection
from voice import VoiceModule
from speech_recog import recognize
from intent_clsf import IntentClassifier
from intent_disp import IntentDispatcher


def main():
    is_online = internet_connection() # проверка на наличие интренета
    model = vosk.Model('vosk_model') # первичная загрузка модели 
    voice = VoiceModule(is_online) # инициализация синтезатора голоса
    classifier = IntentClassifier() # инициализация классификатора интентов
    dispatcher = IntentDispatcher() # инициализация диспетчера интентов
    running = True

    if not is_online:
        time.sleep(0.5)
        voice.say('Отсутствует подключение к интернету. Некоторые функции могут не работать')
    while running:
        ## 1. ожидаем wake word и проигрываем приветственный сигнал,
        ## инициализируем переменную LOOP, отвечающую за непрерывный
        ## прием запросов во время одного цикла


        recognize(model, wwactivate=True)
        voice.play('data/wwsound.mp3')
        LOOP = True

        
        while LOOP and running:

            ## 2. обрабатываем одну полноценную звуковую волну и получаем
            ## данные с неё
            data = recognize(model)

            # в основе классификатора и диспетчера интентов лежит техника
            # многоуровневых регулярных выражений
            
            ## 3. отправляем полученные данные в классификатор намерений,
            ## который разделит по intent'ам данные, отправив на выход название
            ## необходимой функции
            intent = classifier.intent_classify(data)
        
            ## 4. отправка интента в диспетчер интентов
            ## если диспетчер при вызове выдает 0, значит надо завершить цикл
            ## в диспетчере выполняется какая-то функция, в конце которой воспроизводится
            ## вопрос о закрытии цикла
            result = dispatcher.intent_classify_disp(intent, voice, is_online, model) # вместе с интентом подается разговорный модуль 
            if result == 0:
                LOOP = False
            elif result == 'close':
                LOOP = False
                running = False


        ## 5. конец цикла, воспроизводится заключительный сигнал, 
        ## программа перезагружает модель (может занять до 3 сек.) для того,
        ## чтобы исключить возможные ошибки при длительном использованиии,
        ## после чего функция возвращается к пункту 1.
        voice.play('data/ending_signal.mp3')
        model = vosk.Model('vosk_model')


    voice.say('Закрытие программы. До свидания')
   

    

## точка входа, необходимая, чтобы запуск программы производился непосредственно из неё самой
if __name__ == '__main__':
    main()