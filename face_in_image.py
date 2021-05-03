#IMPORTING THE LIBRARIES
import cv2
import numpy as np
import dlib
import copy

#DEFINING THE FUNCTION
#detect faces using Haar cascade classifier for a video frame
def detectFacesInImage(videoframe):
    # convert the image to grayscale
    gray = cv2.cvtColor(videoframe, cv2.COLOR_BGR2GRAY)

    rectFrame = np.zeros(videoframe.shape, videoframe.dtype)
    # facesFound = np.empty([1,4])
    # create a cascade classifier to detect frontal faces and profile faces using haar cascade classifier
    faceCascadeClassifier = cv2.CascadeClassifier('haarcascade_frontalface.xml')
    profileCascadeClassifier = cv2.CascadeClassifier('haarcascade_profileface.xml')

    # detect faces
    faces = faceCascadeClassifier.detectMultiScale(gray, 1.3, 5, 0, (70, 70))
    facesFound = np.array(faces,dtype=int)

    if(len(facesFound) == 0):
        faces = profileCascadeClassifier.detectMultiScale(gray, 1.3, 5, 0, (70, 70))
        facesFound = np.array(faces,dtype=int)

    #create a classifier to detect forehead on the face ROI, this is for reducing the false detection of faces
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_81_face_landmarks.dat")
    faces2 = detector(gray)

    totalFaces = []
    faceRectangles = []
    if(len(facesFound) != 0) :
        # draw the faces
        for face,face1 in zip(facesFound,faces2):
            x3 = face[0]
            y3 = face[1]
            w3 = face[2]
            h3 = face[3]

            x1 = face1.left()
            y1 = face1.top()
            x2 = face1.right()
            y2 = face1.bottom()

            landmarks = predictor(gray, face1)
            x_pts = []
            y_pts = []

            for n in range(68, 81):
                x = landmarks.part(n).x
                y = landmarks.part(n).y

                x_pts.append(x)
                y_pts.append(y)

            x1 = min(x_pts)
            x2 = max(x_pts)
            y1 = min(y_pts)
            y2 = max(y_pts)

            cv2.rectangle(videoframe, (x1, y1), (x2, y2-45), (0, 0, 255), 3)
            isFaceDetected = len(faces) > 0

            #confirm it is a face and post process for heart rate
            if(isFaceDetected) :
                cv2.rectangle(rectFrame, (x3, y3), (x3 + w3, y3 + h3), (255, 0, 0), 3)
                faceROI = copy.copy(videoframe[y3:y3 + h3, x3:x3 + w3])
                totalFaces.append(faceROI)
                faceRectangles.append([x3,y3,w3,h3])

    videoframe = cv2.add(videoframe,rectFrame)
    return videoframe,totalFaces