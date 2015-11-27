# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#   Name:		DiscreteFourieTransform.py
#	Author:		R.Imai
#	Created:	2015 / 11 / 24
#	Last Date:	2015 / 11 / 24
#	Note:       コマンドライン引数は、「インポートファイル名 データ数(Nに当たる) 開始点(無くても可)」
#-------------------------------------------------------------------------------

import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
import codecs
from math import *
import re
from pandas import *

argv = sys.argv
argNum = len(sys.argv)

palette = ["#ff0000","#0000ff","#00ff00","#ff8c00","#a600ff","#ff61d7","#1e90ff","#77ff77","#ffff77","#d71a80","#be0b0d","#1a0099","#0e8154","#96781c","#6c128b","#f9a8e4","#9cceff","#a5f0a5","#eff78d","#dc9adf"]

if argNum < 3:
    print("コマンドライン引数は、「インポートファイル名 データ数(N) 開始点(無くても可)」です。")
    exit()

elif argNum == 3:
    N = int(argv[2])
    start = 0

elif argNum == 4:
    N = int(argv[2])
    start = int(argv[3])
pi = 3.141592
#N = 12640

def importData():
    try:
        fp1 = open(argv[1], 'r')
        reader = csv.reader(fp1)
    except IOError:
        print (argv[1]+"cannot be opened.")
        exit()
    except Exception as e:
        print('type' + str(type(e)))
        exit()

    mat=[]
    cnt = 0
    for row in reader:
        if cnt == 0:
            mat = [int(row[0])]
        else:
            mat.append(int(row[0]))
        cnt += 1
    return mat


def DFT():
    real = [0]*N
    img = [0]*N
    dft = [0]*N
    for i in range(0,N):
        print(i)
        d = 2*pi*i/N
        for j in range(0,N):
            ph = j*d
            real[i] += y[start + j]*cos(ph)
            img[i] -= y[start + j]*sin(ph)
    for i in range(0,N):
        dft[i] = sqrt((real[i]*real[i])+(img[i]*img[i]))
    return dft,real,img


def plot(base,coe1,coe2,coe3):

    plt.figure(1)

    plt.subplot(221)
    plt.plot(base,color = palette[0])
    plt.xlim([0,len(base)-1])
    plt.xlabel(u"times")
    plt.ylabel(u"power")
    #plt.legend()


    plt.subplot(222)
    plt.plot(coe1,color = palette[1])
    plt.xlim([0,len(coe1)-1])
    plt.xlabel(u"Hz")
    plt.ylabel(u"power")
    #plt.legend()


    plt.subplot(223)
    plt.plot(coe2,color = palette[2])
    plt.xlim([0,len(coe2)-1])
    plt.xlabel(u"Hz")
    plt.ylabel(u"power")
    #plt.legend()


    plt.subplot(224)
    plt.plot(coe3,color = palette[3])
    plt.xlim([0,int((len(coe2)-1)/2)])
    plt.xlabel(u"Hz")
    plt.ylabel(u"power")
    #plt.legend()
    plt.show()
    #plt.savefig("Fig1.png")

if __name__ == '__main__':
    y = importData()

    dft,real,img = DFT()
    plot(y,real,img,dft)
