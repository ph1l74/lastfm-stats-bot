import telebot
import config
import time

print('modules imported')

bot = telebot.TeleBot(config.token)

telebot.apihelper.proxy = {'https': 'socks5h://35.185.64.205:1080'}

if bot:
    print('bot started')
else:
    print('bot start failed')

user_list = []

period_table = {'period_week': '7day',
                'period_month': '1month',
                'period_3month': '3month',
                'period_6month': '6month',
                'period_year': '12month',
                'period_overall': 'overall'}


@bot.message_handler(content_types='text')
def answer(message):
    global user_list

    if not any(user['chat_id'] == message.chat.id for user in user_list):
        print('New chat, id: {}'.format(message.chat.id))
        user_list.append({'chat_id': message.chat.id})
        bot.send_message(message.chat.id, 'Введите имя пользователя с помощью команды /username=')
    else:
        if '/username' in message.text:
            username = message.text[message.text.find(' '):len(message.text)]
            print(username)
            # ['lastfm_username'] = username
            keyboard = telebot.types.InlineKeyboardMarkup()
            cb_period_week = telebot.types.InlineKeyboardButton(text="Неделя", callback_data="period_week")
            cb_period_month = telebot.types.InlineKeyboardButton(text="Месяц", callback_data="period_month")
            cb_period_month_three = telebot.types.InlineKeyboardButton(text="3 месяца", callback_data="period_3month")
            cb_period_month_six = telebot.types.InlineKeyboardButton(text="Полгода", callback_data="period_6month")
            cb_period_year = telebot.types.InlineKeyboardButton(text="Год", callback_data="period_year")
            cb_period_overall = telebot.types.InlineKeyboardButton(text="За все время", callback_data="period_overall")
            keyboard.add(cb_period_week, cb_period_month, cb_period_month_three, cb_period_month_six, cb_period_year,
                         cb_period_overall)
            answer_msg = "Выберите период статистики:"
            bot.send_message(message.chat.id, answer_msg, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global period_table
    if call.message:
        print(period_table[call.data])




try:
    bot.polling(none_stop="True")
except AttributeError:
    print('Attribute Error')
    bot.polling(none_stop="True")
except ConnectionResetError:
    print('Connection Error. Retry in 5 secs...')
    time.sleep(5)
    bot.polling(none_stop="True")
