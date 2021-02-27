from django.test import TestCase
from core.models import *
from core.logic import *
import datetime

class CoreTestCase(TestCase):

    def now(self):
        datetime.datetime.now()

    def test_MongodbSave(self):
        device = DeviceData(id = "1", clusterId = "cl1")
        device.save()
        # device.days = TimeArray()
        # device.days.data = [{'uptime': 0.1, 'date': str(datetime.datetime.now())}]
        
        # device.save()
        savedDevice = DeviceData.objects.get(id = '1')
        self.assertTrue(device == savedDevice)

    def test_savePing(self):
        ping = DevicePing('1', 'cl1', 'here', self.now())
        savePing(ping)

        expected = DeviceData('1', 'cl1')

        received = DeviceData.objects.get(id = '1')
        assert expected == received