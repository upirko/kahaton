import os
import sys
import logging
from video_processing import VideoProcess

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        logging.error("Первым параметром передайте путь до файла!")
        sys.exit(1)
    arg = sys.argv[1]
    if arg.startswith("http://") or arg.startswith("https://") or os.path.isfile(arg):
        vpf = VideoProcess(arg, {'trans': 0.765432, 'crash': 0.5})
    else:
        logging.error("Файл не загрузил, пока.")
        sys.exit(-5)