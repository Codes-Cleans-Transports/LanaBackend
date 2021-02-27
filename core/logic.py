from datetime import datetime
from core.models import DeviceData
from collections import deque

class DevicePing:
    def __init__(self, id: str, clusterId: str, location: str, date: datetime):
        self.id = id
        self.clusterId = clusterId
        self.location = location
        self.date = date


def savePing(devicePing: DevicePing):
    try:
        device = DeviceData.objects.get(id = devicePing.id, clusterId = devicePing.clusterId)
    except DeviceData.DoesNotExist as _:
        device = createDevice(devicePing)

    # addPing(device)
    device.save()

def addPing(device: DeviceData):
    overflow = device.days['overFlow']

    if(device.days['currentSequence'] + 1 >= overflow):
        print("overflow")
    else:
        q = deque(device.days['data'])

        if(q.count == overflow):
            q.pop()

        data = {'uptime': 100, 'date': datetime.now()}
        q.append(data)
        device.days['data'] = list(q)

def createDevice(devicePing: DevicePing):
    return DeviceData(devicePing.id, devicePing.clusterId)
