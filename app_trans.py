from googletrans import Translator


trans = Translator()


def translate(s: str, reverse=False):

    if not reverse:
        trans_result = trans.translate(s, src='ru', dest='en')
        return trans_result.text
    trans_result = trans.translate(s, src='en', dest='ru')
    return trans_result.text