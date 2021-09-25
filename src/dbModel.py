from datetime import *

from peewee import *
from constants import *
from datetime import date
from replies import *

# DB
db = SqliteDatabase('./events.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64})


# DB tables
class Events(Model):
    id = AutoField(unique=True, null=False)
    name = CharField()
    owner = CharField()
    start_dt = DateField(formats=[dateFormat])
    start_time = TimeField(formats=[timeFormat])
    duration = CharField()
    description = CharField()
    event_status = IntegerField(default=None)

    class Meta:
        db_table = 'events'
        database = db


class Users(Model):
    id = PrimaryKeyField(unique=True, null=False)
    name = CharField(default="")
    userType = IntegerField(-1)
    userName = CharField(default="")
    status = IntegerField(default=UserStatus.UNKNOWN)

    class Meta:
        db_table = 'users'
        database = db


class Registrations(Model):
    id = AutoField(unique=True, null=False)
    eventId = ForeignKeyField(Events, backref='events')
    userId = ForeignKeyField(Users, backref='users')
    active = IntegerField()

    class Meta:
        db_table = 'registrations'
        database = db


# DB functions
def add_event(name="", owner="", start_dt="", start_time="",
              duration="", description="", event_status=EventStatus.UNKNOWN):
    Events.create(
        name=name,
        owner=owner,
        start_dt=start_dt,
        start_time=start_time,
        duration=duration,
        description=description,
        event_status=event_status
    )

    return True


def add_user(id, name="", userType=UserType.UNKNOWN, userName="", status=UserStatus.UNKNOWN):
    Users.create(
        id=id,
        name=name,
        userType=userType,
        userName=userName,
        status=status
    )

    return True


def add_registration(eventId=0, userId=0, active=RegistrationStatus.INACTIVE):
    app = Registrations.create(
        eventId=eventId,
        userId=userId,
        active=active
    )
    app.save()
    return True


def get_table(Class):
    app_table = (Class.select())
    return app_table


def registered(id):
    users = get_table(Users)

    for line in users:
        if line.id == id:
            return True

    return False


def checkAdminStatus(id):
    users = get_table(Users)

    for line in users:
        if line.id == id and line.userType == UserType.ADMIN:
            return True

    return False


def getEvent(id):
    new_table = Events.select().where(Events.id == id).execute()

    return new_table


def deleteEvent(id):
    Events.delete().where(Events.id == id).execute()
    return 0


def giveAdminStatus(id, password=""):
    if password == magicWord:
        query = Users.update(userType=UserType.ADMIN).where((Users.id == id))
        query.execute()
        return True
    else:
        return False


def giveGuestStatus(id):
    query = Users.update(userType=UserType.GUEST).where((Users.id == id))
    query.execute()


def fillUserFIO(id, FIO):
    users_table = get_table(Users)
    for user in users_table:
        if user.id == id:
            user.name = FIO
            user.status = UserStatus.REGISTRATED
            user.save()
            return 0
    return -1


def getUserType(id) -> int:
    query = Users.get_by_id(id)
    return query.userType


def getUserName(id) -> str:
    query = Users.get_by_id(id)
    return query.name


def getTodayEvents() -> str:
    today = date.today().strftime(dateFormat)
    return selectValidEventForTheDay(today)


# возвращает ивенты текущей недели
def getWeekEvents() -> [str]:
    dates = getThisWeekDates()

    events = [None for i in range(0, 7)]
    for i in range(0, 7):
        events[i] = selectValidEventForTheDay(dates[i])
        if events[i] is None or events[i] == "":
            events[i] = reply_nothing_found

    return events


# true on success
def addRegistrationOnEvent(event_id, user_id) -> bool:
    try:
        Registrations.get(Registrations.eventId == event_id,
                          Registrations.userId == user_id,
                          Registrations.active == RegistrationStatus.ACTIVE)
    except:
        add_registration(event_id, user_id, RegistrationStatus.ACTIVE)
        return True

    return False


# true on success
def calncelRegistrationOnEvent(event_id, user_id) -> bool:
    try:
        print(event_id, user_id)
        Registrations.get(Registrations.eventId == event_id,
                          Registrations.userId == user_id,
                          Registrations.active == RegistrationStatus.ACTIVE)

        Registrations.update(active=RegistrationStatus.INACTIVE) \
            .where(Registrations.eventId == event_id,
                   Registrations.userId == user_id,
                   Registrations.active == RegistrationStatus.ACTIVE).execute()
        return True
    except Exception as e:
        print(str(e))
        return False


# возвращает aктивные ивенты на неделю вперед не более %maxAmount
def getActiveWeekUpfrontEvents(maxAmount) -> [dict]:
    dates = getWeekUpfrontDates()
    eventNames = []
    for date in dates:
        eventNames.append(selectEventNamesForTheDay(date))
        if len(eventNames) >= maxAmount:
            eventNames = eventNames[0:maxAmount]
            break

    eventNames = [item for sublist in eventNames for item in sublist]
    return eventNames


# возвращает все ивенты на неделю вперед не более %maxAmount
def getAllWeekUpfrontEvents(maxAmount) -> [dict]:
    dates = getWeekUpfrontDates()
    eventNames = []
    for date in dates:
        eventNames.append(selectEventNamesForTheDay(date, status=EventStatus.UNKNOWN))
        if len(eventNames) >= maxAmount:
            eventNames = eventNames[0:maxAmount]
            break

    eventNames = [item for sublist in eventNames for item in sublist]
    return eventNames


def getRegistratedStatsForGivenMonth(month):
    today = date.today()
    firstDay = datetime(today.year, int(month), 1)
    lastDay = firstDay + timedelta(weeks=4) - timedelta(days=1)

    firstDay = firstDay.strftime(dateFormat)
    lastDay = lastDay.strftime(dateFormat)

    print("1 ", firstDay, "2 ", lastDay)
    events = selectStatsForGivenMonth(firstDay, lastDay)
    return events


def selectValidEventForTheDay(day):
    todayEvents = Events.select().where(Events.start_dt == day, Events.event_status == EventStatus.GOINGTO).execute()
    events = []
    for line in todayEvents:
        events.append(reply_event_markup.format(line.name, line.start_dt,
                                                line.start_time, line.duration, line.owner, line.description))
    return '\n'.join(events)


def selectEventNamesForTheDay(day, status=EventStatus.GOINGTO):
    if status != EventStatus.UNKNOWN:
        todayEvents = Events.select().where(Events.start_dt == day, Events.event_status == status).execute()
    else:
        todayEvents = Events.select().where(Events.start_dt == day).execute()
    events = []
    for line in todayEvents:
        event = {"id": line.id,
                 "name": line.name,
                 "start_dt": line.start_dt,
                 "status": line.event_status,
                 "owner": line.owner,
                 "description": line.description,
                 "start_time": str(line.start_time)}
        events.append(event)

    return events


def selectStatsForGivenMonth(firstDay, lastDay) -> [dict]:
    query = (Registrations
             .select(Events.id,
                     Events.name,
                     fn.Sum(Case(None, ((Registrations.active == RegistrationStatus.ACTIVE, 1),), 0)).alias(
                         'count_active'),
                     fn.Sum(Case(None, ((Registrations.active == RegistrationStatus.INACTIVE, 1),), 0)).alias(
                         'count_inactive'))
             .join(Events)
             .group_by(Events.id, Events.name)
             .where(Events.start_dt >= firstDay, Events.start_dt <= lastDay))

    agg = []
    for line in query:
        agg.append({"id": line.eventId.id, "name": line.eventId.name,
                    "count_active": line.count_active, "count_inactive": line.count_inactive})

    return agg


# возвращает по айдишнику активные реги клиента позже сегодняшней даты
def getUserActiveRegistratedEvents(id, maxAmount) -> [dict]:
    eventNames = selectUserActiveRegistratedEvents(id)
    if len(eventNames) >= maxAmount:
        eventNames = eventNames[0:maxAmount]

    return eventNames


def selectUserActiveRegistratedEvents(id):
    today = date.today()
    query = (Registrations
             .select(Registrations.id, Events.name, Events.id, Registrations.eventId)
             .join(Events)
             .where(Registrations.userId == id,
                    Events.start_dt.year >= today.year,
                    Events.start_dt.month >= today.month,
                    Events.start_dt.day >= today.day,
                    Registrations.active == RegistrationStatus.ACTIVE))

    events = []
    for line in query:
        event = {"id": line.id,
                 "name": line.eventId.name,
                 "eventId": line.eventId.id
                 }
        # print("line", event)
        events.append(event)

    return events


def changeRegistrationStatus():
    query = Registrations.update(id=id).where((Users.id == id))
    query.execute()


def loadSomeEvents():
    add_event("🕺 dickскотека", "@daniil_toro", "08-09-2021", "10:00", "4 часа",
              "Оч крутая дискотека с тусичем и пивом", EventStatus.GOINGTO)
    add_event("☕ Чаепитие", "@daniil_toro", "25-09-2021", "21:00", "10 часов",
              "Пьем чай с шишками", EventStatus.GOINGTO)
    add_event("☕ Отмененное Чаепитие", "@utyuzhnikova", "18-09-2021", "21:00", "10 часов",
              "Пьем чай с шишками", EventStatus.CANCELED)
    add_event("🍺 Пивопильня", "@daniil_toro", "27-09-2021", "21:00", "всю ночь еклмн",
              "Будем пить пиво всю ночь и кушать жареные пельмени", EventStatus.GOINGTO)
    add_event("💘 Блайнд-дейтинг!", "@utyuzhnikova", "25-09-2021", "21:00", "20 минуток",
              "Всем завяжут глаза и заставят встречаться друг с другом", EventStatus.GOINGTO)
    add_event("🥞 Масленица", "@kattyog", "23-09-2021", "00:00", "неделю!!",
              "Блины кушаем никого не слушаем", EventStatus.GOINGTO)
    add_event("📚 Книжный вечер", "@utyuzhnikova", "22-09-2021", "12:00", "6 часов",
              "Читаем книжки 6 часов подряд", EventStatus.CANCELED)
    add_event("👖 Своп-парти", "@daniil_toro", "22-10-2021", "09:00", "all day long",
              "Свопаемся свопами хе-хе", EventStatus.GOINGTO)
    add_event("👨‍💼 Бизнес-тренинг", "@daniil_toro", "26-10-2021", "09:00", "all day long",
              "Бизнес тренеруемся хе-хе", EventStatus.GOINGTO)


def getThisWeekDates():
    today = date(date.today().year, date.today().month, date.today().day)
    dates = [today + timedelta(days=i) for i in range(0 - today.weekday(), 7 - today.weekday())]
    dates = [i.strftime(dateFormat) for i in dates]

    return dates


def getWeekUpfrontDates():
    today = date(date.today().year, date.today().month, date.today().day)
    dates = [today + timedelta(days=i) for i in range(0, 7)]
    dates = [i.strftime(dateFormat) for i in dates]

    return dates


def selectAllFromUsers() -> [dict]:
    users_table = get_table(Users)
    users = []
    for line in users_table:
        users.append({"id": line.id, "name": line.name, "userType": line.userType, "status": line.status})

    return users


def selectAllFromRegs() -> [dict]:
    reg_table = get_table(Registrations)
    reg = []
    for line in reg_table:
        reg.append({"id": line.id, "eventId": line.eventId, "userId": line.userId, "active": line.active})

    return reg


def updateEvent(event):
    try:
        query = Events.update(name=event["name"], start_dt=event["start_dt"], start_time=event["start_time"],
                              owner=event["owner"], event_status=event["status"], description=event["description"]) \
            .where((Events.id == event["id"]))
        query.execute()

        return True
    except Exception as e:
        print(str(e))

    return False


if __name__ == "__main__":
    # db and tables init
    try:
        db.connect()
        Users.create_table()
        Events.create_table()
        Registrations.create_table()
    except InternalError as px:
        print(str(px))

    loadSomeEvents()
