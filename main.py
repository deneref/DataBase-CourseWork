import constants
from dbModel import *
from replies import *
from keyboards import *
from peewee import *

bot = telebot.TeleBot(constants.token)


# /start
@bot.message_handler(commands=["start"])
def handle_start(message):
    userId = message.from_user.id
    if not registered(message.from_user.id):
        add_user(id=userId, userName=message.from_user.username,
                 userType=UserType.GUEST, status=UserStatus.PREREGISTRATED)
        bot.register_next_step_handler(bot.send_message(message.chat.id, reply_unreg_user0), fill_name_step)
    else:
        try:
            bot.send_message(message.from_user.id, "{}, алло уже зареган".format(getUserName(userId)))
        except:
            bot.send_message(message.from_user.id, "алло уже зареган")


@bot.message_handler(commands=["admin"])
def handle_start(message):
    if registered(message.from_user.id):
        # bot.send_message(userId, reply_admin_password)
        bot.register_next_step_handler(bot.send_message(message.chat.id, reply_admin_password),
                                       fill_admin_password_step)
        '''
        succ = giveAdminStatus(userId, message.text)
        if succ:
            bot.send_message(message.from_user.id, reply_admin_change_succ)
        else:
            bot.send_message(message.from_user.id, reply_admin_change_denied)

    sendMainOptionsKeyboard(userId)
'''


@bot.message_handler(commands=["menu"])
def handle_start(message):
    if registered(message.from_user.id):
        sendMainOptionsKeyboard(message.chat.id)


def sendMainOptionsKeyboard(id):
    userType = getUserType(id)
    if userType == UserType.GUEST:
        bot.send_message(id, reply_main_options, reply_markup=guestMainOptionsKeyboard())
    elif userType == UserType.ADMIN:
        bot.send_message(id, reply_main_options, reply_markup=adminMainOptionsKeyboard())


def fill_name_step(message):
    try:
        userId = message.from_user.id
        fillUserFIO(id=userId, FIO=message.text)
        sendMainOptionsKeyboard(userId)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def fill_admin_password_step(message):
    userId = message.chat.id
    print(message.chat.id, message.from_user.id)
    succ = giveAdminStatus(userId, message.text)
    if succ:
        bot.send_message(message.from_user.id, reply_admin_change_succ)
    else:
        bot.send_message(message.from_user.id, reply_admin_change_denied)

    sendMainOptionsKeyboard(userId)


@bot.message_handler(func=lambda message: message.text == GuestChoiceButton.PrimalChoice.SHOWEVENTS,
                     content_types=['text'])
def choiceGuestShowEvents(message):
    bot.send_message(message.chat.id, empty_msg, reply_markup=guestEventShowChoice())


@bot.message_handler(func=lambda message: message.text == GuestChoiceButton.EventShow.SHOWTHISWEEK,
                     content_types=['text'])
def choiceGuestShowWeekEvents(message):
    bot.send_message(message.chat.id, empty_msg, reply_markup=guestWeekEvents())


@bot.message_handler(func=lambda message: message.text == GuestChoiceButton.EventShow.SHOWTODAY,
                     content_types=['text'])
def choiceGuestShowTodayEvents(message):
    try:
        bot.send_message(message.chat.id, getTodayEvents())
    except Exception as e:
        print(str(e))
        bot.send_message(message.chat.id, "Кажись сегодня ничего нет!")


@bot.message_handler(func=lambda message: message.text == GuestChoiceButton.PrimalChoice.SETTINGS,
                     content_types=['text'])
def choiceGuestOptionsChangeName(message):
    bot.send_message(message.chat.id, empty_msg, reply_markup=guestSettingMenu())


@bot.message_handler(func=lambda message: message.text == GuestChoiceButton.Options.CHANGENAME,
                     content_types=['text'])
def choiceGuestOptionsChangeName(message):
    try:
        bot.register_next_step_handler(bot.send_message(message.chat.id, reply_unreg_user0), fill_name_step)
    except Exception as e:
        print(str(e))
        bot.send_message(message.chat.id, "Упс не получилось!")


if __name__ == "__main__":
    try:
        db.connect()
        Users.create_table()
        Events.create_table()
        Registrations.create_table()

        loadSomeEvents()
    except InternalError as px:
        print(str(px))

    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()

    bot.polling(none_stop=True)
