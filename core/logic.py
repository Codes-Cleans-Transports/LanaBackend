from datetime import datetime
from core.models import DeviceData
from collections import deque

class DevicePing:
    def __init__(self, id: str, clusterId: str, location: str, date: datetime):
        self.id = id
        self.clusterId = clusterId
        self.location = location
        self.date = date

def acceptPing(devicePing: DevicePing):
    try:
        device = DeviceData.objects.get(id = devicePing.id, clusterId = devicePing.clusterId)
    except DeviceData.DoesNotExist as _:
        device = createDevice(devicePing)

    addPing(device)
    device.save()

def addPing(device: DeviceData):
    addNewSegmentToList(device, 100)

    if(device.buckets[0]['currentSequence'] == device.buckets[0]['overflow']):
        overflow(device)

def addNewSegmentToList(device, uptime):
    maxSize = device.buckets[0]['maxSize']
    q = deque(device.buckets[0]['data'])

    if(len(q) == maxSize):
        q.pop()

    data = {'uptime': 100, 'date': datetime.now()}
    q.append(data)
    device.buckets[0]['currentSequence'] += 1
    device.buckets[0]['data'] = list(q)

def overflow(device):
    device.buckets[0]['currentSequence'] = 0

def createDevice(devicePing: DevicePing):
    return DeviceData(devicePing.id, devicePing.clusterId)
