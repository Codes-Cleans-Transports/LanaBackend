from djongo import models
from django import forms
import json

from neomodel import *


class TimeData(models.Model):
    uptime = models.DecimalField()
    date = models.DateTimeField()

    class Meta:
        abstract = True


class TimeArray(models.Model):
    currentSequence = models.IntegerField(default=0)
    overFlow = models.IntegerField(default=10)
    data = models.ArrayField(
        model_container=TimeData
    )

    class Meta:
        abstract = True


class DeviceData(models.Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.days = {"currentSequence": 0, "overFlow": 10, "data": []}

    def __eq__(self, obj):
        return \
            isinstance(obj, DeviceData) and \
            obj.id == self.id and \
            obj.clusterId == self.clusterId and \
            obj.days == self.days and \
            obj.months == self.months

    id = models.CharField(max_length=255, primary_key=True)
    clusterId = models.CharField(max_length=255)
    days = models.EmbeddedField(
        model_container=TimeArray
    )
    months = models.EmbeddedField(
        model_container=TimeArray
    )


class ClusterOwnershipRel(StructuredRel):
    pass


class Device(StructuredNode):
    last_hour_uptime = FloatProperty(default=100)

    location = []

    parent_cluster = Relationship('Cluster', 'PARENTS', model=ClusterOwnershipRel)


class Cluster(StructuredNode):
    def __init__(self, average_uptime, location, radius):
        average_uptime = average_uptime
        location = location
        radius = radius

    parent_cluster = Relationship('Cluster', 'PARENTS', model=ClusterOwnershipRel)
