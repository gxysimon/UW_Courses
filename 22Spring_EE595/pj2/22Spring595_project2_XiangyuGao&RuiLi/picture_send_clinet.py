# 客户端client.py
import socket
import os
import sys
import struct
import face_recognize


def sock_client_image():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', 10310))  # 服务器和客户端在不同的系统或不同的主机下时使用的ip和端口，首先要查看服务器所在的系统网卡的ip
            # s.connect(('127.0.0.1', 8001))  #服务器和客户端都在一个系统下时使用的ip和端口
        except socket.error as msg:
            print(msg)
            print(sys.exit(1))

        print('Name Sending...')
        while True:
            print('Shoot or upload?')
            choose = input('(Please input "shoot" or "upload"):')
            if choose == 'shoot':
                face_recognize.get_picture()
                filepath = "C:/UW/22 Spring/595/pj2/22Spring595_project2_XiangyuGao&RuiLi/client_picture/client.jpg"
                break
            elif choose == 'upload':
                filepath = input('Please input the address of the file:')
                break
            else:
                print('Wrong input, please try again!')

        # 输入当前目录下的图片名 xxx.jpg
        # print('step1')

        fhead = struct.pack(b'128sq', bytes(os.path.basename(filepath), encoding='utf-8'),
                            os.stat(filepath).st_size)  # 将xxx.jpg以128sq的格式打包
        s.send(fhead)
        print('Name Sent!')
        print('Picture Sending...')
        fp = open(filepath, 'rb')  # 打开要传输的图片
        while True:
            data = fp.read(1024)  # 读入图片数据
            if not data:
                print('{0} send over...'.format(filepath))
                break
            s.send(data)  # 以二进制格式发送图片数据
        print('Picture sent')
        # received = s.recv(1024)
        # if received is True:
        s.close()
        break    #循环发送


# if __name__ == '__main__':
#     sock_client_image()
#     print(2)
