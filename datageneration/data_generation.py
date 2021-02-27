from random import random

from core.models import DeviceData

sofia_points = 486
varna_points = 236
burgas_points = 208


def generate_data():
    return [generate_sofia_data(), generate_varna_data(), generate_burgas_data()]


def generate_sofia_data():
    sofia_local_data = generate_sofia_location_data()
    sofia_bucket_data = [[0 for x in range(40)] for y in range(sofia_points)]
    for i in range(sofia_points):
        for j in range(40):
            sofia_bucket_data[i].append(random() * 100)
    sofia_data = []
    for i in range(sofia_points):
        sofia_data.append(DeviceData(id=1,
                                     clusterId=1,
                                     buckets=sofia_bucket_data[i],
                                     location=sofia_local_data[i]
                                     ))
    return sofia_data


def generate_varna_data():
    varna_local_data = generate_varna_location_data()
    varna_bucket_data = [[0 for x in range(40)] for y in range(varna_points)]
    for i in range(varna_points):
        for j in range(40):
            varna_bucket_data[i].append(random() * 100)
    varna_data = []
    for i in range(varna_points):
        varna_data.append(DeviceData(id=1,
                                     clusterId=1,
                                     buckets=varna_bucket_data[i],
                                     location=varna_local_data[i]
                                     ))
    return varna_data


def generate_burgas_data():
    burgas_local_data = generate_burgas_location_data()
    burgas_bucket_data = [[0 for x in range(40)] for y in range(burgas_points)]
    for i in range(burgas_points):
        for j in range(40):
            burgas_bucket_data[i].append(random() * 100)
    burgas_data = []
    for i in range(burgas_points):
        burgas_data.append(DeviceData(id=1,
                                      clusterId=1,
                                      buckets=burgas_bucket_data[i],
                                      location=burgas_local_data[i]
                                      ))
    return burgas_data


def generate_sofia_location_data():
    sofia_data = []
    current_x = 0
    current_y = 0
    serdika = (42.697684, 23.321857)
    for i in range(sofia_points):
        current_x += 7 / 100 / 486
        current_y += 9 / 100 / 486
        sofia_data.append((serdika[0] + current_x, serdika[1] + current_y))
        sofia_data.append((serdika[0] - current_x, serdika[1] - current_y))
    return sofia_data


def generate_varna_location_data():
    varna_data = []
    current_x = 0
    current_y = 0
    grand_mall = (43.217821, 27.902738)
    for i in range(varna_points):
        current_x += 1 / 100 / 236
        current_y += 1 / 100 / 236
        varna_data.append((grand_mall[0] + current_x, grand_mall[1] + current_y))
        varna_data.append((grand_mall[0] - current_x, grand_mall[1] - current_y))
    return varna_data


def generate_burgas_location_data():
    burgas_data = []
    current_x = 0
    current_y = 0
    aqua = (42.511620, 27.465627)
    for i in range(burgas_points):
        current_x += 2 / 100 / 208
        current_y += 1 / 100 / 208
        burgas_data.append((aqua[0] + current_x, aqua[1] + current_y))
        burgas_data.append((aqua[0] - current_x, aqua[1] - current_y))
    return burgas_data
