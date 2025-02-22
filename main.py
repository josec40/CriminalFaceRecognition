import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'MostWantedList'
images = []
inmateNames = []
myList = os.listdir(path)      # places names of images in MostWanted List folder into myList 

# iterates through reading every image in the myList
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')             # iterates through reading every image in the myList
    images.append(curImg)                           # adds the read image into images list
    inmateNames.append(os.path.splitext(cl)[0])      # splits the string to just give the name of the person                       

# now we have to find the encoding of each image in the images list
def findEncodings(images):
    encodeList= []                                              # encodeList will contain the encodings of every 
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)               # images are required to be in RGB for facial encoding
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# function adds name into Jail Record CSV file with time of addition
def markBooking(name):         
    with open('JailRecord.csv', 'r+') as f:
        myDataList = f.readlines()                              
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])  
        if name not in nameList:                                # if criminal name is not in the csv file, name will be included with data and time of booking
            now = datetime.now()
            dtString = now.strftime('%M/%D/%Y,%H:%M:%S')
            f.writelines(f'\n{name}, {dtString}')


# encoding the images of all the faces in MostWantedList
encodeListKnown = findEncodings(images)
print('Encoding complete.\n')

print("Press 'q' to quit.\n")
cap = cv2.VideoCapture(0)                                             # using the webcam to obtain frames to comapre to the encodings in encodeListKnown
while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0), None, 0.25, 0.25)                    # reducing size of image helps with time to process, in this case 1/4 of size
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)                       # every single frame will be encoded looking for faces and savings their encodings
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):           # one by one grab one face location from cur framelist and grabe encode face from encodesCurFrame
        
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance=0.55)           # comparing each encoded frame to the bank of encoded criminal faces, a match is attempted to be found
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)           # finding out how similar images are, find best match, find distance
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:                                                             # if match found, rectangle with name of match is placed over webcam frame
            name = inmateNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 *4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (7,87,15), 2)
            cv2.rectangle(img,(x1,y2-35), (x2,y2), (176,7,4), cv2.FILLED)
            cv2.putText(img,name,(x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX,0.5,(255, 255, 255),2)
            markBooking(name)                                                               # call markBooking to add booking of criminal into Jail Record file

        top, right, bottom, left = faceLoc                                                  # if match is not found, rectangles will still be placed over unknown detected faces for security
        top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4  
        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)  

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()

