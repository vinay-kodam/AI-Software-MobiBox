import setup_path
import airsim
import speech_recognition as sr
#from keras.models import load_model
import sys
import numpy as np
import cv2

#if (len(sys.argv) != 2):
#    print('usage: python drive.py <modelName>')
#    sys.exit()

#print('Loading model...')
#model = load_model(sys.argv[1])

# connect to the AirSim simulator 
client = airsim.CarClient()
client.confirmConnection()
print('Client-Connected-Server')
client.enableApiControl(True)
car_controls = airsim.CarControls()

car_controls.steering = 0
car_controls.throttle = 0
car_controls.brake = 0

# image_buf = np.zeros((1, 144, 256, 3))
# state_buf = np.zeros((1,4))

# def get_image():
#     image = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])[0]
#     image1d = np.fromstring(image.image_data_uint8, dtype=np.uint8)
#     image_rgb = image1d.reshape(image.height, image.width, 3)
#     return image_rgb

while (True):
    car_state = client.getCarState()
   
    print('car speed: {0}'.format(car_state.speed))
    
    if (car_state.speed < 20):
        car_controls.throttle = 1.0
        client.setCarControls(car_controls)
    else:
        car_controls.throttle = 0.0
    
    #state_buf[0] = np.array([car_controls.steering, car_controls.throttle, car_controls.brake, car_state.speed])
    #model_output = model.predict([image_buf, state_buf])
    #car_controls.steering = float(model_output[0][0])
    
    car_controls.steering = 0

    recording = sr.Recognizer()
    with sr.Microphone() as source:
        recording.adjust_for_ambient_noise(source)
        print("Please Say something:")
        audio = recording.listen(source)
        a = recording.recognize_google(audio)
   
    try:
        print("You said: \n" + recording.recognize_google(audio))
    except Exception as e:
        print(e)
   
    if recording.recognize_google(audio) == 'light':
        car_controls.steering = 0.5
        print("turning right")
        
    if recording.recognize_google(audio) == 'left':
        car_controls.steering = -0.5
        print("turning left")
        
    if recording.recognize_google(audio) == 'stop':
        car_controls.steering = 0
        car_controls.throttle = 0.0
        car_controls.brake = 1
        print("stopping")
        
    print('Sending steering = {0}, throttle = {1}'.format(car_controls.steering, car_controls.throttle))
    
    client.setCarControls(car_controls)
    
    #responses = client.simGetImages([ImageRequest(1, AirSimImageType.Scene)])
    responses = client.simGetImages([airsim.ImageRequest(1, airsim.ImageType.Scene)])
    #responses = client.simGetImages(airsim.ImageRequest("1", airsim.ImageType.Scene, False, False))
    img1d = np.fromstring(responses.image_data_uint8, dtype=np.uint8) # get numpy array
    img_rgb = img1d.reshape(responses.height, responses.width, 3)
    
    def region_of_interest(img, vertices):
        mask = np.zeros_like(img)
        ignore_mask_color = (255)
        cv2.fillPoly(mask, vertices, ignore_mask_color)
        masked_image = cv2.bitwise_and(img, mask)
        return masked_image
    
    def draw_lines(img, lines):
      img = np.copy(img)
      blank_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    
      for line in lines:
        for x1, y1, x2, y2 in line:
          cv2.line(blank_img, (x1,y1), (x2,y2), (0,255, 0), thickness=3)
      
      img = cv2.addWeighted(img, 0.8, blank_img, 1, 0.0)
      return img
    
    def process(image):
      def grayscale(image):
          return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
      gray = grayscale(image)
      canny_image = cv2.Canny(gray, 100, 200)
      
      #Applies a Gaussian Noise kernel
      def gaussian_blur(img, kernel_size):
          return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
      gaus_image = gaussian_blur(canny_image, 1)
    
      height = image.shape[0]
      width = image.shape[1]
      vertices = [(0,height), (width/2, 310), (width, height)]
      masked = region_of_interest(gaus_image, np.array([vertices], np.int32))
    
      lines = cv2.HoughLinesP(masked,
                              rho=6,
                              theta=np.pi/60,
                              threshold=160,
                              lines=np.array([]),
                              minLineLength=40,
                              maxLineGap=25)
      image_with_lines = draw_lines(image, lines)
      return image_with_lines
      
    responsesLanes = process(img_rgb)
    cv2.imshow('frameWindow', responsesLanes)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cv2.destroyAllWindows()
client.enableApiControl(False)  