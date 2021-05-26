
from AirSimClient import CarClient, CarControls
import time
    
# connect to the AirSim simulator 
client = CarClient()
client.confirmConnection()
print('Connected')
client.enableApiControl(True)
car_controls = CarControls()

client.reset()

# go forward
for i in range(100000000):
    car_controls.throttle = 1.0
    car_controls.steering = 0
    client.setCarControls(car_controls)

client.enableApiControl(False)
