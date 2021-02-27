from django.test import TestCase
from core.models import *
from core.logic import *
import datetime
from datetime import timedelta

import copy

from unittest import mock

class CoreTestCase(TestCase):

    # This code is interly for error message visibility. 
    # We couldn't figure out which method to override to get a detailed deserialization of the objects on error
    # self.assertEquals(obj1, obj2) does everything this code does and more, but the message is unusable when something fails
    def assertEq(self, obj1, obj2):
        self.assertEquals(obj1.id, obj2.id)
        self.assertEquals(obj1.clusterId, obj2.clusterId)
        for i in range(0, len(obj1.buckets)):
            self.assertEquals(obj1.buckets[i]['data'], obj2.buckets[i]['data'])
            self.assertEquals(obj1.buckets[i]['currentSequence'], obj2.buckets[i]['currentSequence'])
            self.assertEquals(obj1.buckets[i]['overflow'], obj2.buckets[i]['overflow'])
            self.assertEquals(obj1.buckets[i]['maxSize'], obj2.buckets[i]['maxSize'])

        self.assertEquals(obj1, obj2)

    def test_MongodbSave(self):
        device = DeviceData(id = "1", clusterId = "cl1")
        device.save()
        # device.buckets[0] = TimeArray()
        # device.buckets[0].data = [{'uptime': 0.1, 'date': str(datetime.datetime.now())}]
        
        # device.save()
        savedDevice = DeviceData.objects.get(id = '1')
        self.assertTrue(device == savedDevice)

    # def test_savePing(self):
    #     ping = DevicePing('1', 'cl1', 'here', current_time)
    #     savePing(ping)

    #     expected = DeviceData('1', 'cl1')

    #     received = DeviceData.objects.get(id = '1')
    #     self.assertEq(expected, device)

    @mock.patch("core.logic.datetime") 
    def test_addPingEmpty(self, datetime_mock):
        current_time = datetime.datetime.now()
        datetime_mock.now.return_value = current_time

        device = DeviceData(id = "1", clusterId = "cl1")


        addPing(device)


        expected = DeviceData(id = "1", clusterId = "cl1")
        expected.buckets[0]['currentSequence'] = 1
        expected.buckets[0]['data'] = [{'uptime': 100, 'date': current_time}]

        self.assertEq(expected, device)

    @mock.patch("core.logic.datetime")
    def test_addPingExisting(self, datetime_mock):
        current_time = datetime.datetime.now()
        datetime_mock.now.return_value = current_time

        device = DeviceData(id = "1", clusterId = "cl1")
        device.buckets[0]['currentSequence'] = 1
        device.buckets[0]['data'] = [{'uptime': 100, 'date': current_time}]
        

        addPing(device)


        expected = DeviceData(id = "1", clusterId = "cl1")
        expected.buckets[0]['currentSequence'] = 2
        expected.buckets[0]['data'] = [{'uptime': 100, 'date': current_time}, {'uptime': 100, 'date': current_time}]

        self.assertEq(expected, device)

    @mock.patch("core.logic.datetime")
    def test_addPingRemovesIfFull(self, datetime_mock):
        current_time = datetime.datetime.now()
        datetime_mock.now.return_value = current_time

        device = DeviceData(id = "1", clusterId = "cl1")
        maxSize = device.buckets[0]['maxSize']
        data = [{'uptime': 100, 'date': current_time}] * maxSize
        device.buckets[0]['data'] = copy.deepcopy(data)


        addPing(device)


        del data[0]
        data.append({'uptime': 100, 'date': current_time})
        expected = DeviceData(id = "1", clusterId = "cl1")
        expected.buckets[0]['currentSequence'] = 1
        expected.buckets[0]['data'] = data

        self.assertEq(expected, device)


    @mock.patch("core.logic.datetime")
    def test_addPingOverflows(self, datetime_mock):
        current_time = datetime.datetime.now()
        datetime_mock.now.return_value = current_time

        device = DeviceData(id = "1", clusterId = "cl1")
        overflow = device.buckets[0]['overflow']
        device.buckets[0]['currentSequence'] = overflow - 1
        data = [{'uptime': 100, 'date': current_time}] * (overflow - 1)
        device.buckets[0]['data'] = copy.deepcopy(data)
        

        addPing(device)


        data.append({'uptime': 100, 'date': current_time})
        expected = DeviceData(id = "1", clusterId = "cl1")

        expected.buckets[0]['currentSequence'] = 0
        expected.buckets[0]['data'] = data
        expected.buckets[1]['currentSequence'] = 1
        expected.buckets[1]['data'] = [{'uptime': 100, 'date': current_time}]

        self.assertEq(expected, device)

    @mock.patch("core.logic.datetime")
    def test_addPingOverflowsMultipleBuckets(self, datetime_mock):
        current_time = datetime.datetime.now()
        datetime_mock.now.return_value = current_time

        device = DeviceData(id = "1", clusterId = "cl1")

        overflowFirstBucket = device.buckets[0]['overflow']
        data = [{'uptime': 100, 'date': current_time}] * (overflowFirstBucket - 1)
        device.buckets[0]['currentSequence'] = overflowFirstBucket - 1
        device.buckets[0]['data'] = copy.deepcopy(data)

        overflowSecondBucket = device.buckets[1]['overflow']
        data = [{'uptime': 100, 'date': current_time}] * (overflowSecondBucket - 1)
        device.buckets[1]['currentSequence'] = overflowSecondBucket - 1
        device.buckets[1]['data'] = copy.deepcopy(data)
        

        addPing(device)


        data.append({'uptime': 100, 'date': current_time})
        expected = DeviceData(id = "1", clusterId = "cl1")
        expected.buckets[0]['currentSequence'] = 0
        expected.buckets[0]['data'] = data
        expected.buckets[1]['currentSequence'] = 0
        expected.buckets[1]['data'] = data
        expected.buckets[2]['currentSequence'] = 1
        expected.buckets[2]['data'] = [{'uptime': 100, 'date': current_time}]

        self.assertEq(expected, device)


    @mock.patch("core.logic.datetime")
    def test_addMissingPings(self, datetime_mock):
        current_time = datetime.datetime.now()
        datetime_mock.now.return_value = current_time

        device = DeviceData(id = "1", clusterId = "cl1")

        overflowFirstBucket = device.buckets[0]['overflow']
        data = [{'uptime': 100, 'date': current_time}] * (overflowFirstBucket - 1)
        device.buckets[0]['currentSequence'] = overflowFirstBucket - 1
        device.buckets[0]['data'] = copy.deepcopy(data)

        overflowSecondBucket = device.buckets[1]['overflow']
        data = [{'uptime': 100, 'date': current_time}] * (overflowSecondBucket - 1)
        device.buckets[1]['currentSequence'] = overflowSecondBucket - 1
        device.buckets[1]['data'] = copy.deepcopy(data)
        

        addPing(device)


        data.append({'uptime': 100, 'date': current_time})
        expected = DeviceData(id = "1", clusterId = "cl1")
        expected.buckets[0]['currentSequence'] = 0
        expected.buckets[0]['data'] = data
        expected.buckets[1]['currentSequence'] = 0
        expected.buckets[1]['data'] = data
        expected.buckets[2]['currentSequence'] = 1
        expected.buckets[2]['data'] = [{'uptime': 100, 'date': current_time}]

        self.assertEq(expected, device)
