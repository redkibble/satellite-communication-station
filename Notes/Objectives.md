****## Objectives of the ground station
Given a sattelite - 
- [x] 1. When will it be visible, for how long - min to max azimuth, elevation
- [ ] 2. Trigger alert when it is visible. 
- [x] 3. Lock & Follow a sattelite - track the motion of the sattelite and accordingly rotate the antena and keep downloading the data.
- [x] 4. Find all the visible time intervals for next 24Hrs

Give a ground station - 
- [x] 1. What all sattelites are in the communication range right now. 
- [x] 2. If user selects a sattelite, show for how much more it'll be visible
- [x] 3. Lock & Follow the sattelite - track the motion of the sattelite and accordingly rotate the antena and keep downloading the data.

Given multiple ground stations (A ground station network)
- [ ] 1. Lock and follow a sattelite and tranmit/recieve data.

### API

### UI Requirements
- PyQT based prototype
- UI wireframe finalizingwith figma
- Final UI in PyQT for a desktop appliaction
- Serial communication with Rotor and Radio reciever. 


### TODO
- [] Design APIS
- [] UI wireframes
- [] Develope APIs
- [] Integrate Rotors
- [] Integrate Radios
- [] Integrate Information processing
- Depending on different sattelites


/ New thigs
- Allow users to input tle data. 
- Automate the TLE refresh
- 

### Small TODOs.
- [ ] Make API Response format consistent.
- [ ] Refresh TLEs API - handle errors.
- [x] consider elevation of gs

### APIS

**Sattelites**

- [x] GET: /sattelites - List of available sattelites

- [x] GET: /sattelites/{id} - Details of one sattelite

- [x] GET: /sattelites/{id}/observe

- [x] GET: /sattelites/{id}/passes - Predict all next passes

**Tracked Satellites**

GET: /trackedsats - List of all observed sattelites

GET: /trackedsats/{SAT_NAME} - Observed sattelite

POST: /trackedsats - Add new observation for a sattelite

POST: /trackedsats/{id}/download_data

**Data**

GET: /data/download/{download-key}

Actions: 

Webhook -> 

/api/incoming-data-from-sgcc/

**Status & Health**

GET: /sgcc/status

PUT: /sgcc/ - Update Ground station properties. 

**Antena**

GET: /antena/status

POST: /antena/move

**Radio**

GET: /radio/status
