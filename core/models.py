from djongo import models
from django import forms

from neomodel import *


class TimeData(models.Model):
    uptime = models.DecimalField()
    date = models.DateTimeField()
    
    class Meta:
        abstract = True

class TimeDataForm(forms.ModelForm):
    class Meta:
        model = TimeData
        fields = (
            'uptime', 'date'
        )

class TimeArray(models.Model):
    currentSequence = models.IntegerField(default=0)
    overFlow = models.IntegerField(default=10)
    data = models.ArrayField(
        model_container=TimeData,
        model_form_class=TimeDataForm
    )

    class Meta:
        abstract = True

class DeviceData(models.Model):

    # def __init__(self, id: str, clusterId: str):
    #     self.id = id
    #     self.clusterId = clusterId
    #     self.days = TimeArray()
    #     self.days.data = []
    #     self.months = TimeArray()
    #     self.months.data = []

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
