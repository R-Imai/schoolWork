# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#   Name:		FourieTransform.py
#	Author:		R.Imai
#	Created:	2015 / 11 / 27
#	Last Date:	2015 / 12 / 01
#	Note:
#-------------------------------------------------------------------------------

import sys
import csv
import numpy as np
from scipy import fftpack
from scipy import signal as sg
import matplotlib.pyplot as plt
import codecs
from math import *
import re

argv = sys.argv
argNum = len(sys.argv)

palette = ["#ff0000","#0000ff","#00ff00","#ff8c00","#a600ff","#ff61d7","#1e90ff","#77ff77","#ffff77","#d71a80","#be0b0d","#1a0099","#0e8154","#96781c","#6c128b","#f9a8e4","#9cceff","#a5f0a5","#eff78d","#dc9adf"]

PI = 3.141592
output = "p"
exFileName = "Fig"

def checkUsage():
    check = False
    if argv[1] == "help" or argv[1] == "-h" or argv[1] == "usage":
        print("\nこのプログラムはフーリエ変換をしてグラフ出力するものです。")
        check = True
    elif argNum < 4:
        check = True
    return check

def usage():
    print("\nコマンドライン引数: (入力ファイル名)(サンプリング間隔)(モード)(値1)(値2)(値3)")
    print("\n\tモード:\t出力:\tp: その場にプロット")
    print("\t　　  \t　　 \ts: 保存(コマンドラインの最後に保存したいファイル名を拡張子なしで指定)")
    print("\t　　  \t範囲:\t-a: すべての区間\t")
    print("\t　　  \t　　 \t-n: (値1)にNの値を指定。最初からN間隔でフーリエ変換")
    print("\t　　  \t　　 \t-s: (値1)に開始点を指定。そこから最後まで。")
    print("\t　　  \t　　 \t-f: (値1)に終端点を指定。最初からそこまで。")
    print("\t　　  \t　　 \t-p: (値1)に開始点,(値2)に終端点を指定")
    print("\t　　  \t窓関数:\t-hm: ハミング窓")
    print("\t　　  \t　　　:\t-hn: ハ二ング窓")
    print("\t　　  \t　　　:\t-bk: ブラックマン窓")
    print("\t　　  \t　　　:\t-ga: ガウス窓")
    print("\t　　  \t　　　:\t-bar: バートレット窓")
    print("\tモードは(出力)(範囲)(窓関数)で記述\n\tex)p-a-hm: すべての区間にハミング窓をかけその場に表示")
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

    cnt = 0
    for row in reader:
        if cnt == 0:
            mat = np.array(int(row[0]))
        else:
            mat = np.append(mat,int(row[0]))
        cnt += 1
    print("\tsucess!")
    return mat

def mkWindow(com,N):
    if com == "hm":
        win = sg.hamming(N)
    elif com == "hn":
        win = sg.hann(N)
    elif com == "bk":
        win = sg.blackman(N)
    elif com == "ga":
        win = sg.gaussian(N,N/16)
    elif com == "bar":
        win = sg.bartlett(N)
    elif com == "rect":
        win = np.ones(N)
    else :
        usage()
    return win

def makePalam(y):
    global output
    global exFileName

    mode = re.split(r"[-]",argv[3])
    if not(len(mode) == 3 or len(mode) == 2):
        usage()

    output = mode[0]

    if mode[1] == "a":
        start = 0
        N = len(y)
        if mode[0] == "s":
            exFileName = argv[4]
    elif mode[1] == "n":
        start = "n"
        N = int(argv[4])
        if mode[0] == "s":
            exFileName = argv[5]
    elif mode[1] == "s":
        start = int(argv[4])
        N = len(y) - int(argv[4])
        if mode[0] == "s":
            exFileName = argv[5]
    elif mode[1] == "f":
        start = 0
        N = int(argv[4])
        if mode[0] == "s":
            exFileName = argv[5]
    elif mode[1] == "p":
        start = int(argv[4])
        N = int(argv[5]) - int(argv[4])
        if mode[0] == "s":
            exFileName = argv[6]
    else :
        usage()

    if (len(mode) == 3):
        win = mkWindow(mode[2],N)
    else:
        win = mkWindow("rect",N)

    return start,N,win


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


def plot(base,coe1,coe2,coe3,Hz,start,end,n):
    print("ploting...")
    plt.figure(figsize=(16, 9))

    plt.subplot(221)
    plt.plot(base,color = palette[0])
    plt.axvline(start, color = palette[12],label = "start")
    plt.axvline(end, color = palette[11],label = "end")
    plt.xlim([0,len(base)-1])
    plt.xlabel(u"number of data")
    plt.ylabel(u"power")
    plt.title("origin signal")


    plt.subplot(222)
    plt.plot(coe1,color = palette[1])
    plt.xlim([0,len(coe1)-1])
    plt.xlabel(u"Hz")
    plt.ylabel(u"power")
    plt.title("window function")


    plt.subplot(223)
    plt.plot(coe2,color = palette[2])
    plt.xlim([0,len(coe2)-1])
    plt.xlabel(u"Hz")
    plt.ylabel(u"power")
    plt.title("processing signal")


    plt.subplot(224)
    plt.plot(coe3,color = palette[3])
    #plt.yscale("log")
    plt.xticks(np.linspace(0,(len(coe3)//16)*16,17),np.linspace(0,(len(coe3)//16)*16*Hz,17).astype(np.int))
    plt.xlim([0,int((len(coe2)-1)/2)])
    plt.xlabel(u"frequency [kHz]")
    plt.ylabel(u"power")
    plt.title("fourie transform")
    if output == "p":
        plt.show()
        print("\tsucess!")
        plt.clf
    elif output == "s":
        plt.savefig(exFileName + str(n) + ".png")
        print("\tsave " + exFileName + str(n) + ".png")
        plt.close()



if __name__ == '__main__':
    if checkUsage():
        usage()
    y = importData()
    start,N,win = makePalam(y)
    dt = int(argv[2])
    if start == "n":
        for i in range((len(y)//N)*2):
            start = i*(N//2)
            yCut = broach(y, start, N)
            winY = yCut * win
            sig,freq = FFT(yCut,dt)
            #plot(y,np.real(sig),np.imag(sig),np.abs(sig),dt,start,start + N,i)
            plot(y,win,winY,np.abs(sig),dt,start,start + N, i)
    else :
        yCut = broach(y, start, N)
        winY = yCut * win
        sig,freq = FFT(yCut,dt)
        #plot(y,np.real(sig),np.imag(sig),np.abs(sig),dt,start,start + N,"")
        plot(y,win,winY,np.abs(sig),dt,start,start + N,"")
