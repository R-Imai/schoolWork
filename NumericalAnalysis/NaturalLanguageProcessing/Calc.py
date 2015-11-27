# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#   Name:		Calc.py
#	Author:		R.Imai
#	Created:	2015 / 11 / 25
#	Last Date:	2015 / 11 / 25
#	Note:       読み込むcsvファイルの名称は「名前+連番+.csv」であること
#               コマンドライン引数は、「「読み込むcsvの(番号.csv)を除いたやつ」 連番の最大数 出力ファイル」
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

def checkUsage():
    check = False
    if argv[1] == "help" or argv[1] == "-h" or argv[1] == "usage":
        print("このプログラムはNaturalLanguageProcessing.pyの出力ファイルを操作するものです。")
        check = True
    elif argNum < 5:
        check = True
    return check

def usage():
    print("読み込むcsvファイルの名称は「名前+連番+.csv」であること")
    print("コマンドライン引数は,(読み込むcsvの共通部分)(連番の最大数)(出力ファイル名)(mode)")
    print("mode:\tsum:\t合計\n    \tratio:\tパーセンテージ\n")
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

def importData(path,Map,numChar):
    fp = fileOpen(path,'r')
    reader = csv.reader(fp, delimiter = '\t')
    cnt = 0
    for row in reader:
        if row[0] not in Map:
            Map[row[0]] = int(row[1])
            numChar += int(row[1])
        else :
            Map[row[0]] += int(row[1])
            numChar += int(row[1])
    fp.close()
    return Map,numChar

def Sum():
    Map = {}
    numChar = 0
    for i in range(1,int(argv[2])+1):
        Map,numChar = importData(argv[1] + str(i) + ".csv", Map, numChar)

    fp2 = fileOpen(argv[3],'w')
    for k, v in sorted(Map.items(), key=lambda x:x[1], reverse=True):
        fp2.write(k + "\t" + str(v) + "\n")
        #print(k + ": " + str(v))

def Ratio():
    Map = {}
    numChar = 0
    for i in range(1,int(argv[2])+1):
        Map,numChar = importData(argv[1] + str(i) + ".csv", Map, numChar)

    fp2 = fileOpen(argv[3],'w')
    for k, v in sorted(Map.items(), key=lambda x:x[1], reverse=True):
        fp2.write(k + "\t" + str(v/numChar) + "\n")
        #print(k + ": " + str(v))

if __name__ == '__main__':
    if checkUsage():
        usage()
    if argv[4] == "sum":
        Sum()
    elif argv[4] == "ratio":
        Ratio()
    else :
        print("mode:\tsum:\t合計\n    \tratio:\tパーセンテージ\n")
