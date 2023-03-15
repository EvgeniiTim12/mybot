transl={
    'eng':{
        "Хтось використав вашу ссилку!":"Someone used your link!",
        "Але це ж ваша ссилка!":"But it's your link!",
        "Ви зареєстровані успішно":"You are registered successfully",
        "Привіт!":"Hi!",
        "Ваша ссилка:":"Your link:",
        "К-сть рефералов:":"Number of referrals:",
        "Некоректний номер картки, /cancel для скасування":"Incorrect card number, /cancel to cancel",
        "Введіть карту":"Enter card",
        "Карта успішно додана":"Card successfully added",
        "Видалено":"Deleted",
        "Скасовано":"Canceled",
        "Додано":"Added",
        "Номер карти:":"Card number:",
        "Баланс:":"Balance:",
        "Виберіть операцію":"Choose operation"

    }
}

def trans(text,lang='ukr'):
    if lang=='ukr':
        return text
    else:
        global transl
        try:
            return transl[lang][text]
        except:
            return text


