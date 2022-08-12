from orbit_predictor import locations as oploc
class GroundStation:
    def __init__(self, name, latitude, longitude, height):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.height = height
        self.observer = oploc.Location(self.name, latitude_deg=self.latitude, longitude_deg=self.longitude, elevation_m=self.height)

    def __str__(self):
        return self.name + " (" + str(self.latitude) + ", " + str(self.longitude) + ", " + str(self.height) + ")"
    