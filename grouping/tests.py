from django.test import TestCase
from matplotlib import pyplot as plt

from grouping.Kmeans import get_clusters
from grouping.models import Device


# Create your tests here.


def test_KMeans():
    devices = []
    for i in range(20):
        devices.append(Device(location=(i * i, i * i + 1), average_uptime=100 - i * 2))
    clusters = get_clusters(devices, 8)
    x = []
    y = []
    for i in clusters:
        x.append(i.location[0])
        y.append(i.location[1])
    plt.scatter(x, y, s=7)
