import math

coordinates = [
    [-7.299221268484248, 112.76742160320283],
    [-7.29898182586388, 112.76744842529298],
    [-7.298779629773526, 112.7674698829651],
    [-7.298566791684952, 112.76749134063722],
    [-7.298359274451085, 112.76751279830934],
    [-7.298178361912265, 112.76751816272737],
    [-7.297970844498225, 112.76753962039949],
    [-7.297816536615127, 112.76755034923555],
    [-7.29764094482136, 112.76758253574373],
    [-7.297529204553078, 112.76758253574373],
    [-7.297539846484597, 112.76773810386659],
    [-7.29755580938139, 112.76792585849763],
    [-7.297566451312285, 112.76809751987457],
    [-7.2975770932429, 112.76814043521883],
    [-7.297773968913876, 112.7681350708008],
    [-7.297906992966849, 112.76812434196474],
    [-7.298082584656205, 112.7681189775467],
    [-7.298098547533636, 112.7679741382599],
    [-7.298077263696935, 112.76779174804689],
]

def getDistance(origin, destination):
    # return distance in meters
    lon1 = toRadian(origin[1])
    lat1 = toRadian(origin[0])
    lon2 = toRadian(destination[1])
    lat2 = toRadian(destination[0])

    deltaLat = lat2 - lat1
    deltaLon = lon2 - lon1

    a = math.pow(math.sin(deltaLat/2), 2) + math.cos(lat1) * math.cos(lat2) * math.pow(math.sin(deltaLon/2), 2)
    c = 2 * math.asin(math.sqrt(a))
    EARTH_RADIUS = 6371

    return c * EARTH_RADIUS * 1000

def toRadian(degree):
    return degree*3.14/180

def getTotalDistance():
    result = 0
    for i in range(0, len(coordinates)-1):
        result += getDistance(coordinates[i], coordinates[i+1])
        
    return result



