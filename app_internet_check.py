import requests

# проверка заключается в том, что если устройству удается получить запрос
# с какого-либо сайта, то значит, что интернет на устройстве есть

def internet_connection():
    try:
        requests.get('https://ya.ru/').ok
    except Exception:
        return False
    return True