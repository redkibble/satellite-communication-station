from groundstation import GroundStation
import orbitpredictor as op
import asyncio

'''
This example shows tracking a satellite with a ground station.
'''
# Refresh TLEs every 24 hours.
# asyncio.run(op.refresh_tles())


India = GroundStation("India", 17.3850, 78.4867, 542)
Sattelite = "COMS 1"
# satelite_next_pass = op.predict_sattelite(Sattelite, India.observer)
# print(satelite_next_pass)

# # Final all next orbits during the next 24 Hrs.
# predict_next_visible_orbits = op.predict_next_visible_orbits(Sattelite, India.observer, 86400)
# print(predict_next_visible_orbits)

# # Find all visible sattelites.
# all_visible_sattelites = op.get_all_visible_sattelites(India.observer)
# print(all_visible_sattelites)

# Follow the sattelite position.
op.follow_sattelite(Sattelite, India.observer)
