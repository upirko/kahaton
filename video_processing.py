import warnings
import os
import cv2 as cv
import logging
from datetime import datetime
import torch
import ssl


ssl._create_default_https_context = ssl._create_unverified_context

current_dir = os.getcwd()
DIR_FOR_SAVED_FRAMES = current_dir + '/detects'

if not os.path.exists(DIR_FOR_SAVED_FRAMES):
    os.mkdir(DIR_FOR_SAVED_FRAMES)

device = torch.device('cpu')
warnings.filterwarnings('ignore') # https://stackoverflow.com/questions/70044442/get-warnings-warnuser-provided-device-type-of-cuda-but-cuda-is-not-availa

model = torch.hub.load('ultralytics/yolov5', 'custom', current_dir + '/weights.pt')

logging.basicConfig(level=logging.INFO)


class VideoProcess:
    # Класс обработки видео

    def __init__(self, file, common_objects):
        self.video_capture = cv.VideoCapture(file)
        while self.video_capture.isOpened():
            ret, frame = self.video_capture.read() # захват кадра
            if ret is True:
                result = model(frame) # обработка фрейма моделью
                meta_info = result.pandas().xyxy[0] # получение обнаруженных объектов
                names = meta_info.name
                coords = list()
                for idx, val in enumerate(names):
                    if common_objects.get(val, None) is not None \
                            and common_objects.get(val) < meta_info.confidence[idx]: # проверка совпадения по заданным параметрам
                        coords.append([meta_info.xmin[idx], meta_info.ymin[idx], meta_info.xmax[idx], meta_info.ymax[idx]]) # сохранение координат для отображения на фрейме
                        break
                if len(coords) > 0:
                    for coord in coords:
                        # выделение объектов на фрейме
                        cv.rectangle(frame,
                                     (int(coord[0]), int(coord[1])),
                                     (int(coord[2]), int(coord[3])),
                                     (255, 0, 0),
                                     3)
                    filename = f'{DIR_FOR_SAVED_FRAMES}/CRASH_{os.path.basename(file)}_{datetime.now()}.jpg'
                    cv.imwrite(filename, frame) # сохранение фрейма
                    logging.info(f'Coords: {meta_info.to_json()}, filename = {filename}') # вывод полученных координат для отладки
            else:
                self.release()

    def release(self):
        self.video_capture.release()
