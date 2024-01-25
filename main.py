import telebot
from key import token
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = ('Вас приветствует бот-конвертатор валют! Для начала работы введите сообщение боту вида:\n'
            '<имя валюты> <в какую валюту перевести> <количество переводимой валюты>')
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Список доступных валют: евро, доллар, рубль')


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) < 3:
            raise APIException('Недостаточно параметров')
        if len(values) > 3:
            raise APIException('Слишком много параметров')
        quote, base, amount = values
        conversion_result = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Не удалось обработать команду: {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду: {e}')
    else:
        text = f'Цена {amount} {quote} в {base} равна {conversion_result}'
        bot.reply_to(message, text)

bot.polling()

