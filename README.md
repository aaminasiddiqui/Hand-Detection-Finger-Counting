### Hand Detection and Finger Counting using OpenCV

___

This project involves using OpenCV to detect and count the number of fingers shown by a hand in real-time through a webcam feed. The main objectives include hand detection, segmentation, and finger counting. The process can be broken down into several key steps

1. **Video Capture**: Capturing real-time video from a webcam and preprocessing each frame.

2. **Hand Detection**: Using techniques like background subtraction and thresholding to isolate the hand.

3. **Contour Detection**: Finding the hand's contour and identifying the largest one.

4. **Convex Hull and Defects**: Computing the convex hull of the hand contour and identifying convexity defects to locate finger valleys.

5. **Finger Counting**: Analyzing the defects to count the fingers, typically by detecting peaks in the contour that represent fingers.

6. **Displaying Results**: Overlaying the counted fingers on the video feed and displaying the count on the screen in real-time.

**DEMO-**

<img width="1274" alt="Screenshot 2024-07-28 at 18 29 46" src="https://github.com/user-attachments/assets/cd039994-7ae6-43cf-8b3c-2f26099dab81">

<img width="1277" alt="Screenshot 2024-07-28 at 18 29 48" src="https://github.com/user-attachments/assets/544bdd7f-2a1f-468e-80d9-17de8d0e9cb1">

<img width="1274" alt="Screenshot 2024-07-28 at 18 29 55" src="https://github.com/user-attachments/assets/25f46f6c-a661-4cf0-9867-1ada7cdbd3e3">

<img width="1277" alt="Screenshot 2024-07-28 at 18 38 47" src="https://github.com/user-attachments/assets/630d4979-0aac-44b7-bbce-a0d8acb1221c">
