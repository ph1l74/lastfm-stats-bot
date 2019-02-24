import telebot
import config

print('modules imported')

bot = telebot.TeleBot(config.token)

telebot.apihelper.proxy = {'https': 'socks5h://35.185.64.205:1080'}

if bot:
    print('bot started')
else:
    print('bot start failed')

status = []


@bot.message_handler(content_types='text')
def answer(message):
    global status
    if message.chat.id not in status:
        print('New chat, id: %s' % message.chat.id)
        status.append(message.chat.id)


try:
    bot.polling(none_stop="True")
except AttributeError:
    print('Attribute Error')
    bot.polling(none_stop="True")
