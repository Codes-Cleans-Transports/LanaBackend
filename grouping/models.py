from django.db import models

# Create your models here.
from neomodel import StructuredRel, StructuredNode, Relationship


class ClusterOwnershipRel(StructuredRel):
    pass


class Device(StructuredNode):
    def __init__(self, average_uptime, location):
        average_uptime = average_uptime
        location = location

    parent_cluster = Relationship('Cluster', 'PARENTS', model=ClusterOwnershipRel)


class Cluster(StructuredNode):
    def __init__(self, average_uptime, location, radius):
        average_uptime = average_uptime
        location = location
        radius = radius

    parent_cluster = Relationship('Cluster', 'PARENTS', model=ClusterOwnershipRel)