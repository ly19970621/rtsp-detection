import cv2
import time
import threading
from pipeline_human import PipePredictor
from cfg_utils_rtsp import merge_cfg, argsparser
from datetime import datetime

parser = argsparser()
FLAGS = parser.parse_args()
cfg = merge_cfg(FLAGS)
predict = PipePredictor(FLAGS, cfg)

stack = []
global fps
global width
global height
# 检测开关
global detect_switch
globals()['detect_switch'] = False
fourcc = cv2.VideoWriter_fourcc(*'XVID')


# 向共享缓冲栈中写入数据:
def write(stack, cam) -> None:
    """
    :param cam: 摄像头参数
    :param stack: list对象
    :param top: 缓冲栈容量
    :return: None
    """
    while True:
        globals()['detect_switch'] = False
        cap = cv2.VideoCapture(cam)
        globals()['fps'] = cap.get(5)
        globals()['width'] = int(cap.get(3))
        globals()['height'] = int(cap.get(4))
        pulled_video = cv2.VideoWriter('pulled.avi', fourcc, fps, (width, height))
        while cap.isOpened():
            _, img = cap.read()
            if _:
                stack.append(img)
                pulled_video.write(img)
            # 每到一定容量清空一次缓冲栈
            # 利用gc库，手动清理内存垃圾，防止内存溢出
            else:
                break
        if len(stack) != 0:
            print(len(stack))
            globals()['detect_switch'] = True
            pulled_video.release()
            time.sleep(len(stack)*0.1)
            del stack[:]
            print('清除')
        # time.sleep(0.5)


# 在缓冲栈中读取数据:
def detect_video(stack) -> None:
    while True:
        if detect_switch:
            now = datetime.now()
            str_time = now.strftime('%Y.%m.%d %H:%M:%S')
            print(len(stack))
            inter_storage = stack.copy()
            start_time = time.time()
            human_num, visualize_list = predict.predict_video(inter_storage, width, height, fps)
            out = cv2.VideoWriter('detected.avi', fourcc, fps, (width, height))
            for frame in visualize_list:
                out.write(frame)
            out.release()
            end_time = time.time()
            run_time = '人流量统计所用时间：' + str(end_time - start_time) + ' s'
            txt_file = open('log.txt', 'a')
            str_human_num = '该视频的人流量：' + str(human_num) + ' 人'
            txt_file.write(str_time + '\n' + str_human_num + '\n' + run_time + '\n' + '\n')
            txt_file.close()
            print(str_human_num)
            del inter_storage[:]
            del stack[:]
            globals()['detect_switch'] = False


if __name__ == '__main__':
    for i in range(1):
        thread_con = threading.Thread(target=write, args=(stack, "rtsp://127.0.0.1:8554/mystream", ))
        thread_con.start()

    for j in range(1):
        thread_con = threading.Thread(target=detect_video, args=(stack, ))
        thread_con.start()


