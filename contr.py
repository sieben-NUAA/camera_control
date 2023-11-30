import socket
import time
import cv2
import numpy as np
import insightface


model = insightface.app.FaceAnalysis(root='./',
                                     allowed_modules=None,
                                     providers=['CUDAExecutionProvider'])
model.prepare(ctx_id=1, det_thresh=0.50)


def recognize(img):
    face_list = model.get(img)
    print(len(face_list))
    if len(face_list) == 0:
        return
    x = int((face_list[0].bbox[0] + face_list[0].bbox[2]) / 2)
    y = int((face_list[0].bbox[1] + face_list[0].bbox[3]) / 2)
    height, width, _ = img.shape
    block_height = height // 3
    block_width = width // 3
    row, col = get_block(x, y, block_height, block_width)
    print(f"Coordinate ({x}, {y}) is in block ({row}, {col})")
    move_to_block(row, col)
    print(f"Move to block ({row}, {col})")


def get_block(x, y, block_height, block_width):
    row = y // block_height
    col = x // block_width
    return row, col


def move_to_block(row, col):
    if row == 0 and col == 0:
        upleft()
    elif row == 0 and col == 1:
        up()
    elif row == 0 and col == 2:
        upright()
    elif row == 1 and col == 0:
        left()
    elif row == 1 and col == 1:
        return
    elif row == 1 and col == 2:
        right()
    elif row == 2 and col == 0:
        downleft()
    elif row == 2 and col == 1:
        down()
    elif row == 2 and col == 2:
        downright()


def downright():
    client = socket.socket()
    client.connect(('192.168.3.24', 1259))
    client.send(b'\x81\x01\x06\x01\x08\x08\x02\x02\xFF')
    time.sleep(1.6)
    client.send(b'\x81\x01\x06\x01\x09\x00\x03\x03\xFF')
    client.close()


def go_to_position():
    client = socket.socket()
    client.connect(('192.168.3.24', 1259))
    client.send(b'\x81\x01\x04\x3F\x02\x00\xFF')
    time.sleep(2)
    print('go to pre-position')
    client.close()


def down():
    client = socket.socket()
    client.connect(('192.168.3.24', 1259))
    client.send(b'\x81\x01\x06\x01\x18\x09\x03\x02\xFF')
    # 先补6个0，命令一，命令二，数据长度（两位），左转，状态（开始/停止），速度
    time.sleep(1)
    # 8X 01 06 01 VV WW 02 03 FF
    client.send(b'\x81\x01\x06\x01\x09\x00\x03\x03\xFF')
    client.close()


def up():
    client = socket.socket()
    client.connect(('192.168.3.24', 1259))
    client.send(b'\x81\x01\x06\x01\x00\x09\x03\x01\xFF')
    # 先补6个0，命令一，命令二，数据长度（两位），左转，状态（开始/停止），速度
    time.sleep(1)
    # 8X 01 06 01 VV WW 02 03 FF
    client.send(b'\x81\x01\x06\x01\x09\x00\x03\x03\xFF')
    client.close()


def right():
    client = socket.socket()
    client.connect(('192.168.3.24', 1259))
    client.send(b'\x81\x01\x06\x01\x12\x08\x02\x03\xFF')
    time.sleep(0.75)
    client.send(b'\x81\x01\x06\x01\x09\x00\x03\x03\xFF')
    client.close()


def left():
    client = socket.socket()
    client.connect(('192.168.3.24', 1259))
    client.send(b'\x81\x01\x06\x01\x12\x08\x01\x03\xFF')
    time.sleep(0.75)
    client.send(b'\x81\x01\x06\x01\x09\x00\x03\x03\xFF')
    client.close()


def upleft():
    client = socket.socket()
    client.connect(('192.168.3.24', 1259))
    client.send(b'\x81\x01\x06\x01\x08\x08\x01\x01\xFF')
    time.sleep(1.5)
    client.send(b'\x81\x01\x06\x01\x09\x00\x03\x03\xFF')
    client.close()


def upright():
    client = socket.socket()
    client.connect(('192.168.3.24', 1259))
    client.send(b'\x81\x01\x06\x01\x08\x08\x02\x01\xFF')
    time.sleep(1.6)
    client.send(b'\x81\x01\x06\x01\x09\x00\x03\x03\xFF')
    client.close()


def downleft():
    client = socket.socket()
    client.connect(('192.168.3.24', 1259))
    client.send(b'\x81\x01\x06\x01\x08\x08\x01\x02\xFF')
    time.sleep(1.5)
    client.send(b'\x81\x01\x06\x01\x09\x00\x03\x03\xFF')
    client.close()


def stop():
    client = socket.socket()
    client.connect(('192.168.3.24', 1259))
    client.send(b'\x00\x00\x00\x00\x00\x00\x22\x31\x00\x03\x17\x01\x04')
    time.sleep(5)
    client.send(b'\x81\x01\x06\x01\x09\x00\x03\x03\xFF')
    client.close()


if __name__ == "__main__":
    f = 0
    cap = cv2.VideoCapture("rtsp://192.168.3.24:554/live/av0")

    while True:
        # 读取图片
        ret, frame = cap.read()
        # cv2.imshow("Result", frame)
        if f % 50 == 0:
            # 显示图片
            # cv2.imshow("Result", frame)
            cv2.imwrite("test.jpg", frame)
            print(f"图片的shape为: {np.shape(frame)}")
            recognize(frame)

        f += 1
        # 定义关闭
        cv2.waitKey(1)

    # 释放资源
    cap.release()
    # cam.down(cam, 5)
