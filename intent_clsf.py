import re
 

class IntentClassifier:
    def __init__(self, request: str = '') -> None:
        self.FUNCTIONS_NAMES = [
            self.weather_sum,
            self.watch_sum,
            self.media_sum,
            self.settings_sum,
            self.stop_word_sum,
            self.send_media_sum,
            self.translator_sum
        ]

    
    @staticmethod
    def weather_sum(s: str):

        ## какая сейчас погода в волгограде
        ## сколько сейчас градусов на улице
        ## сколько сейчас градусов в волгограде

        w1 = len(re.findall(r'погод', s) * 20)
        w2 = len(re.findall(r'температур', s) * 10)
        w3 = len(re.findall(r'градус', s) * 10)
        w4 = len((re.findall(r'сколько', s) + re.findall(r'улиц|ок[а-я]*о', s)) * 5)
        
        return w1 + w2 + w3 + w4



    @staticmethod
    def watch_sum(s: str):

        ## сколько сейчас времени
        ## сколько времени

        w1 = len(re.findall(r'врем', s) * 10 + re.findall(r'сколько|посмотри', s) * 2)
        return w1


    @staticmethod
    def media_sum(s: str):

        ##  есть ли новые сообщения в вконтакте?
        ## пришли ли новые уведомления в телеграмме

        w2 = len((re.findall(r'сообщени', s) + re.findall(r'есть', s)) * 15)
        w3 = len(re.findall(r'уведомлени', s) * 20)
        w4 = len(re.findall(r'пришл', s) + re.findall(r'нов', s) * 5)

        return w2 + w3 + w4


    @staticmethod
    def send_media_sum(s: str):

        ## отправь сообщение максимке в вк

        w1 = len((re.findall(r'сообщени', s) + re.findall(r'напиши|отправ', s)) * 15)

        return w1


    @staticmethod
    def settings_sum(s: str):

        ### для открытия настроек нужно отдельно сказать запрос ###
        
        ## открой настройки
        ## зайди в настройки
        
        w1 = len(re.findall(r'настройк', s) * 20)
        return w1


    @staticmethod
    def stop_word_sum(s: str):

        ## стоп
        ## хватит
        ## нет
        ## ничем

        w1 = len(re.findall(r'стоп', s) * 20)
        w2 = len(re.findall(r'хватит', s) * 20)

        return w1 + w2
    
    @staticmethod
    def translator_sum(s: str):

        ## открой переводчик
        ## найди перевод слова

        w1 = len(re.findall(r'перевод', s) * 20)
        w2 = len(re.findall(r'перевед', s) * 20)

        return w1 + w2
    
    # финальная проверка
    def intent_classify(self, s):
        fnames = self.FUNCTIONS_NAMES
        if s == '':
            return '<empreq>'
        max_points = 0
        s_class = ''
        for i in fnames:
            if i(s) > max_points:
                s_class = str(i.__name__)
                max_points = i(s)
        if max_points <= 10:
            return '<tlk>' + s
        return s_class