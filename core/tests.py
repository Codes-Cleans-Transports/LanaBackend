from django.test import TestCase
from core.models import *
from core.logic import *
import datetime

class CoreTestCase(TestCase):

    def now(self):
        datetime.datetime.now()

    def test_Example(self):
        """Mongodb saves"""
        device = DeviceData(id = "1", clusterId = "cl1")
        # device.days = TimeArray()
        # device.days.data = [{'uptime': 0.1, 'date': str(datetime.datetime.now())}]
        
        # device.save()
        # savedDevice = DeviceData.objects.all()[0]
        # self.assertTrue(device == savedDevice)

    def test_savePing(self):
        savePing(DevicePing('1', 'cl1', 'here', self.now()))