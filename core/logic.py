import datetime
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
    device
    # if(device.days.currentSequence + 1 >= device.days.overFlow):
    #     print("overflow")
    # else:
    #     q = dequeue(device.days.data)
    #     q.pop()

def createDevice(devicePing: DevicePing):
    return DeviceData(devicePing.id, devicePing.clusterId)
