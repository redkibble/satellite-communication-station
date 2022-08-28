# Orbit Predictor
This program can help predict next pass of the sattelite over the given observer location. It also gives other details about aos, los and tca.
```
AOS stands for Acquisition of Signal (or Satellite). AOS is the time that a satellite rises above the horizon of an observer.
TCA stands for Time of Closest Approach. This is the time when the satellite is closest to the observer and when Doppler shift is zero. This usually corresponds to the time that the satellite reaches maximum elevation above the horizon.
LOS stands for Loss of Signal (or Satellite). LOS is the time that a satellite passes below the observer’s horizon.
```

## Usage
**Install dependencies**
```
pip install -r requirements.txt
```

### Run the program
**Run API Server**

```
# Generate prisma db andmigration
prisma generate
prisma db push

# Run the app
uvicorn api.main:app
# http://127.0.0.1:8000 
```

**Run example1.py**
```Shell
python3 example1.py
```

By default it'll look for shakuntala sattelite and observer(Ground stattion) location as Hyderabad. 
You can change in orbit-predictor.py in the end. 

