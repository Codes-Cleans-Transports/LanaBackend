from django.test import TestCase
from core.models import *
import datetime

class CoreTestCase(TestCase):

    def test_Example(self):
        """Mongodb saves"""
        device = DeviceData(id = "1", clusterId = "cl1")
        device.days = TimeArray()
        device.days.data = [{'uptime': 0.1, 'date': str(datetime.datetime.now())}]
        print(device.days.data)
