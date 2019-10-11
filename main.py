import telebot
import socks, socket
import config
import time
import stats_getter
import image_maker
import db
import requests.exceptions as rqst_expts

print('modules imported')

bot = telebot.TeleBot(config.tg_token)


# socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '217.23.6.40', 1080)
telebot.apihelper.proxy = {'https': 'socks5h://45.77.106.122:32125'}


if bot:
    print('bot started')
else:
    print('bot start failed')

user_list = []
lfm_username = ''

period_table = {'period_week': '7day',
                'period_month': '1month',
                'period_3month': '3month',
                'period_6month': '6month',
                'period_year': '12month',
                'period_overall': 'overall'}


def generate_pic(username, period):
    top_artists = stats_getter.get_top_artist(username, period)
    image_report = image_maker.make_report_image_bytes(top_artists, with_frame=True)
    # stats_getter.save_image(image_report, 'image_report')
    return image_report


@bot.message_handler(content_types='text')
def answer(message):
    global user_list
    if not any(user['chat_id'] == message.chat.id for user in user_list):
        print('New chat, id: {}'.format(message.chat.id))
        user_list.append({'chat_id': message.chat.id})
        bot.send_message(message.chat.id, 'Привет! Введите имя пользователя с помощью команды /username')
    else:
        if '/username' in message.text and message.text.find(' ') > 0:
            username = message.text[message.text.find(' ')+1:len(message.text)]
            for user in user_list:
                if user.get('chat_id') == message.chat.id:
                    print('We got user with id ({})'.format(message.chat.id))
                    user.update({'lastfm_username': username})
                    print(user)
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
        else:
            current_user = next(user for user in user_list if user["chat_id"] == message.chat.id)
            if 'lastfm_username' in current_user:
                answer_msg = "Вы случайно не {}? Попробуйте еще раз. Например: \n <a href='https://example.com'>This is an example</a>"\
                    .format(current_user['lastfm_username'], current_user['lastfm_username'],
                            current_user['lastfm_username'], )
            else:
                answer_msg = "Что-то не так с именем пользователя. Попробуйте еще раз. Например: \n " \
                             "[/username ph1l74](/username ph1l74)"
            bot.send_message(message.chat.id, answer_msg)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global period_table, user_list
    if call.message:
        username = ''
        for user in user_list:
            if user.get('chat_id') == call.message.chat.id:
                username = user.get('lastfm_username')
                break
        period = period_table[call.data]
        if len(username) > 0 and period:
            image = generate_pic(username=username, period=period)
            bot.send_photo(call.message.chat.id, image)
            # bot.send_message(call.message.chat.id, answer_msg)
        else:
            bot.send_message(call.message.chat.id, 'Простите, но вы не ввели имя пользователя Last FM. \
            Наберите команду: /username и введите имя пользователя, например: \n /username filatique')


def test_db(chat_id):
    db.get_user_by_chat_id(db_config=config.db, tg_chat_id=chat_id)


while True:
    try:
        bot.polling(none_stop="True", timeout=10)
    except AttributeError:
        print('Attribute Error')
        bot.polling(none_stop="True", timeout=10)
    except ConnectionResetError:
        print('Connection Reset Error. Retry in 5 secs...')
        time.sleep(5)
        bot.polling(none_stop="True", timeout=10)
    except ConnectionError:
        print('Connection Error. Retry in 5 secs...')
        time.sleep(5)
        bot.polling(none_stop="True", timeout=10)
    except rqst_expts.ConnectTimeout:
        print('Connection Timeout Error. Retry in 5 secs...')
        time.sleep(5)
        bot.polling(none_stop="True", timeout=10)
