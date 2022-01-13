import os
import sys
import logging
from video_processing import VideoProcess

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        logging.error("Ну ты что делаешь? Хоть что-нибудь то укажи")
        sys.exit(1)
    if len(sys.argv) > 2:
        logging.error("Ну ты что делаешь? Знаешь же, что только один аргумент командной строки доступен :(")
    arg = sys.argv[1]
    if arg.startswith("http://") or arg.startswith("https://") or os.path.isfile(arg):
        vpf = VideoProcess(arg)
    else:
        logging.error("Ну ты не стрим и не файл загрузил, отстань.")
        sys.exit(228)