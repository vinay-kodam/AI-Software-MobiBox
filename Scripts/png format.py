import airsim
import cv2
import numpy as np
import os
import setup_path 
import time

# connect to the AirSim simulator 
client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()

# go forward
car_controls.throttle = 1.0
car_controls.steering = 0
client.setCarControls(car_controls)
print("Car: Going Forward")

imagequeue = []

for idx in range(5):
    filename = 'C:/Users/ACER/Documents/AirSim/png/' + str(idx)
    responses = client.simGetImages([airsim.ImageRequest("fpv", airsim.ImageType.Scene, False, False)])
    response = responses[0]
    # get numpy array
    img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) 
    # reshape array to 4 channel image array H X W X 4
    img_rgb = img1d.reshape(response.height, response.width, 3)
    # original image is fliped vertically
    #img_rgb = np.flipud(img_rgb)
    # write to png 
    airsim.write_png(os.path.normpath(filename + '.jpg'), img_rgb)
    
    # responses = client.simGetImage(1, airsim.ImageType.Scene, False)
    # imagequeue.append(responses[0].image_data_uint8)
    # #print(responses)
    # filename = 'C:/Users/ACER/Documents/AirSim/png/' + str(idx)
    # #print("Type %d, size %d" % (responses.image_type, len(responses.image_data_uint8)))
    # #airsim.write_file(os.path.normpath(filename + '.png'), responses.image_data_uint8)
    # airsim.write_file(os.path.normpath(filename + '.png' ), imagequeue[idx])
    # imagequeue.pop(0)
    time.sleep(3)
        
client.reset()
client.enableApiControl(False)