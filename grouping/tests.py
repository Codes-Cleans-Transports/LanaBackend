from django.test import TestCase
from matplotlib import pyplot as plt

from grouping.models import Device


# Create your tests here.


def test_KMeans():
    devices = []
    for i in range(10):
        devices.append(Device(location=(i * i, i * i + 1), average_uptime=100 - i * 2))
        locations = []
        for j in devices:
            locations.append(j.location)
        plt.scatter(locations)
        plt.show()
