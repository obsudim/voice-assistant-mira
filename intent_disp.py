import re
import time
import os


from datetime import datetime
from random import choice
from voice import VoiceModule
from app_weather import get_weather
from app_vk import vk_main_check, vk_main_send, get_user_name
from speech_recog import recognize
from app_config import friends_dict, send_message_with_wm
from app_volume import set_volume, get_volume
from app_trans import translate


class IntentDispatcher:

      def intent_classify_disp(self, intent: str, voice: VoiceModule, is_online, model):


            if intent == 'weather_sum':
                  self.weather(intent, voice, is_online)

            elif intent == 'watch_sum':
                  self.watch(intent, voice, is_online)

            elif intent == 'media_sum':
                  self.media(intent, voice, is_online)

            elif intent == 'settings_sum':
                  if self.settings(intent, voice, is_online, model) == 'close':
                        return 'close'

            elif intent == 'send_media_sum':
                  self.send_media(intent, voice, is_online, model)

            elif intent == 'translator_sum':
                  self.translator(intent, voice, is_online, model)

            elif '<tlk>' in intent:
                  self.not_recognized(intent, voice, is_online)

            else:
                  return 0
    
    
      @staticmethod
      def weather(intent: str,
                  voice: VoiceModule,
                  is_online: bool):
            
            # примеры использования функции:
            ## какая сейчас погода
            if is_online:
                  beginnings = ['Сейчас за окном', 'За окном сейчас', 'Температура на улице']

                  voice.say('Подождите секунду. информация загружается')
                  temp, fl, desc = get_weather()
                  voice.say(f'{choice(beginnings)} {int(temp)} градусов. ощущается как {int(fl)} градусов. {translate(desc, reverse=True)}')
            else:
                  voice.say('Извините. данная функция не доступна без интернета')


      @staticmethod
      def watch(intent: str,
                voice: VoiceModule,
                is_online: bool):
            
            beginnings = ['Текущее время', 'Сейчас']
            
            to_hs = ''
            to_mins = ''

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            hours, mins = current_time.split(':')[0], current_time.split(':')[1] 
            
            # красивй вывод
            if hours[-1] == '1' and hours != '11':
                        to_hs = 'час'
            elif hours[-1] in '234' and hours not in ['12', '14', '14']:
                  to_hs = 'часа'
            else:
                  to_hs = 'часов'
            if mins[-1] == '1' and mins != '11':
                        to_mins = 'минута'
            elif mins[-1] in '234' and mins not in ['12', '14', '14']:
                  to_mins = 'минуты'
            else:
                  to_mins = 'минут'

            voice.say(f'{choice(beginnings)} {hours} {to_hs} {mins} {to_mins}')


      @staticmethod
      def media(intent: str,
                voice: VoiceModule,
                is_online: bool):
            
            if is_online:
                  voice.say('Подождите секунду. информация загружается')
                  data = vk_main_check()
                  voice.say('Информация загружена')
                  if len(data) == 0:
                        time.sleep(0.5)
                        voice.say('Нет никаких новых сообщений')
                  elif len(data) == 1:
                        name = get_user_name(data[0][0])
                        voice.say(f'Было получено всего сообщений: одно. от пользователя {name}')
                  else:
                        voice.say(f'Было получено всего сообщений: {len(data)}. от пользователей.')
                        for person in data:
                              voice.say(get_user_name(person[0]))
            else:
                  voice.say('Извините. данная функция не доступна без интернета')
                  
            

      @staticmethod
      def settings(intent: str,
                  voice: VoiceModule,
                  is_online: bool,
                  model):
            
            voice.say('скажите, что бы вы хотели изменить. вы можете. Закрыть программу, выключить устройство, изменить звук, узнать текущую громкость')
            data = recognize(model)
            commands = [len(re.findall('закр', data)), len(re.findall('выключ', data)) + len(re.findall('отключ', data)),
             len(re.findall('измен', data)), len(re.findall('текущ', data))]
            if not sum(commands) == 0:
                  if commands.index(max(commands)) == 0:
                        return 'close'
                  elif commands.index(max(commands)) == 1:
                        voice.say('выключаем устройство. до свидания')
                        os.system('shutdown /s /t 1')

                  elif commands.index(max(commands)) == 2:
                        voice.say('скажите одно слово: требуемый уровень громкости от нуля до десяти')
                        data = recognize(model)
                        try:
                              set_volume(data)
                              voice.play('data\short.mp3')
                        except:
                              voice.say('дан некорректный формат. попробуйте ещё')                  
                  else:
                        vol = get_volume()
                        voice.say(f'текущий уровень громкости: {round(vol* 10)}')


      @staticmethod
      def send_media(intent: str,
                  voice: VoiceModule,
                  is_online: bool,
                  model):
            
            if is_online:
                  voice.say('кому вы хотите отправить сообщение?')
                  user = None
                  data = recognize(model)
                  for i in friends_dict.keys():
                        if i in data:
                              user = i
                              break
                  if user is None:
                        voice.say('Такого пользователя нет в базе. попробуйте добавить его в ручную или повторите снова')
                  else:
                        voice.say('Для того чтобы отправить сообщение четко произнесите текст сообщения')
                        message = recognize(model)
                        if send_message_with_wm:
                              message +='\n\n*отправлено с голосового помощника'
                        vk_main_send(friends_dict[user], message)
                        voice.say('сообщение было отправлено')
            else:
                  voice.say('Извините. данная функция не доступна без интернета')
                  
      
      @staticmethod
      def translator(intent: str,
                  voice: VoiceModule,
                  is_online: bool,
                  model):
            if is_online:
                  voice.say('скажите, какую фразу хотели бы перевести на английский язык')
                  data = recognize(model)
                  trsl = translate(data)
                  voice.say(f'{data}')
                  voice.say('на английском будет звучать как')
                  voice.say(trsl, language='en')
            else:
                  voice.say('Извините. данная функция не доступна без интернета')
            



      @staticmethod
      def not_recognized(intent: str,
                  voice: VoiceModule,
                  is_online: bool):
            
            beginnings = ['Извините, не удалось классифицировать ваше намерение, пожалуйста повторите снова',
                          'Извините, не смогла распознать намерение, повторите снова']

            voice.say(choice(beginnings))


# import vosk
# print(IntentDispatcher.settings('', VoiceModule(True), True, vosk.Model('vosk_model')))