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
    addNewSegmentToList(device, 100, 0)

    checkForOverflow(device, 0)

def addNewSegmentToList(device, uptime, bucket):
    maxSize = device.buckets[bucket]['maxSize']
    q = deque(device.buckets[bucket]['data'])

    if(len(q) == maxSize):
        q.pop()

    data = {'uptime': 100, 'date': datetime.now()}
    q.append(data)
    device.buckets[bucket]['currentSequence'] += 1
    device.buckets[bucket]['data'] = list(q)

def checkForOverflow(device, bucket):
    if(device.buckets[bucket]['currentSequence'] == device.buckets[bucket]['overflow']):
        overflow(device, bucket)

def overflow(device, bucket):
    # Ignore if last bucket
    if(bucket < len(device.buckets)):
        device.buckets[bucket]['currentSequence'] = 0

        uptime = getNextSegmentAvg(device, bucket)
        addNewSegmentToList(device, uptime, bucket + 1)

        checkForOverflow(device, bucket + 1)

def getNextSegmentAvg(device, bucket):
    overflow = device.buckets[bucket]['overflow']
    data = device.buckets[bucket]['data'][:overflow]
    uptime_list = list(map(lambda a : a['uptime'], data))
    average = Average(uptime_list)
    return average

def Average(lst): 
    return sum(lst) / len(lst) 

def createDevice(devicePing: DevicePing):
    return DeviceData(devicePing.id, devicePing.clusterId)
