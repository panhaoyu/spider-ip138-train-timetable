import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spider.settings')
django.setup()

from train_timetable import models
import database

province_list = [models.Province(name=province.name, url=province.url) for province in database.Province]
models.Province.objects.bulk_create(province_list)

station_list = [
    models.Station(name=station.name, url=station.url, province_id=station.province_id)
    for station in database.Station]
models.Station.objects.bulk_create(station_list)


train_list = [models.Train(name=train.name, url=train.url) for train in database.Train]
models.Train.objects.bulk_create(train_list)

timetable_list = [
    models.Timetable(
        train_id=timetable.train_id, station_id=timetable.station_id,
        arrive=timetable.arrive, leave=timetable.leave,
    ) for timetable in database.TimeTable if isinstance(timetable.station_id, int)]
models.Timetable.objects.bulk_create(timetable_list)
