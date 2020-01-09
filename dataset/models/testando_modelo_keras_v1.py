from keras.models import load_model
from keras.models import model_from_json
import numpy as np
from keras.preprocessing import image
import cv2
from datetime import datetime
from time import sleep
print(datetime.now())

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()

json_file.close()
model = model_from_json(loaded_model_json)

model.load_weights("model.h5")
print("Loaded model from disk")

#cap = cv2.VideoCapture("simulacao.mp4")
cap = cv2.VideoCapture("../videos/porta.webm")
delay = 80

def classifer(img):
 test_ibage = image.load_img(img, target_size = (64, 64))
 test_ibage = image.img_to_array(test_ibage)
 test_ibage = np.expand_dims(test_ibage, axis = 0)
 result = model.predict(test_ibage)
 print(model.predict_proba(test_ibage))
 return [int(result[0][0])]


while(True):
    ret, frame = cap.read()
    tempo = float(4/delay)
    sleep(tempo)
    cv2.imwrite("frame.jpg", frame)
    if classifer("frame.jpg")[0] == 0:
        print("porta aberta !")
        cv2.putText(frame, 'porta aberta '+str(datetime.now()), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0) , 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, 'porta fechada '+str(datetime.now()), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0, 255) , 2, cv2.LINE_AA)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
