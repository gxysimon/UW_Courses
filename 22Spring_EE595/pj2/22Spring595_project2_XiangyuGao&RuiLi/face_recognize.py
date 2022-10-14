#! usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import os
import mimetypes  # 判断文件类型
import cv2
import time
import win32api
import win32con


def get_picture():
    cap = cv2.VideoCapture(0)
    cascade = cv2.CascadeClassifier(
        "C:/Users/gxysi/anaconda3/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
    while True:
        # get a frame
        ret, frame = cap.read()
        # show a frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rect = cascade.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=5, minSize=(5, 5),
                                        flags=cv2.CASCADE_SCALE_IMAGE)
        for x, y, z, w in rect:
            cv2.rectangle(frame, (x, y), (x + z, y + w), (0, 0, 255), 2)
        cv2.imshow("capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("C:/UW/22 Spring/595/pj2/22Spring595_project2_XiangyuGao&RuiLi/client_picture/client.jpg", frame)  # 相对路径
            break
    cap.release()
    cv2.destroyAllWindows()


def face_verification():
    BASE_URL = "https://api-cn.faceplusplus.com/facepp/v3"
    API_KEY = "3qTlpuXh3PNcRph3wn913trHAsb-n_Q7"
    API_SECRET = "UvBKTbxhmPXdJUivOu72ppumV7CRTyD1"
    BASE_PARAMS = {
        'api_key': '3qTlpuXh3PNcRph3wn913trHAsb-n_Q7',
        'api_secret': 'UvBKTbxhmPXdJUivOu72ppumV7CRTyD1'
    }

    def upload_img(fileDir, oneface=True):
        url = '%s/detect?api_key=%s&api_secret=%s' % (
            BASE_URL, API_KEY, API_SECRET)
        # 注意参数名与api文档一致
        files = {'image_file': (os.path.basename(fileDir), open(fileDir, 'rb'),
                                mimetypes.guess_type(fileDir)[0]), }
        r = requests.post(url, files=files)
        faces = r.json().get('faces')
        # print faces
        if faces is None:
            print('There is no face found in %s' % fileDir)
        else:
            return faces[0]['face_token']

    def compare(face_token1, face_token2):
        url = '%s/compare' % BASE_URL
        params = BASE_PARAMS
        params['face_token1'] = face_token1
        params['face_token2'] = face_token2
        r = requests.post(url, params)
        # print r.status_code
        # print r.json()
        return r.json().get('confidence')

    #get_picture()
    print("Face loading...\n")
    face1 = upload_img('C:/UW/22 Spring/595/pj2/22Spring595_project2_XiangyuGao&RuiLi/server_picture/demo.jpg')
    print("Proofreading Faces...\n")
    time.sleep(5)  # 防止出现qps
    print("Comparing Faces...\n")
    face2 = upload_img('C:/UW/22 Spring/595/pj2/22Spring595_project2_XiangyuGao&RuiLi/received_picture/client.jpg')
    confidence = compare(face1, face2)
    if confidence >= 70:
        # print u"同一个人"
        # win32api.ShellExecute(0,'op','genealogy.exe','','',1)
        # win32api.MessageBox(0, u"刷脸成功", u"家谱管理系统", win32con.MB_OK)
        print('Verification Succeeded!')
        return True
        # 这里写你想要继续执行的代码
    else:
        # win32api.MessageBox(0, u"刷脸失败", u"家谱管理系统", win32con.MB_OK)
        print('Verification Failed!')
        return False
        # print u"不是同一个人"
# if __name__ == '__main__':
#     get_picture()

# C:/UW/22 Spring/595/pj2/22Spring595_project2_XiangyuGao&RuiLi/client_picture/RyanReynolds.jpg
