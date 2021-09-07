from peewee import *

# DB
db = SqliteDatabase('./zapis.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64})


# DB tables
class Patient(Model):
    id = PrimaryKeyField(unique=True, null=False)
    FIO = CharField()
    insurance = CharField()
    status = CharField(default=None)

    class Meta:
        db_table = 'patient'
        database = db


class Doctor(Model):
    id = PrimaryKeyField(unique=True, null=False)
    FIO = CharField()
    spec = CharField()
    status = CharField(default=None)

    class Meta:
        db_table = 'doctor'
        database = db


class Appointment(Model):
    id = AutoField(unique=True, null=False)
    docid = IntegerField(Doctor)
    patid = IntegerField(Patient)
    spec = CharField()
    year = IntegerField()
    month = IntegerField()
    day = IntegerField()
    hour = IntegerField()
    minute = CharField()

    class Meta:
        db_table = 'appointment'
        database = db


# DB functions
def add_patient(id, FIO="", insurance="", status=""):
    Patient.create(
        id=id,
        FIO=FIO,
        insurance=insurance,
        status=status
    )

    return 0


def add_doctor(id, FIO="", spec="", status=""):
    Doctor.create(
        id=id,
        FIO=FIO,
        spec=spec,
        status=status
    )

    return 0


def add_appointment(patid, spec="", docid=0, year=0, month=0, day=0, hour=0, minute=0):
    app = Appointment.create(
        patid=patid,
        spec=spec,
        docid=docid,
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute
    )
    app.save()
    return 0


def get_table(Class):
    app_table = (Class.select())
    return app_table



def get_clients_by_date(year, month, day, docid):

    new_table = Appointment.select().where(Appointment.docid == docid and
                                           Appointment.year == year and
                                           Appointment.month == month and
                                           Appointment.day == day)
    return new_table


def registered(id):
    pat = get_table(Patient)
    doc = get_table(Doctor)

    for line in pat:
        if line.id == id:
            return 'patient'

    for line in doc:
        if line.id == id:
            return 'doctor'

    return 0





def change_patient_insurance(id, insurance):
    pat_table = get_table(Patient)
    for pat in pat_table:
        if pat.id == id:
            pat.insurance = insurance
            pat.save()
            return 0
    return -1


def change_patient_status(id, status):
    pat_table = get_table(Patient)
    for pat in pat_table:
        if pat.id == id:
            pat.status = status
            pat.save()
            return 0
    return -1


def get_pat_status(id):
    pat_table = get_table(Patient)
    for pat in pat_table:
        if pat.id == id:
            return pat.status
    return -1


def change_doctor_FIO(id, FIO):
    doc_table = get_table(Doctor)
    for doc in doc_table:
        if doc.id == id:
            doc.FIO = FIO
            doc.save()
            return 0
    return -1


def change_doctor_spec(id, spec):
    doc_table = get_table(Doctor)
    for doc in doc_table:
        if doc.id == id:
            doc.spec = spec
            doc.save()
            return 0
    return -1


def change_doctor_status(id, status):
    doc_table = get_table(Doctor)
    for doc in doc_table:
        if doc.id == id:
            doc.status = status
            doc.save()
            return 0
    return -1


def get_doctor_status(id):
    doc_table = get_table(Doctor)
    for doc in doc_table:
        if doc.id == id:
            return doc.status
    return -1


if __name__ == "__main__":
    # db and tables init
    try:
        db.connect()
        Patient.create_table()
        Doctor.create_table()
        Appointment.create_table()
    except InternalError as px:
        print(str(px))

    # #Добавить пациентов
    add_patient(1, "Петрова Анна Владимировна", "1234567890")
    add_patient(2, "Куликов Игнат Степанович", "2093847473")
    add_patient(3, "Суржко Милана Романовна", "2847473093")
    add_patient(4, "Зябликов Александр Михайлович", "4093284773")
    add_patient(5, "Поздний Дмитрий Денисович", "2097473384")

    # # Добавить врачей
    add_doctor(1, "Иванов Сергей Олегович", "Офтальмолог", "3")
    add_doctor(2, "Петров Алексей Иванович", "Участковый врач", "3")
    add_doctor(3, "Полякова Томара Валерьевна", "Уролог", "3")
    add_doctor(4, "Терехова Анастасия Валерьевна", "Хирург", "3")
    add_doctor(5, "Подольский Дмитрий Анатольевич", "Акушер-гинеколог", "3")
    add_doctor(6, "Макаров Станислав Васильевич", "Оториноларинголог", "3")

    # Добавить записи
    add_appointment(patid=1, docid=324627346, year=2020, month=6, day=10, hour=10, minute=0)
    add_appointment(patid=2, docid=324627346, year=2020, month=6, day=10, hour=11, minute=0)
    add_appointment(patid=3, docid=324627346, year=2020, month=6, day=10, hour=13, minute=0)
    add_appointment(patid=4, docid=324627346, year=2020, month=6, day=10, hour=14, minute=0)
    add_appointment(patid=5, docid=324627346, year=2020, month=6, day=10, hour=16, minute=0)

    print("Patients:")
    pat = get_table(Patient)
    for line in pat:
        print(line.id, line.FIO, line.insurance, line.status)

    print("Doctors:")
    doc = get_table(Doctor)
    for line in doc:
        print(line.id, line.FIO, line.spec, line.status)

    print("Appointments:")
    table = get_table(Appointment)
    for line in table:
        print(line.id, line.patid, line.docid, line.spec, line.year, line.month, line.day, line.hour, line.minute)
