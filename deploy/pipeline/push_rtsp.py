import cv2
import subprocess as sp
import time
import gc
import numpy as np

#此处换为你自己的地址，这里使用一个视频
rtsp_url = './mot17_demo.mp4'
out_rtsp_url = 'rtsp://127.0.0.1:8554/mystream'

while True:
    cap = cv2.VideoCapture(rtsp_url)
# Get video information
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    command = ['ffmpeg',
               '-y',
               '-f', 'rawvideo',
               '-vcodec', 'rawvideo',
               '-pix_fmt', 'bgr24',
               '-s', "{}x{}".format(width, height),
               '-r', str(fps),
               '-i', '-',
               '-c:v', 'libx264',
               '-pix_fmt', 'yuv420p',
               '-preset', 'fast',
               '-f', 'rtsp',
               out_rtsp_url]
    p = sp.Popen(command, stdin=sp.PIPE)
    image_list = []
    fake_frame = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(0, fps*1):
        image_list.append(fake_frame)
    while (cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            print("Opening camera is failed")
            break
        image_list.append(frame)
    for i in range(0, fps*1):
        image_list.append(fake_frame)
    for frame in image_list:
        print(frame.shape)
        p.stdin.write(frame.tostring())
    time.sleep(2)
    print(int(cap.get(7)))
    print(int(len(image_list)))
    del image_list[:]
    gc.collect()
    # time.sleep(30)
    break
