from database import Province, Station, Train, TimeTable, atomic

stations = [(station.name, station.id) for station in Station]
stations = dict(stations)
print(stations)

with atomic():
    for timetable in TimeTable:
        try:
            timetable.station_id = stations[timetable.station_id]
            timetable.save()
        except KeyError:
            timetable.delete()
