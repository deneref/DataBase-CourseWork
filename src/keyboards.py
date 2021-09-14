import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from constants import *
from replies import *


def guestMainOptionsKeyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row(GuestChoiceButton.PrimalChoice.SHOWEVENTS)
    keyboard.row(GuestChoiceButton.PrimalChoice.SETTINGS)

    return keyboard


def guestEventShowChoice():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row(GuestChoiceButton.EventShow.SHOWTODAY)
    keyboard.row(GuestChoiceButton.EventShow.SHOWTHISWEEK)
    keyboard.row(GuestChoiceButton.EventShow.UPTOREGISTRATION)
    keyboard.row(GuestChoiceButton.EventShow.CANCELREGISTRATION)

    return keyboard


def guestWeekEvents():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("Пн", callback_data="пн"),
               InlineKeyboardButton("Вт", callback_data="вт"),
               InlineKeyboardButton("Ср", callback_data="ср"),
               InlineKeyboardButton("Чт", callback_data="чт"),
               InlineKeyboardButton("Пт", callback_data="пт"),
               InlineKeyboardButton("Сб", callback_data="сб"),
               InlineKeyboardButton("Вс", callback_data="вс"),
               )
    return markup


def guestRegEvents(eventNames):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for event in eventNames:
        markup.add(InlineKeyboardButton(inline_reg_button_text.format(event["name"], event["start_dt"]),
                                        callback_data=reply_event_choosing_part + event["name"]))
    return markup


def guestRegestratedEvents(eventNames):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    for event in eventNames:
        markup.add(InlineKeyboardButton(event["name"], callback_data=reply_event_cancel_choosing_part + event["name"]))
    return markup


def guestSettingMenu():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row(GuestChoiceButton.Settings.CHANGENAME)
    return keyboard


def adminMainOptionsKeyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row(AdminChoiceButton.PrimalChoice.SHOWSTATS)
    keyboard.row(AdminChoiceButton.PrimalChoice.EDITEVENTS)
    keyboard.row(AdminChoiceButton.PrimalChoice.SETTINGS)

    return keyboard


def adminEventStatChoice():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row(AdminChoiceButton.ShowStats.REGAMOUNT)
    keyboard.row(AdminChoiceButton.ShowStats.SMTHELSE)

    return keyboard


def adminShowRegedStat():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("Январь", callback_data=months[0]),
               InlineKeyboardButton("Февраль", callback_data=months[1]),
               InlineKeyboardButton("Март", callback_data=months[2]),
               InlineKeyboardButton("Апрель", callback_data=months[3]),
               InlineKeyboardButton("Май", callback_data=months[4]),
               InlineKeyboardButton("Июнь", callback_data=months[5]),
               InlineKeyboardButton("Июль", callback_data=months[6]),
               InlineKeyboardButton("Август", callback_data=months[7]),
               InlineKeyboardButton("Сентябрь", callback_data=months[8]),
               InlineKeyboardButton("Октябрь", callback_data=months[9]),
               InlineKeyboardButton("Ноябрь", callback_data=months[10]),
               InlineKeyboardButton("Декабрь", callback_data=months[11]),
               )
    return markup