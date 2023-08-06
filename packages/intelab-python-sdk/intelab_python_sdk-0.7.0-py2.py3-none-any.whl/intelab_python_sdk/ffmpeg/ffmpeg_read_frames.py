import cv2
import time
import numpy as np
import subprocess

process = subprocess.Popen([
    'ffmpeg', '-v', 'error',
    '-ss', '00:10:00',
    '-i', '/home/wen/D81141699_2020-12-23_02-56-15.mp4',
    '-an',
    '-f', 'rawvideo',
    '-pix_fmt', 'rgb24',
    '-r', '1',  # 跳秒
    '-vframes', '10',  # 取10帧
    '-'
], stdout=subprocess.PIPE, stdin=None)

t = time.time()
return_code = process.poll()
frames = []
while not return_code:
    raw_image = process.stdout.read(768*432*3)
    if not raw_image:
        break

    process.stdout.flush()
    frame_array = np.fromstring(raw_image, dtype='uint8')

    img = frame_array.reshape((432, 768, 3))
    frame = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow('a', frame)
    cv2.waitKey(0)
    frames.append(frames)
    print('---------------------------------')

    return_code = process.poll()

print(time.time() - t)
