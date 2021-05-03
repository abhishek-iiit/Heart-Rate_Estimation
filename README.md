# Heart Rate Estimator
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)](https://forthebadge.com)

A person’s heart rate can be indicative of their health, fit-ness, activity level, stress, and much more. Cardiac pulse is  typically  measured in clinical settings using electrocardiogram(ECG), which require patients to wear chest straps with adhesive gel patches that are abrasive and become uncomfortable for user.Heart rate can also be monitored using pulse oxiometry sensor that may be worn in the fingerprint or earlobe. These sensor are not convienent for long term wear and pressure can be uncomfortable over time. So, Non-contact heart rate measurement through a simple webcam or phone camera would aid telemedicine and allow  the average person to track their heart rate without purchasing special equipment.

![Screenshot from 2021-05-03 15-23-54](https://user-images.githubusercontent.com/69477761/116866622-5aaf3300-ac29-11eb-94c1-c56f9e453d6a.png)

Here,I have used various python libraries and modules for :
- Performing the face detection and tracking using OpenCV or any other computer vision library
- Selecting the forehead as Region of Interest (ROI) and displaying adjusted boundary box
- Calculating heart rate from the signals from ROI under both light conditions
- Implementing signal processing to remove the motion noise to get consistent results
- Calculating heart rate variability (HRV) from the video.

![Screenshot from 2021-05-03 15-33-45](https://user-images.githubusercontent.com/69477761/116866715-86321d80-ac29-11eb-8ba4-68df2423d7a3.png)

## References:
- [Efficient Real-Time Camera Based Estimation of Heart Rate and Its Variability](https://openaccess.thecvf.com/content_ICCVW_2019/papers/CVPM/Gudi_Efficient_Real-Time_Camera_Based_Estimation_of_Heart_Rate_and_Its_ICCVW_2019_paper.pdf)
- [Emotion & Heartbeat Detection using Image Processing](https://www.ijser.org/researchpaper/Emotion-Heartbeat-Detection-using-Image-Processing.pdf)

## Some Previous Blogs:
<!-- BLOG-POST-LIST:START -->
- [How to get started with Machine learning?](https://abhishek-iiit.hashnode.dev/how-to-get-started-with-machine-learning)
- [Basic Introduction to Scikit Learn](https://medium.com/analytics-vidhya/basic-introduction-to-scikit-learn-fa610f14e40d)
- [Basic tools to learn in Data Analysis with Python](https://medium.com/analytics-vidhya/basic-tools-to-learn-in-data-analysis-with-python-5b9b4a7a1b61)
- [Basic Introduction to Numpy](https://medium.com/analytics-vidhya/basic-introduction-to-numpy-8308c2778e43)
- [Basic Introduction to Pandas: Pandas Series(Part 1)](https://medium.com/analytics-vidhya/basic-introduction-to-pandas-pandas-series-part-1-ee08073b109)
- [Basic Introduction to Pandas: Pandas Series(Part 2)](https://medium.com/analytics-vidhya/basic-introduction-to-pandas-pandas-series-part-2-492c887aeb94)
<!-- BLOG-POST-LIST:END -->

<h1 align=center> Made with ❤️ by </h1>
<p align="center">
  <a href="https://github.com/abhishek-iiit"><img src="https://user-images.githubusercontent.com/69477761/111753834-4ef7ef00-88bd-11eb-856c-afe7d58115d5.png" width=150px height=150px /></a> 
    
<p align="center">
  <img src="https://img.shields.io/badge/abhishekiiit%20-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white"/>  <img src="https://img.shields.io/badge/abhishekiiit%20-%231DA1F2.svg?&style=for-the-badge&logo=Twitter&logoColor=white"/> <img src="https://img.shields.io/badge/manneabhi%20-%23E4405F.svg?&style=for-the-badge&logo=Instagram&logoColor=white"/> <img src="https://img.shields.io/badge/abhishekiiit%20-%24E4405F.svg?&style=for-the-badge&logo=Medium&logoColor=white"/>
