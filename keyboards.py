import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from constants import *


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
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Event 1", callback_data="ev_id1"),
               InlineKeyboardButton("Event 2", callback_data="ev_id2"))
    return markup


def guestSettingMenu():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row(GuestChoiceButton.Options.CHANGENAME)
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
