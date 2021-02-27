import math

import numpy as np
from sklearn.cluster import KMeans

from core.models import Cluster


def get_clusters(devices, k):
    kmean = KMeans(n_clusters=k)
    locations = []
    for i in devices:
        locations.append(devices[i].location)
    kmean.fit(locations)
    clusters_sum = []
    clusters_number = []
    cluster_uptime = []
    cluster_radius = np.ones(k)
    for i in kmean.labels_:
        clusters_sum[kmean.labels_[i]] + devices[i].last_hour_uptime
        clusters_number[kmean.labels_[i]] += 1
        x1 = locations[i][0]
        y1 = locations[i][1]
        x2 = kmean.cluster_centers_[i][0]
        y2 = kmean.cluster_centers_[i][1]
        distance = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
        if cluster_radius[i] < distance:
            cluster_radius[i] = distance

    for i in range(k):
        cluster_uptime[i] = clusters_sum[i] / clusters_number[i]

    clusters = []

    for i in cluster_uptime:
        clusters.append(Cluster(location=kmean.cluster_centers_[i],
                                average_uptime=cluster_uptime[i],
                                radius=cluster_radius[i]))

    return clusters
