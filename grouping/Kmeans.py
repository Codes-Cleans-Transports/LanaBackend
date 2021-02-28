import math

import numpy
# from sklearn.cluster import KMeans

from grouping.models import Cluster

from core.logic import Node


def get_clusters(devices: [], k):
    kmean = KMeans(n_clusters=k)
    locations = []
    for i in devices:
        locations.append(i.location)
    kmean.fit(locations)
    clusters_sum = numpy.ones(k)
    clusters_number = numpy.ones(k)
    cluster_uptime = numpy.ones(k)
    cluster_radius = numpy.ones(k)

    children = numpy.ones(k)
    
    for i in range(len(devices)):
        clusters_sum[kmean.labels_[i]] += devices[i].average_uptime
        clusters_number[kmean.labels_[i]] += 1
        x1 = locations[i][0]
        y1 = locations[i][1]
        x2 = kmean.cluster_centers_[kmean.labels_[i]][0]
        y2 = kmean.cluster_centers_[kmean.labels_[i]][1]
        distance = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
        if cluster_radius[kmean.labels_[i]] < distance:
            cluster_radius[kmean.labels_[i]] = distance

    for i in range(k):
        cluster_uptime[i] = clusters_sum[i] / clusters_number[i]

    nodes = []

    for i in range(k):
        nodes.append(Node(location=kmean.cluster_centers_[i],
                          average_uptime=cluster_uptime[i],
                          radius=cluster_radius[i],
                          # TODO: Fill children with nodes that belong to this new group
                          children=[]))

    return clusters
