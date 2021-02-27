from datetime import datetime
from core.models import DeviceData
from collections import deque

class DevicePing:
    def __init__(self, id: str, clusterId: str, location: str, date: datetime):
        self.id = id
        self.clusterId = clusterId
        self.location = location
        self.date = date

timeBetweenPings = 60

def acceptPing(devicePing: DevicePing):
    try:
        device = DeviceData.objects.get(id = devicePing.id, clusterId = devicePing.clusterId)
    except DeviceData.DoesNotExist as _:
        device = createDevice(devicePing)

    addPing(device)
    device.save()

def addPing(device: DeviceData):
    missingDates = getMissingDates(device)
    for date in missingDates:
        addNewSegmentToList(device, date, 0, 0)
    addNewSegmentToList(device, datetime.now(), 100, 0)

    checkForOverflow(device, 0)

def addNewSegmentToList(device, time, uptime, bucket):
    maxSize = device.buckets[bucket]['maxSize']
    q = deque(device.buckets[bucket]['data'])

    if(len(q) == maxSize):
        q.pop()

    data = {'uptime': uptime, 'date': time}
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
        addNewSegmentToList(device, datetime.now(), uptime, bucket + 1)

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

def getMissingDates(device: DeviceData):
    if len(device.buckets[0]['data']) == 0:
        return []

    now = datetime.now()
    lastUpdated = device.buckets[0]['data'][0]
    elapsedTime = (now - lastUpdated['date']).total_seconds()
    missedIntervals = int(elapsedTime / timeBetweenPings)

    return generateMissingSegments(lastUpdated['date'], missedIntervals - 1)
        
def generateMissingSegments(startDate, number):
    data = []
    for i in range(0, number):
        data.append(startDate + datetime.timedelta(seconds=i * timeBetweenPings))

    return data