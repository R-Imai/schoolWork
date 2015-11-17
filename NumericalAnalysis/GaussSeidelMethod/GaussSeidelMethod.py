# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        	GaussSeidelMethod.py
# Author:      	R.Imai
# Created:     	2015/10/07
# Last Date:   	2015/10/11
# Note:         ガウス・ザイデル法
#               コマンドライン引数は,Matrixcsvファイル,結果書き込みcsvファイル,保存するファイル名(拡張子はなし)
#-------------------------------------------------------------------------------

import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
import codecs
from math import *

argv = sys.argv
argNum = len(sys.argv)

u"""
    収束判定する誤差
"""
ACCURACY = 0.00000001

U"""
    importData
    コマンドライン引数で指定されるcsvファイルの内容を連立方程式の拡大行列として読みこみ、その行数とともに返す

    mat:    csvファイルを取り込む配列
    cnt:    matの行数のカウンタ
"""
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

    mat=[[]]
    cnt = 0
    for row in reader:
        if cnt == 0:
            mat[0] = [int(elm) for elm in row]
        else:
            mat.append([int(elm) for elm in row])
        cnt += 1

    return cnt,mat

u"""
    transPos
    行を入れ替えることにより収束するようになるかを判断する

    index:  その列が最大の値になっている行の場所を示した配列(ない場合は-1)
"""
def transPos(index):
    check = True

    for i in range(0,dimension):
        if index[i] == -1:
            check = False

    return check

u"""
    matrixSet
    収束する可能性が高いように行を入れ替える
    transPos()がFalseの場合はそのまま

    newMat:     入れ替え後の配列
    colIndex:   その列が最大になる行の数(ない場合は-1)

"""
def matrixSet(dimension,mat):
    newMat = [[]]
    colIndex = [-1] * dimension
    maxColList = [0] * dimension

    for i in range(0,dimension):
        maxCol = 0
        for j in range(1,dimension):
            if mat[i][maxCol] < mat[i][j]:
                maxCol = j
        maxColList[i] = maxCol
        colIndex[maxCol] = i

    if transPos(colIndex):
        for i in range(0,dimension):
            if i == 0:
                newMat[i] = mat[colIndex[i]]
            else:
                newMat.append(mat[colIndex[i]])

        return newMat

    else:

        return mat

u"""
    possibility
    収束の十分条件を満たしているかの判断
"""
def possibility(dimension,mat):
    check = True
    for i in range(0,dimension):
        cnt = 0
        for j in range(0,dimension):
            if i != j:
                cnt = cnt + mat[i][j]
        if mat[i][i] < cnt:
            check = False

    return check

u"""
    deformation
    matを計算するための係数に移項する
"""
def deformation(mat):
    newMat = np.zeros([dimension,dimension])
    for i in range(0,dimension):
        k = 0
        for j in range(0,dimension+1):
            if i != j:
                newMat[i][k] = mat[i][j]/mat[i][i]
                k += 1
    print (newMat)

    return newMat

u"""
    check
    収束したかの判断
"""
def check(coe):
    check = False
    for i in range(0,dimension):
        if abs(coe[coe.shape[0]-1][i] - coe[coe.shape[0]-2][i]) > ACCURACY:
            check = True

    return check

u"""
    firstCalc
    一回目の解の更新(変数宣言等があるため)
"""
def firstCalc(mat,coe):
    newCoe = np.zeros(dimension)
    for i in range(dimension):
        newCoe[i] = coe[i]
    for i in range(0,dimension):
        k = 0
        newCoe[i] = mat[i][dimension-1]
        for j in range(0,dimension):
            if(i != j):
                newCoe[i] = newCoe[i] - mat[i][k] * newCoe[j]
                k += 1

    return newCoe

u"""
    calc
    計算で解を更新
"""
def calc(mat,coe):
    newCoe = np.zeros(dimension)
    for i in range(dimension):
        newCoe[i] = coe[coe.shape[0]-1][i]
    for i in range(0,dimension):
        k = 0
        newCoe[i] = mat[i][dimension-1]
        for j in range(0,dimension):
            if(i != j):
                newCoe[i] = newCoe[i] - mat[i][k] * newCoe[j]
                k += 1

    return newCoe

u"""
    popCol
    配列coeのcol列目を返す
"""
def popCol(coe,col):
    line = coe[0][col]
    for i in range(1,coe.shape[0]):
        line = np.vstack([line,coe[i][col]])
    return line

u"""
    plot
    グラフ化する
"""
def graphPlot(coe):
    plt.figure(1)
    plt.subplot(111)
    for i in range(dimension):
        plt.plot(popCol(coe,i), label = "X" + str(i+1))
    plt.legend()
    #plt.xlim([0,12])   #x軸の端を指定したい際に使用
    #plt.ylim([-20,100])    #y軸の端を指定したい際に使用
    plt.show()  その場で見たい時に使用
    #plt.savefig(argv[2]+".png")    #保存をしたい際に使用


u"""
    writeCSV
    解の変化の流れをCSVファイルに保存
"""
def writeCSV(coe):
    try:
        fp2 = open(argv[2]+".csv", 'w',newline='')
        csvWriter = csv.writer(fp2)
        for data in coe:
            csvWriter.writerow(data)
        fp2.close()
    except IOError:
        print ("cannot make file.")
        exit()
    except Exception as e:
        print('type' + str(type(e)))
        exit()



u"""
    dimension:  次元
    mat:        拡大行列
    coe:        解の流れを記録する二次元配列
"""
if __name__ == '__main__':
    dimension,mat=importData()
    print(str(dimension))
    coe = np.zeros(dimension)   #初期値が全部ゼロならこっちを使用
    #coe = np.array([1,2,3,4])])    #初期値を指定するならこっち(必要に応じてコマンドライン引数使用)次元に注意
    mat = matrixSet(dimension,mat)
    if possibility(dimension,mat):
        mat = deformation(mat)
        print(coe.shape[0]-1)
        coe = np.vstack([coe,firstCalc(mat,coe)])
        while check(coe):
            coe = np.vstack([coe,calc(mat,coe)])
        print("the answers are "+ str(coe[coe.shape[0]-1]))
        writeCSV(coe)
        graphPlot(coe)

    else:
        print("this case can not calc.")
