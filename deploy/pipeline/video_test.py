import gc
from flask import Flask, render_template, Response
import cv2
import os
import time


app = Flask(__name__)


# 对图片进行编码
def array_to_yield(img):
    ret, buffer = cv2.imencode('.jpg', img)
    frame = buffer.tobytes()
    return frame


pull_frame = cv2.imread('pull.png')
pull_frame = array_to_yield(pull_frame)
detect_frame = cv2.imread('detect.png')
detect_frame = array_to_yield(detect_frame)
# VideoCapture可以读取从url、本地视频文件以及本地摄像头的数据
# 0代表的是第一个本地摄像头，如果有多个的话，依次类推
# camera = cv2.VideoCapture('rtsp://127.0.0.1:8554/mystream')


def gen_pull_frames():
    while True:
        # 检索当前目录下是否有pulled.avi文件
        if os.path.lexists('pulled.avi'):
            print('成功检索到文件')
            time.sleep(1)
            for i in range(5):
                cap = cv2.VideoCapture('pulled.avi')
                while True:
                    ret, frame = cap.read()
                    if ret:
                        frame = array_to_yield(frame)
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                        time.sleep(0.01)
                    else:
                        break
                gc.collect()
            os.remove('pulled.avi')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + pull_frame + b'\r\n')
        gc.collect()


def gen_detect_frames():
    while True:
        # 一帧帧循环读取pull_list
        if os.path.lexists('detected.avi'):
            print('成功检索到文件')
            time.sleep(1)
            for i in range(5):
                cap = cv2.VideoCapture('detected.avi')
                while True:
                    ret, frame = cap.read()
                    if ret:
                        frame = array_to_yield(frame)
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                        time.sleep(0.01)
                    else:
                        break
                gc.collect()
            os.remove('detected.avi')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + detect_frame + b'\r\n')
        gc.collect()

"""
def gen_pull_frames():
    while True:
        # 一帧帧循环读取摄像头的数据
        if len(pull_list) != 0:
            for frame in pull_list:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + pull_frame + b'\r\n')
            gc.collect()
            
            
@app.route('/video_pull')
def video_pull():
    # 通过将一帧帧的图像返回，就达到了看视频的目的。multipart/x-mixed-replace是单次的http请求-响应模式，如果网络中断，会导致视频流异常终止，必须重新连接才能恢复
    return Response(gen_pull_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
"""


@app.route('/video_pull')
def video_pull():
    # 通过将一帧帧的图像返回，就达到了看视频的目的。multipart/x-mixed-replace是单次的http请求-响应模式，如果网络中断，会导致视频流异常终止，必须重新连接才能恢复
    return Response(gen_pull_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_detect')
def video_detect():
    # 通过将一帧帧的图像返回，就达到了看视频的目的。multipart/x-mixed-replace是单次的http请求-响应模式，如果网络中断，会导致视频流异常终止，必须重新连接才能恢复
    return Response(gen_detect_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True, threaded=True)
