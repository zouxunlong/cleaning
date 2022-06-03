# coding = utf-8
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

#========================================================
#  数据预处理
#========================================================

def transform(img):
    '''
    将图像转为一维向量
    '''
    result = np.int_(img.reshape((-1,1)))
    length = len(result)
    # 为便于分类训练色像素点对应的分量值置黑色为-1，其他置为1 
    for i in range(length):
        if int(result[i]) < 255:
            result[i] = -1
        else:
            result[i] = 1
    print(result)
    return result

#========================================================
#  训练阶段
#========================================================

def training(W, img, lr):
    '''
    训练函数
    INPUT --> 权值, 图像, 学习率
    '''
    p = transform(img)
    pLen = len(p)
    # 初始化权值矩阵W全0矩阵
    if W is None:
        W = np.zeros((pLen,pLen))
    t = p
    # 实现训练阶段基于hebb规则的学习过程
    # 使用np.dot()函数实现向量的内积运算
    result = W + lr * np.dot(p,t.T)
    return result

#========================================================
#  测试阶段
#========================================================

def hardlim(a):
    '''
    hardlim硬限传输激发函数
    当网络的输入达到阈值时，则硬限幅激活函数的输出为1，否则为0
    '''
    a[a >= 0] = 1
    a[a < 0] = 0
    return a

def testing(W, img):
    '''
    测试函数
    '''
    # 调用激发函数hardlim控制输出结果为0或1
    result = hardlim(np.dot(transform(img).T, W))
    return result

#========================================================
# 主程序
#========================================================

if __name__=='__main__':
    # 调用训练函数进行自联想存储器的训练
    W = None
    img_train = np.array(Image.open('0.bmp').convert("L"))
    lr = 0.5
    W = training(W, img_train, lr)

    # 利用训练得到的权值矩阵进行测试
    test_old = np.array(Image.open('0_test.bmp').convert("L"))
    test_new = testing(W, test_old).reshape(img_train.shape)

    plt.figure(figsize=(10,10))
    plt.subplot(121)
    # 打印待修复图像
    plt.title('old')
    plt.imshow(test_old, cmap=plt.cm.gray)
    plt.subplot(122)
    # 打印修复后图像
    plt.title('new')
    plt.imshow(test_new, cmap=plt.cm.gray)
    plt.show()