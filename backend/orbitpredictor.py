import math
from orbit_predictor.sources import EtcTLESource
from os import path
import os
import transforms
import datetime as dt
import time
import requests
from api.prisma import prisma

# TLESource = None
TLEDateFile = "tle.txt"
TLES_DIRECTORY = path.join(os.path.dirname(os.path.realpath(__file__)), "tles")
GS_NAME, GS_LAT, GS_LNG, GS_ELE = "GS1", 17.3850, 78.4867, 542

def download_tles():
    """
    Download the TLEs from the internet.
    download from http://celestrak.com/NORAD/elements/active.txt and store it in TLEDateFile
    """
    url = "http://celestrak.com/NORAD/elements/active.txt"
    r = requests.get(url)
    with open(TLEDateFile, "w") as f:
        # Clean the downloaded text. 
        text = r.text
        text = text.replace("\r\n", "\n").replace("/", " ")
        f.write(text)
        f.close()
   
    

def init():
    """
    Initialize the predictor.
    """
    # global TLESource
    # TLESource = EtcTLESource(filename=TLEDateFile)


def get_look_angles_of_sat(observer,position):
    '''
    The transforms package was taken from another javascript library, so it follows slightly different conventsion
    So, we have little wierd things below, but later we can convert transforms package to follow simmilar conventions. 
    '''
    observerGeodetic = {
        "longitude": transforms.degreesToRadians(observer.longitude_deg),
        "latitude": transforms.degreesToRadians(observer.latitude_deg),
        "height": observer.elevation_m/1000
    }
    satelliteEcf = {"x": position.position_ecef[0], "y": position.position_ecef[1], "z": position.position_ecef[2]}
    lookAngles = transforms.ecfToLookAngles(observerGeodetic, satelliteEcf)
    lookAngles = {
        "azimuth": transforms.radiansToDegrees(lookAngles["azimuth"]),
        "elevation": transforms.radiansToDegrees(lookAngles["elevation"]),
        "rangeSat": lookAngles["rangeSat"],
    }
    return lookAngles

def get_position_at_time(predictor, time):
    """
    Get the position of the satellite at the given time.
    """
    position = predictor.get_position(time)
    return position

def predict_next_visible_orbit(sat, observer, after_when = None):
    """
    Predict the next visible orbit of the satellite. Given sattelite name and observer location.
    """
    TLESource = EtcTLESource(filename=path.join(TLES_DIRECTORY,sat + ".txt"))
    predictor = TLESource.get_predictor(sat)
    predicted_pass = predictor.get_next_pass(observer,after_when)
    return {"predictor": predictor, "aos": predicted_pass.aos, "los": predicted_pass.los, "tca": predicted_pass.max_elevation_date}

def predict_next_visible_orbits(sat, observer, duration = 86400, after_when = None):
    """
    Predict all next visible orbit of the satellite for the given duration. Given sattelite name and observer location.
    """
    TLESource = EtcTLESource(filename=path.join(TLES_DIRECTORY,sat + ".txt"))
    predictor = TLESource.get_predictor(sat)
    predicted_passes = []
    while True:
        predicted_pass = predictor.get_next_pass(observer,after_when)
        after_when = predicted_pass.los
        if predicted_pass.los > dt.datetime.now() + dt.timedelta(seconds=duration):
            break
        predicted_passes.append({
            "sate_id": predicted_pass.sate_id,
            "aos": predicted_pass.aos,
            "los": predicted_pass.los,
            "duration_s": predicted_pass.duration_s,
            "max_elevation_date": predicted_pass.max_elevation_date,
            "max_elevation_deg": predicted_pass.max_elevation_deg,
            "max_elevation_position": predicted_pass.max_elevation_position,
        })
    return predicted_passes

def break_tles():
    """
    Break the TLEs into multiple files.
    """
    with open(TLEDateFile, "r") as f:
        lines = f.readlines()
        print(len(lines))
        for i in range(0, len(lines) - 3, 3):
            filename = path.join(TLES_DIRECTORY,lines[i].strip().replace("\\", " ").replace("/", " ") + ".txt")
            with open( filename, "w") as fd:
                fd.write("\n".join([lines[i].strip(), lines[i+1].strip(), lines[i+2].strip()]))
                fd.close()

async def update_sats_in_db():
    """
    Update the sattelites in the database.
    """
    sattelites = []
    await prisma.connect()
    for filename in os.listdir(TLES_DIRECTORY):
        if filename.endswith(".txt"):
            sattelites.append(filename.split(".")[0])
    for sattelite in sattelites:
        try:
            TLESource = EtcTLESource(filename=path.join(
                TLES_DIRECTORY, sattelite + ".txt"))
            predictor = TLESource.get_predictor(sattelite)
            sat = {
                        'name': sattelite,
                        'noradid': predictor.sate_id,
                        'period': predictor.period,
            }
            result = await prisma.satellite.upsert(
                where={
                    'name': sattelite
                },
                data={
                    'create': sat,
                    'update': sat
                }
            )
        except Exception as e:
            print("Error: " + sattelite + e.__str__())
    await prisma.disconnect()

def doppler_factor(observer_ecf, satellite_ecf, velocity_ecf):
    """
    Calculate the Doppler factor of the satellite.
    Code taken from
    https://github.com/shashwatak/satellite-js/blob/develop/src/dopplerFactor.js
    """
    mfactor = 7.292115E-5;
    c = 299792.458 # Speed of light in km/s

    range = {
        'x': satellite_ecf[0] - observer_ecf[0],
        'y': satellite_ecf[1] - observer_ecf[1],
        'z': satellite_ecf[2] - observer_ecf[2],
    };
    range['w'] = math.sqrt(range['x'] ** 2 + range['y'] ** 2 + range['z'] ** 2);

    rangeVel = {
        'x': velocity_ecf[0] + mfactor * observer_ecf[1],
        'y':velocity_ecf[1] - mfactor * observer_ecf[0],
        'z':velocity_ecf[2],
    };

    def sign(value):
        return 1 if value >= 0 else -1;

    rangeRate = (range['x'] * rangeVel['x'] + range['y'] * rangeVel['y'] + range['z'] * rangeVel['z']) / range['w'];
    return (1 + (rangeRate / c) * sign(rangeRate));

# Public Function
def predict_sattelite(sattelite, observer):
    """
    Predict the next visible orbit of the satellite. Given sattelite name and observer location.
    """
    prediction = predict_next_visible_orbit(sattelite,observer)

    aosPosition = get_position_at_time(prediction["predictor"], prediction["aos"])
    losPosition = get_position_at_time(prediction["predictor"], prediction["los"])
    tcaPosition = get_position_at_time(prediction["predictor"], prediction["tca"])
    lookAnglesAos = get_look_angles_of_sat(observer, aosPosition)
    lookAnglesLos = get_look_angles_of_sat(observer, losPosition)
    lookAnglesTca = get_look_angles_of_sat(observer, tcaPosition)
    

    return {
        "sattelite": sattelite,
        "aos": {
            "time": prediction["aos"],
            "position": aosPosition,
            "lookAngles": lookAnglesAos
        },
        "los": {
            "time": prediction["los"],
            "position": losPosition,
            "lookAngles": lookAnglesLos
        },
        "tca": {
            "time": prediction["tca"],
            "position": tcaPosition,
            "lookAngles": lookAnglesTca
        }
    }
# Public Function
def follow_sattelite(sattelite, observer, seconds = 5):
    """
    Follow the sattelite position. 
    """
    TLESource = EtcTLESource(filename=path.join(TLES_DIRECTORY,sattelite + ".txt"))
    predictor = TLESource.get_predictor(sattelite)
    while True:
        print(1)
        position = get_position_at_time(predictor, dt.datetime.utcnow())
        lookAngles = get_look_angles_of_sat(observer, position)
        doppler = doppler_factor(observer.position_ecef, position.position_ecef, position.velocity_ecef)
        print(position.position_llh, lookAngles, doppler)
        time.sleep(seconds)

# Piblic Function
async def refresh_tles():
    """
    Refresh the TLEs.
    """
    download_tles()
    break_tles()
    await update_sats_in_db()

# Public Function 
def get_all_visible_sattelites(observer):
    """
    Get all visible sattelites.
    """
    sattelites = []
    visible_sattelites = []
    for filename in os.listdir(TLES_DIRECTORY):
        if filename.endswith(".txt"):
            sattelites.append(filename.split(".")[0])
    for sattelite in sattelites:
        try:
            TLESource = EtcTLESource(filename=path.join(TLES_DIRECTORY,sattelite + ".txt"))
            predictor = TLESource.get_predictor(sattelite)
            position = get_position_at_time(predictor, dt.datetime.utcnow())
            if observer.is_visible(position):
                visible_sattelites.append({"sat": sattelite, "pos": position})
        except:
            print("Error: " + sattelite)
    return visible_sattelites


# If this is the module called directly
if __name__ == "__main__":
    pass




