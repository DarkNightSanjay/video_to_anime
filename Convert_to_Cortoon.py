import cv2
import numpy as np
import os

# Function to apply cartoon effect to an image
def cartoonize_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                  cv2.THRESH_BINARY, blockSize=9, C=9)
    color = cv2.bilateralFilter(img, d=9, sigmaColor=300, sigmaSpace=300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

# Function to process the video
def cartoonize_video(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: The input video file {input_path} does not exist.")
        return
    
    cap = cv2.VideoCapture(input_path)
    
    if not cap.isOpened():
        print(f"Error: Unable to open the input video file {input_path}.")
        return
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (frame_width, frame_height))
    
    if not out.isOpened():
        print(f"Error: Unable to open the output video file {output_path}.")
        return
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        cartoon_frame = cartoonize_image(frame)
        out.write(cartoon_frame)
        cv2.imshow('Cartoonized Video', cartoon_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()

input_video = r'c:\Users\4a Freeboard\Videos\AnyDesk\demovedio.mp4'
output_video = r'C:\Users\4a Freeboard\Desktop\Result\output_cartoon_video.avi'

cartoonize_video(input_video, output_video)
