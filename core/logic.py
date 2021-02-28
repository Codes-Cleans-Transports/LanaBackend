from datetime import datetime, timedelta
from core.models import DeviceData
from collections import deque

from grouping.Kmeans import get_clusters

from typing import List

class DevicePing:
    def __init__(self, id: str, clusterId: str, location: str):
        self.id = id
        self.clusterId = clusterId
        self.location = location

class DeviceInfo:
    def __init__(self, id: str, cluster_id: str, location: str, uptime: float):
        self.id = id
        self.cluster_id = cluster_id
        self.location = location
        self.uptime = uptime

class Node:
    # Children is a list of nodes
    def __init__(self, location: str, average_uptime: float, children, radius: int):
        self.location = tuple(map(float, location[1:][:-1].split(', ')))
        self.average_uptime = average_uptime
        self.children = children


timeBetweenPings = 60

def acceptPing(devicePing: DevicePing):
    try:
        device = DeviceData.objects.get(id = devicePing.id, clusterId = devicePing.clusterId)
        
        device.location = devicePing.location
    except DeviceData.DoesNotExist as _:
        device = createDevice(devicePing)

    addPing(device)
    device.save()

    return device

def addPing(device: DeviceData):
    missingDates = getMissingDates(device)
    for date in missingDates:
        addPingCustom(device, date, 0)

    addPingCustom(device, datetime.now(), 100)

def addPingCustom(device, time, uptime):
    addNewSegmentToList(device, time, uptime, 0)
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
    if(device.buckets[bucket]['currentSequence'] >= device.buckets[bucket]['overflow']):
        overflow(device, bucket)

def overflow(device, bucket):
    # Ignore if last bucket
    if(bucket < len(device.buckets) - 1):
        device.buckets[bucket]['currentSequence'] = 0

        nextSegmentData = getNextSegmentAvg(device, bucket)
        uptime = nextSegmentData['uptime']
        date = nextSegmentData['date']
        addNewSegmentToList(device, date, uptime, bucket + 1)

        checkForOverflow(device, bucket + 1)

def getNextSegmentAvg(device, bucket):
    overflow = device.buckets[bucket]['overflow']
    data = device.buckets[bucket]['data'][:overflow]
    uptime_list = list(map(lambda a : a['uptime'], data))
    uptime = Average(uptime_list)
    return {'uptime': uptime, 'date': device.buckets[bucket]['data'][overflow - 1]['date']}

def Average(lst): 
    return sum(lst) / len(lst) 

def createDevice(devicePing: DevicePing):
    device = DeviceData(devicePing.id, devicePing.clusterId)

    device.buckets = [ \
        # 60 seconds, overflow every hour hold up to 6 hours
        {"currentSequence": 0, "overflow": 60, "maxSize": 60*6, "data": []}, \
        # Overflow every 24 pings/hours hold up to 7 days
        {"currentSequence": 0, "overflow": 24, "maxSize": 7*24, "data": []}, \
        # Overflow every 7 pings/1 week hold up to 5 weeks
        {"currentSequence": 0, "overflow": 7, "maxSize": 7*5, "data": []}, \
        # Overflow every 4 weeks hold up to 3 months
        {"currentSequence": 0, "overflow": 4, "maxSize": 4*3, "data": []}, \
        # Overflow every 3 months hold up to a year
        {"currentSequence": 0, "overflow": 3, "maxSize": 3*4, "data": []}, \
    ]

    return device

def getDevicesByClusterAndBucketLevel(
    *,
    cluster_id: str,
    bucket_level: int 
) -> List[DeviceInfo]:
    devices = []

    # TODO: Determine if "location" is a str in the form "52.321321 32.3332312" or an object with long/lat fields
    for device in DeviceData.objects.filter(clusterId=cluster_id):
        devices.append(
            DeviceInfo(
                id=device.id,
                cluster_id=cluster_id,
                location=device.location,
                uptime=device.buckets[bucket_level]['data'][0]['uptime']
            )
        )

    return devices

def getMissingDates(device: DeviceData):
    if len(device.buckets[0]['data']) == 0:
        return []

    now = datetime.now()
    lastUpdated = device.buckets[0]['data'][0]
    elapsedTime = (now - lastUpdated['date']).total_seconds()
    missedIntervals = int(elapsedTime / timeBetweenPings)

    return generateMissingSegments(lastUpdated['date'], missedIntervals )
        
def generateMissingSegments(startDate, number):
    data = []
    for i in range(1, number + 1):
        data.append(startDate + timedelta(seconds=i * timeBetweenPings))

    return data

def getClusterGrouped(
    *,
    cluster_id: str
) -> List[Node]:
    devices = getDevicesByClusterAndBucketLevel(cluster_id=cluster_id, bucket_level=0)

    nodes = []

    for device in devices:
        nodes.append(Node(location=device.location, average_uptime=device.uptime, children=None, radius=0))

    k = len(nodes)

    for i in range(6):
        nodes = get_clusters(nodes=nodes, k=k)
        k = ceil(k/3)

    return nodes


def getClusters():
    return list(DeviceData.objects.all().values('clusterId').distinct().values_list('clusterId', flat=True))
