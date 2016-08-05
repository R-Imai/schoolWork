#coding:utf-8
#-------------------------------------------------------------------------------
#   Name:		DP_Matching.py
#	Author:		R.Imai
#	Created:	2016 / 05 / 20
#	Last Date:	2016 / 05 / 20
#	Note:
#-------------------------------------------------------------------------------
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import argparse
import csv
import glob
import math


slantCoe = 1    #math.sqrt(2)    #斜めの倍率

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("dirName", help = "Directory there is a feature data")
    parser.add_argument(
            "-p", "--plot",
            type = str,
            dest = "plot",
            default = None,
            nargs = 4,
            help = "plot result graph[teach, label, check, label]"
    )
    parser.add_argument(
            "-s", "--save",
            type = str,
            dest = "save",
            default = None,
            help = "save result graph name"
    )
    parser.add_argument(
            "-t", "--test",
            type = int,
            dest = "test",
            nargs = 2,
            default = [0, 1],
            help = "set check user point [teach, check]"
    )


    return parser.parse_args()

def getDirList(dirName):
    fileList = []
    dirList = []
    for elem in glob.glob(dirName +"/*"):
        fileList.append(glob.glob(elem + "/*"))

    return fileList

def importFile(path):
    try:
        fp = open(path, 'r')
        reader = csv.reader(fp,delimiter=' ')
    except IOError:
        print (path + "cannot be opened.")
        exit()
    except Exception as e:
        print('type'+ str(type(e)))
        print(path)
        exit()
    data = []
    for i,elem in enumerate(reader):
        if i == 1:
            label = elem[0]
        elif i >= 3:
            data.append([float(i) for i in elem[:-1]])
    return data,label


def mkMatrix(teach, test):
    matrix = [[0 for i in range(len(teach))] for j in range(len(test))]
    for j, testData in enumerate(test):
        for i, teachData in enumerate(teach):
            matrix[j][i] = np.linalg.norm(np.array(testData) - np.array(teachData))
    #print(matrix)
    return matrix

def calcMinRoute(matrix):
    row = len(matrix[0])
    col = len(matrix)
    routeMatrix = [[0 for i in range(row)] for j in range(col)]
    routeMatrix[0][0] = matrix[0][0]
    for i in range(1, row):
        routeMatrix[0][i] = routeMatrix[0][i - 1] + matrix[0][i]
    for j in range(1, col):
        routeMatrix[j][0] = routeMatrix[j - 1][0] + matrix[j][0]

    for j in range(1, col):
        for i in range(1, row):
            calcSpace = []
            calcSpace.append(routeMatrix[j - 1][i] + matrix[j][i])
            calcSpace.append(routeMatrix[j - 1][i - 1] + slantCoe*matrix[j][i])
            calcSpace.append(routeMatrix[j][i - 1] + matrix[j][i])
            routeMatrix[j][i] = min(calcSpace)

    return routeMatrix[col - 1][row - 1]/(col + row), routeMatrix


def DP_matching(teachData, testData):
    num = []
    minNum = 99999999
    for checkData in teachData:
        mat = mkMatrix(checkData, testData)
        minRoute, routeMatrix = calcMinRoute(mat)
        if minRoute < minNum:
            minMat = mat
            minRouteMat = routeMatrix
            minNum = minRoute
        num.append(minRoute)
    #print(np.array(num))
    return np.argmin(np.array(num)), minMat, minRouteMat

def plotMat(mat, locus, save):
    x = np.arange(len(mat[0])+1)
    y = np.arange(len(mat)+1)
    X, Y = np.meshgrid(x, -y)
    plt.pcolor(X, Y, np.array(mat), cmap=plt.cm.binary)
    plt.colorbar()
    plt.plot(locus[0],locus[1])
    plt.xlim(0, len(mat[0]))
    plt.ylim(-len(mat),0)
    if save is None:
        plt.show()
    else:
        plt.savefig(save + ".png")

def plotRoute(mat):
    y = len(mat) - 1
    x = len(mat[0]) - 1
    locusX = [x + 0.5]
    locusY = [-y - 0.5]
    locus = []
    while x != 0 or y != 0:
        if x == 0:
            y -= 1
        elif y == 0:
            x -= 1
        else:
            #print(str(x) + ", " + str(y))
            num = np.argmin(np.array([mat[y - 1][x], mat[y - 1][x - 1], mat[y][x - 1]]))
            if num == 0:
                y -= 1
            elif num == 1:
                x -= 1
                y -= 1
            elif num == 2:
                x -= 1
        locusX.append(x + 0.5)
        locusY.append(-y - 0.5)
    locus.append(locusX)
    locus.append(locusY)
    """
    plt.plot(locusX,locusY)
    plt.xlim(0, len(mat[0]) - 1)
    plt.ylim(-len(mat) + 1)
    plt.show()
    """
    return locus


if __name__ == '__main__':
    arg = parse_arguments()
    fileList = getDirList(arg.dirName)
    feature = []
    labelList = []
    for dataList in fileList:
        elemList = []
        labelElem = []
        for fileName in dataList:
            data, label = importFile(fileName)
            elemList.append(data)
            labelElem.append(label)
        feature.append(elemList)
        labelList.append(labelElem)

    if not(arg.plot is None):
        for label, data in zip(labelList[int(arg.plot[0])], feature[int(arg.plot[0])]):
            if label == arg.plot[1]:
                check = data
                break
        for label, data in zip(labelList[int(arg.plot[2])], feature[int(arg.plot[2])]):
            if label == arg.plot[3]:
                teach = data
                break
        mat = mkMatrix(teach, check)
        minRoute, routeMatrix = calcMinRoute(mat)
        print(minRoute)
        plotMat(mat, plotRoute(routeMatrix), arg.save)


    else:
        cnt = 0
        for i,elem in enumerate(feature[arg.test[1]]):
            n, mat, Rmat = DP_matching(feature[arg.test[0]], elem)
            if i == n:
                cnt += 1
            else:
                print(labelList[arg.test[0]][n] + "::" + labelList[arg.test[1]][i])
            plotMat(mat, plotRoute(Rmat))
            #plotRoute(mat)
            if i % 10 == 0:
                print (str(i) + "%")
        print(cnt)
