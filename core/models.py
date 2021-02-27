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

class TimeArrayForm(forms.ModelForm):
    class Meta:
        model = TimeArray
        fields = (
            'currentSequence', 'overFlow', 'data'
        )

class DeviceData(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    clusterId = models.CharField(max_length=255)
    days = models.EmbeddedField(
        model_container=TimeArray,
        model_form_class=TimeArrayForm
    )
    months = models.EmbeddedField(
        model_container=TimeArray,
        model_form_class=TimeArrayForm
    )

class ClusterOwnershipRel(StructuredRel):
    pass

class Device(StructuredNode):
    last_hour_uptime = FloatProperty(default=100)

    parent_cluster = Relationship('Cluster', 'PARENTS', model=ClusterOwnershipRel)


class Cluster(StructuredNode):
    average_uptime = FloatProperty(default=100)

    parent_cluster = Relationship('Cluster', 'PARENTS', model=ClusterOwnershipRel)
