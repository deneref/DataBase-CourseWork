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
        except Exception as e:
            bot.send_message(message.from_user.id, "алло уже зареган")


@bot.message_handler(commands=["admin"])
def handle_admin(message):
    if not (checkAdminStatus(message.from_user.id)) and registered(message.from_user.id):
        bot.register_next_step_handler(bot.send_message(message.chat.id, reply_admin_password),
                                       fill_admin_password_step)
    else:
        bot.send_message(message.from_user.id, reply_already_admin)
        giveGuestStatus(message.from_user.id)


@bot.message_handler(commands=["menu"])
def handle_start(message):
    if registered(message.from_user.id):
        sendMainOptionsKeyboard(message.chat.id)


@bot.message_handler(commands=["print"])
def handle_admin(message):
    users = selectAllFromUsers()
    regs = selectAllFromRegs()
    [print(u) for u in users]
    [print(r) for r in regs]


@bot.message_handler(commands=["help"])
def handle_admin(message):
    bot.send_message(message.from_user.id, help_note)


def sendMainOptionsKeyboard(id):
    userType = getUserType(id)
    if userType == UserType.GUEST:
        bot.send_message(id, reply_main_options, reply_markup=guestMainOptionsKeyboard())
    elif userType == UserType.ADMIN:
        bot.send_message(id, reply_main_options, reply_markup=adminMainOptionsKeyboard())


def sendGuestEventChoosingKeyboard(id):
    userType = getUserType(id)
    if userType == UserType.GUEST:
        bot.send_message(id, reply_main_options, reply_markup=guestEventShowChoice())


def fill_name_step(message):
    try:
        userId = message.from_user.id
        fillUserFIO(id=userId, FIO=message.text)
        sendMainOptionsKeyboard(userId)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def fill_admin_password_step(message):
    userId = message.chat.id
    if not registered(userId):
        bot.reply_to(message, 'Нажми /start, друг')
        return

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
    try:
        bot.send_message(message.chat.id, reply_choose_day_of_the_week, reply_markup=guestWeekEvents())
    except:
        bot.send_message(message.chat.id, reply_nothing_found)


@bot.callback_query_handler(func=lambda call: call.data in weekDays)
def callback_query(call):
    weekEvents = getWeekEvents()
    try:
        if call.data == weekDays[0]:
            print(weekEvents[0])
            #bot.answer_callback_query(call.id, weekEvents[0])
            bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                  text=weekEvents[0], reply_markup=guestWeekEvents())
            # bot.send_message(call.from_user.id, weekEvents[0])
        elif call.data == weekDays[1]:
            print(weekEvents[1])
            #bot.answer_callback_query(call.id, weekEvents[1])
            bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                  text=weekEvents[1], reply_markup=guestWeekEvents())
            # bot.send_message(call.from_user.id, weekEvents[1])
        elif call.data == weekDays[2]:
            print(weekEvents[2])
            #bot.answer_callback_query(call.id, weekEvents[2])
            # bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
            #                       text=weekEvents[2], reply_markup=guestWeekEvents())
            bot.send_message(call.from_user.id, weekEvents[2])
        elif call.data == weekDays[3]:
            print(weekEvents[5])
            #bot.answer_callback_query(call.id, weekEvents[3])
            bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                  text=weekEvents[3], reply_markup=guestWeekEvents())
            # bot.send_message(call.from_user.id, weekEvents[3])

        elif call.data == weekDays[4]:
            print(weekEvents[4])
            #bot.answer_callback_query(call.id, weekEvents[4])
            bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                  text=weekEvents[4], reply_markup=guestWeekEvents())
            # bot.send_message(call.from_user.id, weekEvents[4])
        elif call.data == weekDays[5]:
            print(weekEvents[5], "5")
            #bot.answer_callback_query(call.id, weekEvents[5])
            bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                  text=weekEvents[5], reply_markup=guestWeekEvents())
            #bot.send_message(call.from_user.id, weekEvents[5])
        elif call.data == weekDays[6]:
            print(weekEvents[6])
            #bot.answer_callback_query(call.id, weekEvents[6])
            bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id,
                                   text=weekEvents[6], reply_markup=guestWeekEvents())
            # bot.send_message(call.from_user.id, weekEvents[6])
    except Exception as e:
        print(str(e))


@bot.message_handler(func=lambda message: message.text == GuestChoiceButton.EventShow.SHOWTODAY,
                     content_types=['text'])
def choiceGuestShowTodayEvents(message):
    try:
        bot.send_message(message.chat.id, getTodayEvents())
        sendMainOptionsKeyboard(message.chat.id)
    except Exception as e:
        print(str(e))
        bot.send_message(message.chat.id, reply_nothing_found)


@bot.message_handler(func=lambda message: message.text == GuestChoiceButton.PrimalChoice.SETTINGS,
                     content_types=['text'])
def choiceGuestOptionsChangeName(message):
    bot.send_message(message.chat.id, empty_msg, reply_markup=guestSettingMenu())


@bot.message_handler(func=lambda message: message.text == GuestChoiceButton.Settings.CHANGENAME
                                          or message.text == AdminChoiceButton.Settings.CHANGENAME,
                     content_types=['text'])
def choiceGuestOptionsChangeName(message):
    try:
        bot.register_next_step_handler(bot.send_message(message.chat.id, reply_settings_change_name), fill_name_step)
    except Exception as e:
        print(str(e))
        bot.send_message(message.chat.id, "Упс не получилось!")


'''ЗАПИСЬ НА ИВЕНТ'''


@bot.message_handler(func=lambda message: message.text == GuestChoiceButton.EventShow.UPTOREGISTRATION,
                     content_types=['text'])
def choiceGuestUpToRegistration(message):
    try:
        upfrontWeekEvents = getActiveWeekUpfrontEvents(MAXEVENTSONREG)
        if len(upfrontWeekEvents) > 0:
            bot.send_message(message.chat.id, reply_choose_event,
                             reply_markup=chooseUpcomingWeekEvents(upfrontWeekEvents, reply_event_choosing_part))
        else:
            bot.send_message(message.chat.id, reply_empty_week)
            sendMainOptionsKeyboard(message.chat.id)
    except Exception as e:
        print(str(e))
        bot.send_message(message.chat.id, reply_nothing_found)


@bot.callback_query_handler(func=lambda call: call.data.find(reply_event_choosing_part) != -1)
def callback_query(call):
    upfrontWeekEvents = getActiveWeekUpfrontEvents(MAXEVENTSONREG)
    for event in upfrontWeekEvents:
        try:
            if call.data == reply_event_choosing_part + event["name"]:
                bot.answer_callback_query(call.id, event["name"])
                ok = addRegistrationOnEvent(event["id"], call.from_user.id)
                if ok:
                    bot.edit_message_text(message_id=call.message.message_id,
                                          chat_id=call.from_user.id,
                                          text=reply_success_registration.format(event["name"]))
                else:
                    bot.edit_message_text(message_id=call.message.message_id,
                                          chat_id=call.from_user.id,
                                          text=reply_already_reged)

                sendGuestEventChoosingKeyboard(call.from_user.id)
        except Exception as e:
            print(str(e))
            print(event)
            bot.edit_message_text(message_id=call.message.message_id,
                                  chat_id=call.from_user.id,
                                  text=error_msg)


@bot.message_handler(func=lambda message: message.text == GuestChoiceButton.EventShow.CANCELREGISTRATION,
                     content_types=['text'])
def choiceGuestCancelRegistration(message):
    try:
        userRegistratedEvents = getUserActiveRegistratedEvents(message.from_user.id, MAXEVENTSONREG)
        if len(userRegistratedEvents) != 0:
            bot.send_message(message.chat.id, reply_choose_event_to_cancel,
                             reply_markup=guestRegestratedEvents(userRegistratedEvents))
        else:
            bot.send_message(message.chat.id, reply_no_hay_events_to_cancel)

    except Exception as e:
        print(str(e))
        bot.send_message(message.chat.id, error_msg)


@bot.callback_query_handler(func=lambda call: reply_event_cancel_choosing_part in call.data)
def callback_query(call):
    userRegistratedEvents = getUserActiveRegistratedEvents(call.from_user.id, MAXEVENTSONREG)
    for event in userRegistratedEvents:
        if call.data == reply_event_cancel_choosing_part + event["name"]:
            bot.answer_callback_query(call.id, event["name"])
            if calncelRegistrationOnEvent(event["eventId"], call.from_user.id):
                bot.edit_message_text(message_id=call.message.message_id,
                                      chat_id=call.from_user.id,
                                      text=reply_success_unregistration.format(event["name"]))
            else:
                bot.edit_message_text(message_id=call.message.message_id,
                                      chat_id=call.from_user.id,
                                      text=reply_unsuccess_unregistration)

            sendMainOptionsKeyboard(call.from_user.id)


'''ADMIN HANDLERS'''


@bot.message_handler(func=lambda message: message.text == AdminChoiceButton.PrimalChoice.SHOWSTATS,
                     content_types=['text'])
def choiceAdminShowRegedStat(message):
    if not checkAdminStatus(message.from_user.id): return
    try:
        bot.send_message(message.chat.id, reply_choose_stat_to_show,
                         reply_markup=adminEventStatChoice())
    except Exception as e:
        print(str(e))
        bot.send_message(message.chat.id, error_msg)


@bot.message_handler(func=lambda message: message.text == AdminChoiceButton.ShowStats.REGAMOUNT,
                     content_types=['text'])
def choiceAdminShowRegedStat(message):
    if not checkAdminStatus(message.from_user.id): return
    try:
        bot.send_message(message.chat.id, reply_choose_months_to_show_stats,
                         reply_markup=adminShowRegedStat())
    except Exception as e:
        print(str(e))
        bot.send_message(message.chat.id, error_msg)


@bot.callback_query_handler(func=lambda call: call.data in months)
def callback_query(call):
    if not checkAdminStatus(call.from_user.id): return
    try:
        stats = getRegistratedStatsForGivenMonth(call.data)
        msg = reply_stats
        [print(e) for e in stats]
        for r in stats:
            msg = msg + reply_stats_row.format(r["name"], r["count_active"], r["count_inactive"])

        print(msg)
        if len(msg) > 4096:
            for x in range(0, len(msg), 4096):
                bot.send_message(call.from_user.id, msg[x:x + 4096])
        elif len(stats) == 0:
            bot.send_message(call.from_user.id, reply_nothing_found)
        else:
            bot.send_message(call.from_user.id, msg)
    except Exception as e:
        print(str(e))
        bot.edit_message_text(message_id=call.message.message_id,
                              chat_id=call.from_user.id,
                              text=reply_no_stat_for_month)


'''ADMIN EDIT EVENT'''


@bot.message_handler(func=lambda message: message.text == AdminChoiceButton.PrimalChoice.EDITEVENTS,
                     content_types=['text'])
def choiceAdminEditEvents(message):
    if not checkAdminStatus(message.from_user.id): return
    upfrontWeekEvents = getAllWeekUpfrontEvents(MAXEVENTSONREG)
    try:
        bot.send_message(message.chat.id, text=reply_event_edit,
                         reply_markup=chooseUpcomingWeekEvents(upfrontWeekEvents, reply_event_edit_part))
    except Exception as e:
        print(str(e))
        bot.send_message(message.chat.id, error_msg)


@bot.callback_query_handler(func=lambda call: call.data.find(reply_event_edit_part) != -1)
def callback_query(call):
    upfrontWeekEvents = getAllWeekUpfrontEvents(MAXEVENTSONREG)
    for event in upfrontWeekEvents:
        try:
            if call.data == reply_event_edit_part + event["name"]:
                bot.answer_callback_query(call.id, event["name"])

                bot.send_message(chat_id=call.from_user.id,
                                 text=reply_event_markup_advanced
                                 .format(event["id"], event["name"], event["start_dt"], event["start_time"],
                                         event["owner"], event["status"], event["description"]))

                bot.register_next_step_handler(bot.send_message(call.from_user.id, reply_event_edit1), edit_event_step)
        except Exception as e:
            print(str(e))
            bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text=error_msg)


def edit_event_step(message):
    try:
        event = {}
        for line in message.text.split("\n"):
            part1, part2 = line.split(": ")[0], line.split(": ")[1]
            if part1 == "№":
                event["id"] = part2
            elif part1 == "Название":
                event["name"] = part2
            elif part1 == "Дата":
                event["start_dt"] = part2
            elif part1 == "Время":
                event["start_time"] = part2
            elif part1 == "Проводит":
                event["owner"] = part2
            elif part1 == "Статус":
                event["status"] = part2
            elif part1 == "Описание":
                event["description"] = part2
        print(event)
        if updateEvent(event):
            bot.send_message(chat_id=message.from_user.id, text=reply_event_succ_upd)
        else:
            bot.send_message(chat_id=message.from_user.id, text=reply_event_unsucc_upd)

    except Exception as e:
        bot.reply_to(message, 'чушь-пурга')
        print(str(e))


'''ADMIN ADD EVENT'''


@bot.message_handler(func=lambda message: message.text == AdminChoiceButton.PrimalChoice.ADDEVENT,
                     content_types=['text'])
def choiceAdminAddEvents(message):
    if not checkAdminStatus(message.from_user.id): return
    try:
        bot.send_message(message.from_user.id, reply_event_add_remind)
        bot.register_next_step_handler(bot.send_message(message.from_user.id, reply_event_add), add_event_step)
    except Exception as e:
        print(str(e))
        bot.send_message(message.chat.id, error_msg)


def add_event_step(message):
    try:
        event = {}
        for line in message.text.split("\n"):
            part1, part2 = line.split(": ")[0], line.split(": ")[1]
            if part1 == "Название":
                event["name"] = part2
            elif part1 == "Дата":
                event["start_dt"] = part2
            elif part1 == "Время":
                event["start_time"] = part2
            elif part1 == "Проводит":
                event["owner"] = part2
            elif part1 == "Как долго":
                event["duration"] = part2
            elif part1 == "Описание":
                event["description"] = part2

        event["status"] = EventStatus.GOINGTO
        print(event)
        add_event(event["name"], event["owner"], event["start_dt"],
                  event["start_time"], event["duration"], event["description"])
        bot.send_message(message.from_user.id, text="Добавили!")
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    try:
        db.connect()
        db.drop_tables([Users, Events, Registrations])
        db.create_tables([Users, Events, Registrations])
        loadSomeEvents()
    except InternalError as px:
        print(str(px))

    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()

    bot.polling(none_stop=True)
