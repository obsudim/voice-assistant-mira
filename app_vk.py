import vk_api

from app_config import access_token


session = vk_api.VkApi(token=access_token)


def vk_main_check():
    messages = session.method('messages.getConversations', {'count': 10, 
                                                        'filter': 'unread',
                                                        'extended': 1})

    ur_count = '' if 'unread_count' not in messages.keys() else messages['unread_count']

    data = []
    if ur_count:
        
        for i in messages['items']:
            last_mes = i['last_message']
            mes_count = i['conversation']['unread_count']
            id = last_mes['from_id']
            text = last_mes['text']
            atts = last_mes['attachments']
            last_m_type = None if len(atts) == 0 else atts[0]['type']
            text = None if not text else text


            data.append((id, mes_count, last_m_type, text))


    return data


def vk_main_send(user_id, s_text):
    session.method('messages.send', {'user_id': user_id,
                                    'random_id': 0,
                                    'message': s_text})
    

def get_user_name(id):
    user = session.method("users.get", {"user_ids": id})
    fullname = user[0]['first_name'] +  ' ' + user[0]['last_name']
    return fullname

