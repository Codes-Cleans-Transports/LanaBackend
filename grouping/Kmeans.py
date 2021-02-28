import math

import numpy
from sklearn.cluster import KMeans


def get_clusters(nodes: [], k):
    # Fix circular import
    from core.logic import Node

    kmean = KMeans(n_clusters=k)
    locations = []
    for i in nodes:
        location = [i.x, i.y]
        locations.append(location)
    kmean.fit(locations)
    clusters_sum = numpy.ones(k)
    clusters_number = numpy.ones(k)
    cluster_uptime = numpy.ones(k)
    cluster_radius = numpy.ones(k)
    cluster_children = []

    for i in range(k):
        cluster_children.append([])

    for i in range(len(nodes)):
        clusters_sum[kmean.labels_[i]] += nodes[i].average_uptime
        clusters_number[kmean.labels_[i]] += 1
        cluster_children[kmean.labels_[i]] = []
        if not nodes[i].children:
            cluster_children[kmean.labels_[i]].append(nodes[i])
        else:
            cluster_children[kmean.labels_[i]] += nodes[i].children
        x1 = locations[i][0]
        y1 = locations[i][1]
        x2 = kmean.cluster_centers_[kmean.labels_[i]][0]
        y2 = kmean.cluster_centers_[kmean.labels_[i]][1]
        distance = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
        if cluster_radius[kmean.labels_[i]] < distance:
            cluster_radius[kmean.labels_[i]] = distance

    for i in range(k):
        cluster_uptime[i] = clusters_sum[i] / clusters_number[i]

    final_nodes = []

    for i in range(k):
        final_nodes.append(Node(location=kmean.cluster_centers_[i],
                                average_uptime=cluster_uptime[i],
                                radius=cluster_radius[i],
                                children=cluster_children[i],
                                ))

    return final_nodes
