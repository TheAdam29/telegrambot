import telebot
from config import TOKEN, currency
from extensions import ConvertionException, APIException
from datetime import datetime


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    now = datetime.now()
    current_time = int(now.strftime("%H"))

    if 6 <= current_time <= 12:
        text = 'Доброе утро👋\n'
    elif 12 <= current_time <= 18:
        text = 'Добрый день👋\n'
    elif 18 <= current_time <= 24:
        text = 'Добрый вечер👋\n'
    else:
        text = 'Доброй ночи👋\n'

    text += 'Чтобы начать работу введите комманду в следующем формате:\n\n<имя валюты>\t\t ' \
           '<в какую валюту перевести>\t\t' \
           '<количество переводимой валюты>\n\nУвидеть список всех доступных валют: /values \n\n' \
           'Пример ввода: доллар рубль 10'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currency.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Должно быть 3 параметра')

        quote, base, amount = values
        total_base = APIException.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} = {round(total_base, 2)}'
        bot.send_message(message.chat.id, text)


bot.polling()