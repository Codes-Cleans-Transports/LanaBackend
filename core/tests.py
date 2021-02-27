from django.test import TestCase
from core.models import *
from core.logic import *
import datetime

class CoreTestCase(TestCase):

    def now(self):
        return datetime.datetime.now()

    # This code is interly for error message visibility. 
    # We couldn't figure out which method to override to get a detailed deserialization of the objects on error
    # self.assertEquals(obj1, obj2) does everything this code does and more, but the message is unusable when something fails
    def assertEq(self, obj1, obj2):
        self.assertEquals(obj1.id, obj2.id)
        self.assertEquals(obj1.clusterId, obj2.clusterId)
        self.assertEquals(obj1.days['data'], obj2.days['data'])
        self.assertEquals(obj1.days['currentSequence'], obj2.days['currentSequence'])
        self.assertEquals(obj1.days['overFlow'], obj2.days['overFlow'])
        self.assertEquals(obj1, obj2)

    def test_MongodbSave(self):
        device = DeviceData(id = "1", clusterId = "cl1")
        device.save()
        # device.days = TimeArray()
        # device.days.data = [{'uptime': 0.1, 'date': str(datetime.datetime.now())}]
        
        # device.save()
        savedDevice = DeviceData.objects.get(id = '1')
        self.assertTrue(device == savedDevice)

    # def test_savePing(self):
    #     ping = DevicePing('1', 'cl1', 'here', self.now())
    #     savePing(ping)

    #     expected = DeviceData('1', 'cl1')

    #     received = DeviceData.objects.get(id = '1')
    #     self.assertEq(expected, device)

    def test_addPingEmpty(self):
        device = DeviceData(id = "1", clusterId = "cl1")
        addPing(device)

        expected = DeviceData(id = "1", clusterId = "cl1")
        expected.days['currentSequence'] = 1
        expected.days['data'] = [{'uptime': 100, 'date': self.now()}]

        self.assertEq(expected, device)

    def test_addPingExisting(self):
        device = DeviceData(id = "1", clusterId = "cl1")
        device.days['currentSequence'] = 1
        device.days['data'] = [{'uptime': 100, 'date': self.now()}]
        
        addPing(device)

        expected = DeviceData(id = "1", clusterId = "cl1")
        expected.days['currentSequence'] = 2
        expected.days['data'] = [{'uptime': 100, 'date': self.now()}, {'uptime': 100, 'date': self.now()}]

        self.assertEq(expected, device)


    def test_addPingRemovesIfFull(self):
        device = DeviceData(id = "1", clusterId = "cl1")
        device.days['currentSequence'] = 10
        data = [{'uptime': 100, 'date': self.now()}] * 10
        device.days['data'] = data
        
        addPing(device)

        expected = DeviceData(id = "1", clusterId = "cl1")
        expected.days['currentSequence'] = 1
        expected.days['data'] = data.append({'uptime': 100, 'date': self.now()})

        self.assertEq(expected, device)
