import peewee

database = peewee.SqliteDatabase('db2.sqlite3')


class Province(peewee.Model):
    class Meta:
        database = database

    name = peewee.CharField(unique=True)
    url = peewee.CharField()


class Station(peewee.Model):
    class Meta:
        database = database

    province = peewee.ForeignKeyField(Province)
    name = peewee.CharField(unique=True)
    url = peewee.CharField()


class Train(peewee.Model):
    class Meta:
        database = database

    name = peewee.CharField(unique=True)
    url = peewee.CharField()


class TimeTable(peewee.Model):
    class Meta:
        database = database

    train = peewee.ForeignKeyField(Train)
    station = peewee.ForeignKeyField(Station)
    arrive = peewee.TimeField()
    leave = peewee.TimeField()

atomic = database.atomic

if __name__ == '__main__':
    database.create_tables([
        Province,
        Station,
        Train,
        TimeTable,
    ])
