import cv2
import numpy as np
import copy
import time
from numpy.core.fromnumeric import mean
from sklearn.decomposition import FastICA
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import face_in_image
from tkinter import filedialog
import tkinter as tk
import math

from tkinter import filedialog  # Used to provide GUI open/save feature
from tkinter import *
from PIL import Image,ImageTk
#defining the Window
window = Tk()
window.geometry('1280x800')
window.resizable(0, 0)
window.title("Heart Rate Estimator @abhishek jaiswal")
image=Image.open("bg.jpg")
photo=ImageTk.PhotoImage(image)
lab=Label(image=photo,bg='#8fb5c2')
lab.pack()

#Defining the Labels
message = Label(window, text="Heart Rate Estimator @abhishek jaiswal" ,bg="#000000"  ,fg="white"  ,width=50  ,height=2,font=('Helvetica', 35, 'italic bold '))
message.place(x=60, y=5)
message = Label(window, text="Normal Resting Heart-Rate\n60–100 beats/min\n\nWhen Exercising\n130–150 beats/min" ,bg="#000000"  ,fg="white"  ,width=25  ,height=6,font=('Helvetica', 15, 'italic bold '))
message.place(x=990, y=270)
message = Label(window, text="Normal HRV :\n20-200 millisec.\n\nDepends on age,gender,\nphysical fitness\ngenetics" ,bg="#000000"  ,fg="white"  ,width=25  ,height=6,font=('Helvetica', 15, 'italic bold '))
message.place(x=990, y=400)
message = tk.Label(window, text="" ,bg="grey"  ,fg="black"  ,width=20  ,height=2, activebackground = "yellow" ,font=('Helvetica', 20 , ' bold ')) 
message.place(x=980, y=540)

#collect data for estimation
def call():
    def collectDataForHeartRateEstimate(traces, detectedFace):

        #crop face ROI
        frows = detectedFace.shape[0]
        fcols = detectedFace.shape[1]

        # croppedROI = copy.copy(detectedFace[0:frows - 10,20:fcols - 20])
        croppedROI = copy.copy(detectedFace[0:30,20:fcols - 20])

        #get the normalized RGB traces and the time elapsed
        red, green, blue = getRGBTraces(croppedROI)
        elapsed_time = time.time() - start_time

        #add in a list entry
        singleReading = []
        singleReading.append(elapsed_time)
        singleReading.append(red)
        singleReading.append(green)
        singleReading.append(blue)

        traces = addReadingToTraces(traces, singleReading)
        print (singleReading)

        return traces

    # add data to the traces buffer
    def addReadingToTraces(traces,singleReading):
        # add the reading to the existing list of traces
        #maintain the length of the list as the threshold given
        if len(traces) < thresholdTraces:
            traces.append(singleReading)
        else:
            traces.pop(0)
            traces.append(singleReading)

        return traces

    #get the normalized RGB traces
    def getRGBTraces(faceROI):

        #separate the pixel values and average them to get the trace values
        b, g, r = cv2.split(faceROI)

        sum_blue = 0.0
        sum_green = 0.0
        sum_red = 0.0

        frows = faceROI.shape[0]
        fcols = faceROI.shape[1]
        total_pixels = frows * fcols

        #find mean of the ROI
        for row in range(0,frows):
            for col in range(0,fcols):
                blue_value = b.item(row,col)
                green_value = g.item(row,col)
                red_value = r.item(row,col)

                sum_blue += blue_value
                sum_green += green_value
                sum_red += red_value

        mean_blue = sum_blue / total_pixels
        mean_green = sum_green / total_pixels
        mean_red = sum_red / total_pixels

        sq_blue = 0.0
        sq_green = 0.0
        sq_red = 0.0

        #find standard deviation
        for row in range(0,frows):
            for col in range(0,fcols):
                blue_value = b.item(row, col)
                green_value = g.item(row, col)
                red_value = r.item(row, col)

                sq_blue += np.square(blue_value - mean_blue)
                sq_green += np.square(green_value - mean_green)
                sq_red += np.square(red_value - mean_red)

        std_blue = np.sqrt(sq_blue / total_pixels)
        std_green = np.sqrt(sq_green / total_pixels)
        std_red = np.sqrt(sq_red / total_pixels)

        total_blue_val = 0.0
        total_green_val = 0.0
        total_red_val = 0.0

        #find norm RGB trace
        for row in range(0,frows):
            for col in range(0,fcols):
                norm_blue_value = (b.item(row, col) - mean_blue) / std_blue
                norm_green_value = (g.item(row, col) - mean_green) / std_green
                norm_red_value = (r.item(row, col) - mean_red) / std_red

                total_blue_val += norm_blue_value
                total_green_val += norm_green_value
                total_red_val += norm_red_value

        # return norm_red_trace, norm_blue_trace, norm_green_trace
        return mean_red,mean_green,mean_blue

    # find the bpm for one component from ICA
    def getHeartRateForComponent(reconstructedComponent, times, tracelength, frameRate):

        #get equally spaced intervals from the elapsed time
        intervals = np.linspace(times[0], times[-1], tracelength)
        # 
        # # fit a curve over the component values and interpolate to find the value for the intervals above
        interpolatedValues = np.interp(intervals, times, reconstructedComponent)
        # 
        # #smoothen and standardize the interpolated values
        interpolatedValues = np.hamming(tracelength) * interpolatedValues
        interpolatedValues = interpolatedValues - np.mean(interpolatedValues)

        # run FFT on the interpolated values.rfft gives only the positive values from the interpolated values since the FFT is a symmetric curve
        fftValues = np.fft.rfft(interpolatedValues)
        # fftValues = np.fft.rfft(reconstructedComponent)

        #get the power of the FFT
        powerFFT = np.abs(fftValues)
        #descending sorted index
        sortedidx = powerFFT.argsort()[::-1][:len(powerFFT)]

        #construct frequencies at equally spaced intervals. the length is divided by half as we get only half the values .
        # f = 1/t
        # multiply by 60 as the frequency to bpm mapping indicates [0.75,4] Hz maps to [45,240] bpm
        freqsComponent = (frameRate / tracelength) * np.arange(tracelength / 2 + 1)
        freqsComponent = 60 * freqsComponent

        hr = 0.0
        for idx in sortedidx:
            if(freqsComponent[idx] > 50 and freqsComponent[idx] < 150 ):
                hr = freqsComponent[idx]
                break

        return hr

    #method called to get the heart rate values after collecting the data
    def estimateHeartRate(traces,frameRate):
        traceArray = np.array(traces)

        redTrace = traceArray[:,1]
        redmean = np.mean(redTrace)
        redstd = np.std(redTrace)
        norm_red = (redTrace - redmean ) / redstd

        greenTrace = traceArray[:,2]
        greenmean = np.mean(greenTrace)
        greenstd = np.std(greenTrace)
        norm_green = (greenTrace - greenmean) / greenstd

        blueTrace = traceArray[:,3]
        bluemean = np.mean(blueTrace)
        bluestd = np.std(blueTrace)
        norm_blue = (blueTrace - bluemean) / bluestd

        traceArray[:,1] = norm_red
        traceArray[:,2] = norm_green
        traceArray[:,3] = norm_blue

        times = traceArray[:,0]

        # delete the time column from the trace array
        traceArray = np.delete(traceArray, 0, 1)

        #perform ICA on the three colors treating them as signals
        #the input signals - red, green and blue traces
        matrixSignals = np.matrix(traceArray)

        #compute ICA using FastICA from Scipy module
        ica = FastICA(n_components = 3,max_iter=1000)
        reconstructedSignal = ica.fit_transform(matrixSignals)

        #get individual components
        reconstructedComponent1 = reconstructedSignal[:,0]
        reconstructedComponent2 = reconstructedSignal[:,1]
        reconstructedComponent3 = reconstructedSignal[:,2]

        tracelength = len(traceArray)

        #extract the heart rate for individual components
        hr1 = getHeartRateForComponent(reconstructedComponent1,times,tracelength,frameRate)
        hr2 = getHeartRateForComponent(reconstructedComponent2,times,tracelength,frameRate)
        hr3 = getHeartRateForComponent(reconstructedComponent3,times,tracelength,frameRate)

        #maximum of the heart rate values are output as the correct value
        # hr = max(hr1,hr2,hr3)
        hr = hr2
        print ("heart rate : ", hr)
        print ("c1 : ", hr1)
        print ("c2 : ", hr2)
        print ("c3 : ", hr3)
        t = math.sqrt((pow(abs(hr2-hr1),2)+pow(abs(hr3-hr2),2)+pow(abs(hr3-hr1),2)))
        s = "HRV : " +  str(format(t, ".4f"))
        message.configure(text= s)

        return hr

    #main program start

    # provides a dialog box for asking file to open and returns it's path
    window.filename =  filedialog.askopenfilename(title="Select Video File",filetypes=(("mp4 file","*.mp4"),("mov file","*.mov"),("avi file","*.avi"),("flv file","*.flv"),("mkv file","*.mkv"),("all files",".")))
    # cap = cv2.VideoCapture('Test_Video.avi')
    cap = cv2.VideoCapture(window.filename)
    # cap = cv2.VideoCapture(0)
    plt.ion()

    fps = cap.get(cv2.cv2.CAP_PROP_FPS)
    print ("Frames per second: ", format(fps))

    count = 0
    bpmcount = 0
    start_time = time.time()
    tracesList = []
    thresholdTraces = 70
    counti = 100
    while(counti):
        ret ,frame = cap.read()
        if ret == True:

            count += 1

            print ("Processing frame " , count)
            frame, totalFaces = face_in_image.detectFacesInImage(frame)

            if(len(totalFaces) != 0):
                detectedFace = totalFaces[0]

                tracesList = collectDataForHeartRateEstimate(tracesList, detectedFace)

            else:
                #if no faces found in this frame, use the previous reading
                print ("No face detected using the last reading values again")
                if(len(tracesList) > 0):
                    lastReading = tracesList[-1]
                    elapsed_time = time.time() - start_time
                    lastReading[0] = elapsed_time
                    print (lastReading)
                    tracesList = addReadingToTraces(tracesList, lastReading)

            # check if the number of readings in traces list are more than the threshold
            if len(tracesList) >= thresholdTraces:
                if(bpmcount == 2):
                    bpmcount = 0
                    bpm = estimateHeartRate(tracesList,fps)
                    # put the text of heart rate
                    heartRate = 'Estimated heart rate : ' + str(format(bpm, ".4f") + ' beats/min.')
                else:
                    bpmcount+=1

            else:
                # put the text that data is being recorded
                needed = (thresholdTraces - len(tracesList))
                heartRate = 'Collecting data - ' + str(needed) + 's left'

            # show the video frame
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, heartRate, (10, 32), font, 1, (0, 0, 0))

            frame = cv2.resize(frame, (700, 500))
            videoWindow = "Heart Rate Estimation @abhishek-jaiswal"
            cv2.namedWindow(videoWindow, cv2.WINDOW_AUTOSIZE)
            # cv2.resizeWindow(videoWindow, 1440, 810)
            cv2.moveWindow(videoWindow, 260,240)
            cv2.imshow(videoWindow, frame)

            k = cv2.waitKey(60) & 0xff
            if k == 27:
                break

        else:
            break
        counti -=1
    cv2.destroyAllWindows()
    cap.release()

#Defining the buttons
pictext = Button(window, text="Upload Video", command=call  ,fg="black"  ,bg="white"  ,width=20  ,height=3, activebackground = "grey" ,font=('Helvetica', 15 , ' bold '))
pictext.place(x=1000, y=170)
quitWindow = Button(window, text="Quit", command=window.destroy  ,fg="black"  ,bg="white"  ,width=17  ,height=2, activebackground = "grey" ,font=('Helvetica', 15 , ' bold '))
quitWindow.place(x=1020, y=700)

window.mainloop()