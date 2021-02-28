from djongo import models
from django import forms
import json

from neomodel import *


class TimeData(models.Model):
    uptime = models.FloatField()
    date = models.DateTimeField()

    class Meta:
        abstract = True


class TimeArray(models.Model):
    currentSequence = models.IntegerField(default=0)
    overflow = models.IntegerField(default=10)
    maxSize = models.IntegerField(default=60)
    data = models.ArrayField(
        model_container=TimeData
    )

    class Meta:
        abstract = True


class DeviceData(models.Model):

    def __eq__(self, obj):
        return \
            isinstance(obj, DeviceData) and \
            obj.id == self.id and \
            obj.clusterId == self.clusterId and \
            obj.buckets == self.buckets

    id = models.CharField(max_length=255, primary_key=True)
    clusterId = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    buckets = models.ArrayField(
        model_container=TimeArray
    )
