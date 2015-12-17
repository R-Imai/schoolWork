# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#   Name:		FourieTransform.py
#	Author:		R.Imai
#	Created:	2015 / 11 / 27
#	Last Date:	2015 / 12 / 17
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
from mpl_toolkits.mplot3d import Axes3D
#from pylab import*


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
    print("\nコマンドライン引数: (入力ファイル名)(サンプリング間隔)(モード)(値1)(値2)(保存先ファイル名)(プロット内容)")
    print("\n\tモード:\t出力:\tp: その場にプロット")
    print("\t　　  \t　　 \ts: 保存((保存先ファイル名)に保存したいファイル名を拡張子なしで指定)")
    print("\t　　  \t　　 \tcsv: csvで保存((保存先ファイル名)に保存したいファイル名を拡張子なしで指定)")
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
    print("\tモードは(出力)(範囲)(窓関数)で記述\n\tex)p-a-hm: すべての区間にハミング窓をかけその場に表示\n")
    print("\tプロット内容:\t出力内容を指定する。2Dなら最大4つまででそれぞれの間は-でつなぐ(記述がない場合はデフォルト値(o-w-p-f)になる)")
    print("\t　　  \t　　　:\to: オリジナルの信号")
    print("\t　　  \t　　　:\tr: フーリエ実数部")
    print("\t　　  \t　　　:\ti: フーリエ虚数部")
    print("\t　　  \t　　　:\tw: 窓関数")
    print("\t　　  \t　　　:\tf: フーリエ変換結果")
    print("\t　　  \t　　　:\tp: 窓関数をかけた後の信号")
    print("\t　　  \t　　　:\t3D: 3Dプロット(3Dの場合は一つだけ)")

    exit()

def fileOpen(path,mode):
    try:
        fp = open(path, mode)
    except IOError:
        print (path+"cannot be opened.")
        exit()
    except Exception as e:
        print('type' + str(type(e)))
        exit()
    return fp


def importData():
    print("importing...")
    fp1 = fileOpen(argv[1], "r")
    reader = csv.reader(fp1)

    cnt = 0
    for row in reader:
        if cnt == 0:
            mat = np.array(float(row[0]))
        else:
            mat = np.append(mat,float(row[0]))
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
        if mode[0] == "s" or mode[0] == "csv":
            exFileName = argv[4]
            try:
                palamList = argv[5]
            except IndexError:
                palamList = "o-w-p-f"
        elif mode[0] == "p":
            try:
                palamList = argv[4]
            except IndexError:
                palamList = "o-w-p-f"

    elif mode[1] == "n":
        start = "n"
        N = int(argv[4])
        if mode[0] == "s" or mode[0] == "csv":
            exFileName = argv[5]
            try:
                palamList = argv[6]
            except IndexError:
                palamList = "o-w-p-f"
        elif mode[0] == "p":
            try:
                palamList = argv[5]
            except IndexError:
                palamList = "o-w-p-f"

    elif mode[1] == "s":
        start = int(argv[4])
        N = len(y) - int(argv[4])
        if mode[0] == "s" or mode[0] == "csv":
            exFileName = argv[5]
            try:
                palamList = argv[6]
            except IndexError:
                palamList = "o-w-p-f"
        elif mode[0] == "p":
            try:
                palamList = argv[5]
            except IndexError:
                palamList = "o-w-p-f"

    elif mode[1] == "f":
        start = 0
        N = int(argv[4])
        if mode[0] == "s" or mode[0] == "csv":
            exFileName = argv[5]
            try:
                palamList = argv[6]
            except IndexError:
                palamList = "o-w-p-f"
        elif mode[0] == "p":
            try:
                palamList = argv[5]
            except IndexError:
                palamList = "o-w-p-f"

    elif mode[1] == "p":
        start = int(argv[4])
        N = int(argv[5]) - int(argv[4])
        if mode[0] == "s" or mode[0] == "csv":
            exFileName = argv[6]
            try:
                palamList = argv[7]
            except IndexError:
                palamList = "o-w-p-f"
        elif mode[0] == "p":
            try:
                palamList = argv[6]
            except IndexError:
                palamList = "o-w-p-f"

    else :
        usage()

    if (len(mode) == 3):
        win = mkWindow(mode[2],N)
    else:
        win = mkWindow("rect",N)

    return start,N,win,palamList

def getPlotPalam(palamList):
    trans = {"o":0,"w":1,"r":2,"i":3,"f":4,"p":5}
    if argv[argNum - 1]:
        arg = re.split(r"[-]",palamList)
    if arg[0] == "3D" or arg[0] == "3d":
        palam = "3d"
    else:
        palam = []
        try:
            for i in range(4):
                if i < len(arg):
                    palam.append(trans[arg[i]])
        except :
            print("プロット内容の指定がおかしいです。")
            exit()
    return palam




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




def detailPlot(palam, start, end, leng, Hz):
    if palam == 0:
        plt.axvline(start, color = palette[12],label = "start")
        plt.axvline(end, color = palette[11],label = "end")
        plt.xlim([0,leng-1])
        plt.xlabel(u"number of data")
        plt.ylabel(u"power")
        plt.title("origin signal")
    elif palam == 1:
        plt.xlim([0,leng-1])
        plt.xlabel(u"number of data")
        plt.ylabel(u"power")
        plt.title("window function")
    elif palam == 2:
        plt.xticks(np.linspace(0,(leng//16)*16,17),np.linspace(0,(leng//16)*16*Hz/(end-start),17).astype(np.int))
        plt.xlim([0,leng-1])
        plt.xlabel(u"frequency [kHz]")
        plt.ylabel(u"power")
        plt.title("real part")
    elif palam == 3:
        plt.xticks(np.linspace(0,(leng//16)*16,17),np.linspace(0,(leng//16)*16*Hz/(end-start),17).astype(np.int))
        plt.xlim([0,leng-1])
        plt.xlabel(u"frequency [kHz]")
        plt.ylabel(u"power")
        plt.title("imaginary part")
    elif palam == 4:
        plt.xticks(np.linspace(0,(leng//16)*16,17),np.linspace(0,(leng//16)*16*Hz/(end-start),17).astype(np.int))
        plt.xlim([0,int((leng-1)/2)])
        plt.ylim([-5,120000])
        plt.xlabel(u"frequency [kHz]")
        plt.ylabel(u"power")
        plt.title("fourie transform")
    elif palam == 5:
        plt.xlim([0,leng-1])
        plt.xlabel(u"number of data")
        plt.ylabel(u"power")
        plt.title("processing signal")


def plot2D(plotPalam, data,Hz,start,end,n):
    print("ploting2D...")
    plt.figure(figsize=(16, 9))
    winDict = [0,110,210,220,220]

    for i in range(len(plotPalam)):
        plt.subplot(winDict[len(plotPalam)] + i + 1)
        plt.plot(data[plotPalam[i]] ,color = palette[i])
        detailPlot(plotPalam[i],start,end,len(data[plotPalam[i]]),Hz)

    if output == "p":
        plt.show()
        print("\tsucess!")
        plt.clf
    elif output == "s":
        plt.savefig(exFileName + str(n) + ".png")
        print("\tsave " + exFileName + str(n) + ".png")
        plt.close()


def plot3D(re,N,Hz):
    print("ploting3D...")
    x = np.arange(0,len(re[0]))*(Hz/N)
    y = np.arange(0,len(re))*(N/(Hz*2000))
    X,Y = np.meshgrid(x,y)
    fig = plt.figure(1)
    ax = Axes3D(fig)
    ax.plot_wireframe(X,Y,re,color = palette[6])
    ax.set_xlabel("frequency [kHz]")
    ax.set_ylabel("time [s]")
    ax.set_zlabel("power")

    if output == "p":
        plt.show()
        print("\tsucess!")
        plt.clf
    elif output == "s":
        plt.savefig(exFileName + ".png")
        print("\tsave " + exFileName + ".png")
        plt.close()


def saveCSV(sig, Hz, N, n):
    fpW = fileOpen(exFileName + str(n) + ".csv", "w")
    for i in range(len(sig)):
        fpW.write(str(i*Hz/N) + "," + str(sig[i]) + "\n")
    print("save " + exFileName + str(n) + ".csv")
    fpW.close()



if __name__ == '__main__':
    if checkUsage():
        usage()
    y = importData()
    print(len(y))
    start,N,win,palamList = makePalam(y)
    isFirstTime = True
    power3D = []
    dt = float(argv[2])
    if start == "n":
        for i in range((len(y)//N)*2 - 1):
            start = i*(N//2)
            yCut = broach(y, start, N)
            winY = yCut * win
            sig,freq = FFT(winY,dt)
            plotPalam = getPlotPalam(palamList)
            sendData = [y, win, np.real(sig), np.imag(sig), np.abs(sig), winY]
            if output == "csv":
                saveCSV(np.abs(sig),dt,N,i)
            elif plotPalam == "3d":
                power3D.append(np.abs(sig[0:len(sig)/2]))
            else:
                plot2D(plotPalam, sendData,dt,start,start + N, i)
        if plotPalam == "3d":
            power3D = np.array(power3D)
            plot3D(power3D,N,dt)
    else :
        yCut = broach(y, start, N)
        winY = yCut * win
        sig,freq = FFT(winY,dt)
        plotPalam = getPlotPalam(palamList)
        sendData = [y, win, np.real(sig), np.imag(sig), np.abs(sig), winY]
        if output == "csv":
            saveCSV(np.abs(sig),dt,N,"")
        elif plotPalam == "3d":
            print("3D表示は範囲がnの時のみ使用可能です")
        else:
            plot2D(plotPalam, sendData,dt,start,start + N,"")
