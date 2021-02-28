from random import random

from core.models import DeviceData
from core.logic import addPingCustom, createDevice, DevicePing

from datetime import datetime, timedelta

sofia_points = 486
varna_points = 236
burgas_points = 208


def generate_data():
    data = generate_sofia_data() + generate_varna_data() + generate_burgas_data()
    for device in data:
        current_time = datetime.now()
        ping_uptimes = device.buckets
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

        for ping in ping_uptimes:
            addPingCustom(device, current_time, ping)
            current_time += timedelta(seconds=60)
        
        device.save()


def generate_sofia_data():
    sofia_local_data = generate_sofia_location_data()
    sofia_bucket_data = []
    for i in range(sofia_points):
        sofia_bucket_data.append([])
        for j in range(800):
            sofia_bucket_data[i].append(random() * 20 + 80)
    sofia_data = []
    for i in range(sofia_points):
        sofia_data.append(DeviceData(id=i,
                                     clusterId=1,
                                     buckets=sofia_bucket_data[i],
                                     location=sofia_local_data[i]
                                     ))
    return sofia_data


def generate_varna_data():
    varna_local_data = generate_varna_location_data()
    varna_bucket_data = []
    for i in range(varna_points):
        varna_bucket_data.append([])
        for j in range(800):
            varna_bucket_data[i].append(random() * 20 + 80)
    varna_data = []
    for i in range(varna_points):
        varna_data.append(DeviceData(id=i + sofia_points,
                                     clusterId=2,
                                     buckets=varna_bucket_data[i],
                                     location=varna_local_data[i]
                                     ))
    return varna_data


def generate_burgas_data():
    burgas_local_data = generate_burgas_location_data()
    burgas_bucket_data = [] 
    for i in range(burgas_points):
        burgas_bucket_data.append([])
        for j in range(800):
            burgas_bucket_data[i].append(random() * 20 + 80)
    burgas_data = []
    for i in range(burgas_points):
        burgas_data.append(DeviceData(id=i + sofia_points + varna_points,
                                      clusterId=3,
                                      buckets=burgas_bucket_data[i],
                                      location=burgas_local_data[i]
                                      ))
    return burgas_data


def generate_sofia_location_data():
    sofia_data = []
    serdika = (42.697684, 23.321857)
    for i in range(int(sofia_points/3)):
        sofia_data.append((serdika[0] + random() * 7 / 100, serdika[1] + random() * 9 / 100))
        sofia_data.append((serdika[0] - random() * 7 / 100, serdika[1] - random() * 9 / 100))
        sofia_data.append((serdika[0] + random() * 7 / 100, serdika[1] - random() * 9 / 100))
        sofia_data.append((serdika[0] - random() * 7 / 100, serdika[1] + random() * 9 / 100))
    return sofia_data


def generate_varna_location_data():
    varna_data = []
    grand_mall = (43.217821, 27.902738)
    for i in range(int(varna_points/3)):
        varna_data.append((grand_mall[0] + random() / 100, grand_mall[1] + random() / 100))
        varna_data.append((grand_mall[0] - random() / 100, grand_mall[1] - random() / 100))
        varna_data.append((grand_mall[0] - random() / 100, grand_mall[1] + random() / 100))
        varna_data.append((grand_mall[0] + random() / 100, grand_mall[1] - random() / 100))
    return varna_data


def generate_burgas_location_data():
    burgas_data = []
    aqua = (42.511620, 27.465627)
    for i in range(int(burgas_points/3)):
        burgas_data.append((aqua[0] + random() / 50, aqua[1] + random() / 100))
        burgas_data.append((aqua[0] - random() / 50, aqua[1] - random() / 100))
        burgas_data.append((aqua[0] + random() / 50, aqua[1] - random() / 100))
        burgas_data.append((aqua[0] - random() / 50, aqua[1] + random() / 100))
    return burgas_data
