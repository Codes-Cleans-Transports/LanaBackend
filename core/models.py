from djongo import models

from neomodel import *

class Blog(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

class Entry(models.Model):
    blog = models.EmbeddedField(
        model_container=Blog
    )    
    headline = models.CharField(max_length=255)    

class ClusterOwnershipRel(StructuredRel):
    pass

class Device(StructuredNode):
    last_hour_uptime = FloatProperty(default=100)

    parent_cluster = Relationship('Cluster', 'PARENTS', model=ClusterOwnershipRel)


class Cluster(StructuredNode):
    average_uptime = FloatProperty(default=100)

    parent_cluster = Relationship('Cluster', 'PARENTS', model=ClusterOwnershipRel)
