'''
Taken from sattelitejs project
https://github.com/shashwatak/satellite-js/blob/1e6c4f0d14de5abab0d52b91a27b70028a0a0221/src/transforms.js
'''
import math
pi = math.pi
twoPi = pi * 2
deg2rad = pi / 180.0
rad2deg = 180 / pi
minutesPerDay = 1440.0
mu = 398600.5 # in km3 / s2
earthRadius = 6378.137 # in km
xke = 60.0 / math.sqrt((earthRadius * earthRadius * earthRadius) / mu)
vkmpersec = (earthRadius * xke) / 60.0
tumin = 1.0 / xke
j2 = 0.00108262998905
j3 = -0.00000253215306
j4 = -0.00000161098761
j3oj2 = j3 / j2
x2o3 = 2.0 / 3.0

def unpack(dict, *keys):
    return (dict[key] for key in keys)

def radiansToDegrees(radians):
    return radians * rad2deg


def degreesToRadians(degrees):
    return degrees * deg2rad

def degreesLat(radians):
    if radians < (-pi / 2) or radians > (pi / 2):
        raise('Latitude radians must be in range [-pi/2 pi/2].')
    return radiansToDegrees(radians)

def degreesLong(radians):
    if radians < -pi or radians > pi:
        raise('Longitude radians must be in range [-pi pi].')
    return radiansToDegrees(radians)


def radiansLat(degrees):
    if (degrees < -90 or degrees > 90):
        raise('Latitude degrees must be in range [-90 90].')
    return degreesToRadians(degrees)


def radiansLong(degrees):
    if (degrees < -180 or degrees > 180):
        raise('Longitude degrees must be in range [-180 180].')
    return degreesToRadians(degrees)


def geodeticToEcf(geodetic):
    longitude, latitude, height = unpack(
        geodetic, 'longitude', 'latitude', 'height')
    # print("geodeticToEcf", longitude, latitude, height)
    a = 6378.137
    b = 6356.7523142
    f = (a - b) / a
    e2 = ((2 * f) - (f * f))
    normal = a / \
        math.sqrt(1 - (e2 * (math.sin(latitude) * math.sin(latitude))))
    x = (normal + height) * math.cos(latitude) * math.cos(longitude)
    y = (normal + height) * math.cos(latitude) * math.sin(longitude)
    z = ((normal * (1 - e2)) + height) * math.sin(latitude)

    return {'x': x, 'y': y,
            'z': z,
            }

def eciToGeodetic(eci, gmst):
    # http:#www.celestrak.com/columns/v02n03/
    a = 6378.137
    b = 6356.7523142
    R = math.sqrt((eci["x"] * eci["x"]) + (eci["y"] * eci["y"]))
    f = (a - b) / a
    e2 = ((2 * f) - (f * f))

    longitude = math.atan2(eci["y"], eci["x"]) - gmst
    while (longitude < -pi):
        longitude += twoPi
    while (longitude > pi):
        longitude -= twoPi
    

    kmax = 20
    k = 0
    latitude = math.atan2(
    eci["z"],
    math.sqrt((eci["x"] * eci["x"]) + (eci["y"] * eci["y"])),
    )
    C = 0
    while (k < kmax):
        C = 1 / math.sqrt(1 - (e2 * (math.sin(latitude) * math.sin(latitude))))
        latitude = math.atan2(eci["z"] + (a * C * e2 * math.sin(latitude)), R)
        k += 1
    
    height = (R / math.cos(latitude)) - (a * C)
    return { 'longitude': longitude, 'latitude': latitude, 'height': height }

def ecfToEci(ecf, gmst):
    # ccar.colorado.edu/ASEN5070/handouts/coordsys.doc
    #
    # [X]     [C -S  0][X]
    # [Y]  =  [S  C  0][Y]
    # [Z]eci  [0  0  1][Z]ecf
    #
    X = (ecf["x"] * math.cos(gmst)) - (ecf["y"] * math.sin(gmst))
    Y = (ecf["x"] * (math.sin(gmst))) + (ecf["y"] * math.cos(gmst))
    Z = ecf["z"]
    return { 'x': X, 'y': Y, 'z': Z }

def eciToEcf(eci, gmst):
  # ccar.colorado.edu/ASEN5070/handouts/coordsys.doc
  #
  # [X]     [C -S  0][X]
  # [Y]  =  [S  C  0][Y]
  # [Z]eci  [0  0  1][Z]ecf
  #
  #
  # Inverse:
  # [X]     [C  S  0][X]
  # [Y]  =  [-S C  0][Y]
  # [Z]ecf  [0  0  1][Z]eci

    x = (eci["x"] * math.cos(gmst)) + (eci["y"] * math.sin(gmst))
    y = (eci["x"] * (-math.sin(gmst))) + (eci["y"] * math.cos(gmst))
    z  = eci["z"]

    return {
    'x':x,
    'y':y,
    'z':z,
    }

def topocentric(observerGeodetic, satelliteEcf):
    # http:#www.celestrak.com/columns/v02n02/
    # TS Kelso's method, except I'm using ECF frame
    # and he uses ECI.

   
    longitude, latitude = unpack(observerGeodetic, "longitude", "latitude")
    observerEcf = geodeticToEcf(observerGeodetic)
    rx = satelliteEcf["x"] - observerEcf["x"]
    ry = satelliteEcf["y"] - observerEcf["y"]
    rz = satelliteEcf["z"] - observerEcf["z"]
    topS =  (math.sin(latitude) * math.cos(longitude) * rx) + (math.sin(latitude) * math.sin(longitude) * ry)- (math.cos(latitude) * rz)
    topE = (-math.sin(longitude) * rx) + (math.cos(longitude) * ry)
    topZ = math.cos(latitude) * math.cos(longitude) * rx + math.cos(latitude) * math.sin(longitude) * ry + math.sin(latitude) * rz
    return { "topS":topS, "topE":topE, "topZ":topZ }


'''
/**
 * @param {Object} tc
 * @param {Number} tc.topS Positive horizontal vector S due south.
 * @param {Number} tc.topE Positive horizontal vector E due east.
 * @param {Number} tc.topZ Vector Z normal to the surface of the earth (up).
 * @returns {Object}
 */

'''

def topocentricToLookAngles(tc):
    topS, topE, topZ  = unpack(tc, "topS", "topE", "topZ")
    rangeSat = math.sqrt((topS * topS) + (topE * topE) + (topZ * topZ))
    El = math.asin(topZ / rangeSat)
    Az = math.atan2(-topE, topS) + pi
    # print("P1: ",El, Az)
    return {
    "azimuth": Az,
    "elevation": El,
    "rangeSat":rangeSat, # Range in km
    }

def ecfToLookAngles(observerGeodetic, satelliteEcf):
    topocentricCoords = topocentric(observerGeodetic, satelliteEcf)
    # print("topocentricCoords", topocentricCoords)
    return topocentricToLookAngles(topocentricCoords)
