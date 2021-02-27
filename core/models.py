from djongo import models
from django import forms

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

    parent_cluster = Relationship('Cluster', 'PARENTS', model=ClusterOwnershipRel)


class Cluster(StructuredNode):
    average_uptime = FloatProperty(default=100)

    parent_cluster = Relationship('Cluster', 'PARENTS', model=ClusterOwnershipRel)
