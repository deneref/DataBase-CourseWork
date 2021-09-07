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
    start_dt = DateField()
    start_time = TimeField()
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
    eventId = IntegerField(Events)
    userId = IntegerField(Users)
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
    today = date.today()
    print(today)
    d = today.strftime(dateFormat)
    print(d)
    todayEvents = Events.select().where(Events.start_dt == d and Events.event_status == EventStatus.GOINGTO).execute()
    events = []
    for line in todayEvents:
        print(line)
        events.append(reply_event_markup.format(line.name, line.start_dt,
                                                line.start_time, line.duration, line.owner, line.description))
    return '\n'.join(events)


def loadSomeEvents():
    add_event("🕺 dickскотека", "@daniil_toro", "07-09-2021", "10:00", "4 часа",
              "Оч крутая дискотека с тусичем и пивом", EventStatus.GOINGTO)
    add_event("☕ Чаепитие", "@daniil_toro", "07-09-2021", "21:00", "10 часов",
              "Пьем чай с шишками", EventStatus.GOINGTO)
    add_event("☕ Отмененное Чаепитие", "@utyuzhnikova", "07-09-2021", "21:00", "10 часов",
              "Пьем чай с шишками", EventStatus.CANCELED)
    add_event("🍺 Пивопильня", "@daniil_toro", "08-09-2021", "21:00", "всю ночь еклмн",
              "Будем пить пиво всю ночь и кушать жареные пельмени", EventStatus.GOINGTO)
    add_event("📚 Книжный вечер", "@utyuzhnikova", "10-09-2021", "12:00", "6 часов",
              "Читаем книжки 6 часов подряд", EventStatus.CANCELED)
    add_event("👖 Своп-парти", "@daniil_toro", "10-10-2021", "09:00", "all day long",
              "Свопаемся свопами хе-хе", EventStatus.GOINGTO)
    add_event("👨‍💼 Бизнес-тренинг", "@daniil_toro", "10-10-2021", "09:00", "all day long",
              "Бизнес тренеруемся хе-хе", EventStatus.GOINGTO)


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
