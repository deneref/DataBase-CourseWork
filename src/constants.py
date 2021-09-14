with open('secrets/API-token.txt') as f:
    token = f.read()

with open('secrets/magicWord.txt') as f:
    magicWord = f.read()
    
dateFormat = "%d-%m-%Y"
timeFormat = "%H:%m"

weekDays = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
# months = ["январь", "февраль", "март", "апрель", "май", "июнь",
#          "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
MAXEVENTSONREG = 10


class UserStatus:
    UNKNOWN = -1  # default
    PREREGISTRATED = 1  # pressed button, not filled name
    REGISTRATED = 2  # fully registrated
    DELETED = 4  # deleted user....:(


class UserType:
    UNKNOWN = -1  # default
    GUEST = 1  # guest type with limited prems
    ADMIN = 0  # admin status


class EventStatus:
    UNKNOWN = -1
    GOINGTO = 1
    CANCELED = 2
    INDEV = 3


class RegistrationStatus:
    ACTIVE = 1
    INACTIVE = 0


class GuestChoiceButton:
    class PrimalChoice:
        SHOWEVENTS = "А шо там по ивентам?"
        SETTINGS = "Хочу кое-шо поменять..."

    class EventShow:
        SHOWTODAY = "Что будет сегодня?"
        SHOWTHISWEEK = "Что будет на этой неделе?"
        UPTOREGISTRATION = "Я хочу записаться на ивент"
        CANCELREGISTRATION = "Хочу отменить запись"

    class Settings:
        CHANGENAME = "Хочу поменять имя"


class AdminChoiceButton:
    class PrimalChoice:
        SHOWSTATS = "Смотреть статистику"
        EDITEVENTS = "Редактировать ивенты"
        SETTINGS = "Настройки"

    class ShowStats:
        REGAMOUNT = "Сколько куда записаны"
        SMTHELSE = "Smth else..."

    class Settings:
        CHANGENAME = "Хочу поменять имя"
