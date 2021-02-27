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

    if(device.days['currentSequence'] == device.days['overFlow']):
        overflow(device)

def addNewSegmentToList(device, uptime):
    overflow = device.days['overFlow']
    q = deque(device.days['data'])

    if(len(q) == overflow):
        q.pop()

    data = {'uptime': 100, 'date': datetime.now()}
    q.append(data)
    device.days['currentSequence'] += 1
    device.days['data'] = list(q)

def overflow(device):
    device.days['currentSequence'] = 0

def createDevice(devicePing: DevicePing):
    return DeviceData(devicePing.id, devicePing.clusterId)
