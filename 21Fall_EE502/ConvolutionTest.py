# -*- coding: utf-8 -*-
"""
Created on Mon Nov 06 20:49:26 2017

@author: chen
"""

# 卷积 http://blog.csdn.net/wkj3022073/article/details/45585837
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

font = FontProperties(fname=r"C:\\WINDOWS\\Fonts\\simsun.ttc", size=14)

'''
a=np.array([1,2,3,4])
v=np.array([1,1,3])


plt.close('all')
plt.figure(1)
plt.plot(a)
plt.plot(v)

end=np.convolve(a,v,'full')
plt.figure(2)
plt.plot(end)
plt.title(u'卷积结果',fontproperties=font)
'''
'''
# 实现一个系统的阶跃响应
# 思路是阶跃信号和一个z传函
N=100   #  仿真点数
u=np.ones(N, np.float) # 输入信号
y=np.zeros(N, np.float) # 输出信号
y[0]=0.0;
for i in np.arange(0,N-1,1):
    y[i+1]=0.5*y[i]+0.2*u[i+1]

plt.close('all')
plt.figure(1)
plt.plot(np.arange(0,N,1),y)
plt.xlabel(u'时间',fontproperties=font)
plt.ylabel(u'响应', fontproperties=font)
plt.title(u'阶跃响应实验', fontproperties=font)
plt.show()
'''

'''
# 手工计算卷积
x = np.array([1, 2, 3, 4], dtype=float)
h = np.array([1, 1], dtype=float)

N = len(x)
L = len(h)

M = np.arange(0, L + N - 1, 1)
y = np.zeros_like(M, np.float)  # 建立一个长度为L+N-1的数组，预备存放

for n in M:
    temp = 0.0
    for k in np.arange(0, N, 1):
        j = n - k
        if j >= L:
            h = np.append(h, 0.0)
        temp = temp + x[k] * h[j]
        if j == 0:
            break
    y[n] = temp
print (y)
print('I have finished the program')
'''

# 卷积函数编写
def MyConvolution(x, h):
    # type: (ndarray, ndarray) -> ndarray
    """

    :param x: 输入信号，参与卷积的信号1 ,一维
    :param h: 冲击响应，参与卷积的信号2，一维
    :return: 系统输出，y，一维
    """
    N = len(x)
    L = len(h)

    M = np.arange(0, L + N - 1, 1)
    y = np.zeros_like(M, np.float)  # 建立一个长度为L+N-1的数组，预备存放

    for n in M:
        temp = 0.0
        for k in np.arange(0, N, 1):
            j = n - k
            if j >= L:
                h = np.append(h, 0.0)
            temp = temp + x[k] * h[j]
            if j == 0:
                break
        y[n] = temp
    print (y)
    print("自编的卷积函数计算完成鸟")
    return y

def main():
        print ('开始进入主函数')
        x = np.array([1, 2, 3, 4], dtype=float)
        h = np.array([1, 1], dtype=float)
        aa=MyConvolution(x,h)
        print (aa)
        plt.plot()

if __name__=='__main__':
    main()