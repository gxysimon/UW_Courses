# 服务器端server.py
import socket
import os
import sys
import struct


def socket_service_image():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.bind(('127.0.0.1', 8001))
        s.bind(('127.0.0.1', 10310))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    #print("Wait for Connection.....................")

    while True:
        sock, addr = s.accept()  # addr是一个元组(ip,port)
        deal_image(sock, addr)
        break


def deal_image(sock, addr):
    print("Accept connection from {0}".format(addr))  # 查看发送端的ip和端口

    while True:
        fileinfo_size = struct.calcsize('128sq')
        buf = sock.recv(fileinfo_size)  # 接收图片名
        print('Picture Name Received')
        if buf:
            filename, filesize = struct.unpack('128sq', buf)
            fn = filename.decode().strip('\x00')
            new_filename = os.path.join(r'C:/UW/22 Spring/595/pj2/22Spring595_project2_XiangyuGao&RuiLi/received_picture/' + fn)
            # 在服务器端新建图片名（可以不用新建的，直接用原来的也行，只要客户端和服务器不是同一个系统或接收到的图片和原图片不在一个文件夹下）
            print('Picture Receiving...')
            recvd_size = 0
            fp = open(new_filename, 'wb')

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = sock.recv(1024)
                    recvd_size += len(data)
                else:
                    data = sock.recv(1024)
                    recvd_size = filesize
                fp.write(data)  # 写入图片数据
            print('Picture Received')
            fp.close()
        sock.close()
        break
# if __name__ == '__main__':
#     socket_service_image()
#     print(1)
