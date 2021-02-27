import datetime

class DevicePing:
    def __init__(self, id: str, clusterId: str, location: str, date: datetime):
        self.id = id
        self.clusterId = clusterId
        self.location = location
        self.date = date


def savePing(devicePing: DevicePing):
    print(devicePing)