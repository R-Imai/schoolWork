# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#   Name:		FourieTransform.py
#	Author:		R.Imai
#	Created:	2015 / 11 / 27
#	Last Date:	2015 / 11 / 27
#	Note:
#-------------------------------------------------------------------------------

import sys
import csv
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
import codecs
from math import *
import re
from pandas import *

argv = sys.argv
argNum = len(sys.argv)

palette = ["#ff0000","#0000ff","#00ff00","#ff8c00","#a600ff","#ff61d7","#1e90ff","#77ff77","#ffff77","#d71a80","#be0b0d","#1a0099","#0e8154","#96781c","#6c128b","#f9a8e4","#9cceff","#a5f0a5","#eff78d","#dc9adf"]

PI = 3.141592

def checkUsage():
    check = False
    if argv[1] == "help" or argv[1] == "-h" or argv[1] == "usage":
        print("\nこのプログラムはフーリエ変換をしてグラフ出力するものです。")
        check = True
    elif argNum < 4:
        check = True
    return check

def usage():
    print("\nコマンドライン引数: (入力ファイル名)(サンプリング間隔)(範囲)(開始点)(終端点)")
    print("\t範囲:\t-a: すべての区間\t(開始点)(終端点)は入力なし")
    print("\t　　 \t-s: 開始点のみ指定\t(終端点)は入力なし")
    print("\t　　 \t-f: 終端点のみ指定\t(開始点)のところに終端点を入力")
    print("\t　　 \t-p: 開始点,終端点を指定")
    exit()

def importData():
    print("importing...")
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
    print("\tsucess!")
    return mat

def makePalam(y):
    if argv[3] == "-a":
        start = 0
        N = len(y)
    elif argv[3] == "-s":
        start = int(argv[4])
        N = len(y) - int(argv[4])
    elif argv[3] == "-f":
        start = 0
        N = int(argv[4])
    elif argv[3] == "-p":
        start = int(argv[4])
        N = int(argv[5]) - int(argv[4])
    else :
        usage()

    return start,N

def broach(y, start, n):
    newY = []
    for i in range(start,start + n):
        newY.append(y[i])

    return newY

def FFT(y,dt):
    print("During analysis...")
    freq = fftpack.fftfreq(len(y), d = dt)
    sig = fftpack.fft(y)
    print("\tsucsess!")
    return sig,freq

def plot(base,coe1,coe2,coe3,Hz):
    print("ploting...")
    plt.figure(1)

    plt.subplot(221)
    plt.plot(base,color = palette[0])
    plt.xlim([0,len(base)-1])
    plt.xlabel(u"number of data")
    plt.ylabel(u"power")
    plt.title("origin signal")
    #plt.legend()


    plt.subplot(222)
    plt.plot(coe1,color = palette[1])
    plt.xlim([0,len(coe1)-1])
    plt.xlabel(u"Hz")
    plt.ylabel(u"power")
    plt.title("real part")
    #plt.legend()


    plt.subplot(223)
    plt.plot(coe2,color = palette[2])
    plt.xlim([0,len(coe2)-1])
    plt.xlabel(u"Hz")
    plt.ylabel(u"power")
    plt.title("imaginary part")
    #plt.legend()


    plt.subplot(224)
    plt.plot(coe3,color = palette[3])
    plt.yscale("log")
    plt.xticks(np.linspace(1, len(coe3), 12), np.linspace(1, len(coe3)*Hz, 12))
    plt.xlim([0,int((len(coe2)-1)/2)])
    plt.xlabel(u"kHz")
    plt.ylabel(u"power")
    #plt.legend()
    plt.title("fourie transform")
    plt.show()
    #plt.savefig("Fig1.png")
    print("\tsucess!")



if __name__ == '__main__':
    if checkUsage():
        usage()
    y = importData()
    start,N = makePalam(y)
    dt = int(argv[2])                       # サンプリング間隔
    yCut = broach(y, start, N)
    sig,freq = FFT(yCut,dt)
    print(freq)
    print(len(sig))
    plot(y,np.real(sig),np.imag(sig),np.abs(sig),dt)
    #print(len(y))
