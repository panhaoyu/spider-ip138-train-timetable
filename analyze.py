import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spider.settings')
django.setup()

from train_timetable.models import *

src_province = Province.objects.filter(name__in=['贵州'])
dst_province = Province.objects.filter(name__in=['浙江'])

src_stations = Station.objects.filter(province__in=src_province)
dst_stations = Station.objects.filter(province__in=dst_province)

src_trains = Train.objects.filter(timetable__station__in=src_stations).distinct()
dst_trains = Train.objects.filter(timetable__station__in=dst_stations).distinct()
available_trains = src_trains & dst_trains
available_trains = available_trains.order_by('name')
import os

os.path.exists('result.txt') and os.remove('result.txt')
for train in available_trains:
    timetables = Timetable.objects.filter(train=train)
    timetables = [timetable.station for timetable in timetables
                  if timetable.station in src_stations | dst_stations]
    if not (timetables[0] in src_stations and timetables[-1] in dst_stations):
        continue
    timetables = [timetable.name for timetable in timetables]
    timetables = ','.join(timetables)
    with open('result.txt', mode='a', encoding='utf-8') as f:
        f.write(f'{train.name}\t{timetables}\n')
