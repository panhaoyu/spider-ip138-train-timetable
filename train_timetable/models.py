from django.db import models


# Create your models here.

class Province(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)


class Station(models.Model):
    province = models.ForeignKey(Province, models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)


class Train(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)


class Timetable(models.Model):
    train = models.ForeignKey(Train, models.CASCADE)
    station = models.ForeignKey(Station, models.CASCADE)
    arrive = models.CharField(max_length=20)
    leave = models.CharField(max_length=20)
