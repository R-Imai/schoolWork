# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#   Name:		NaturalLanguageProcessing.py
#	Author:		R.Imai
#	Created:	2015 / 11 / 25
#	Last Date:	2015 / 11 / 25
#	Note:       コマンドライン引数は、(入力ファイル名)(区切り文字数)(出力ファイル名)
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
        print("このプログラムは自然言語処理をするものです。")
        check = True
    if argNum < 4:
        check = True
    return check

def usage():
    print("コマンドライン引数は,(入力ファイル名)(区切り文字数)(出力ファイル名)")
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
    fp1 = fileOpen(argv[1],'r')
    read = fp1.read()
    fp1.close()
    return read

def mkMap(txt,num):
    Map = {}
    for i in range(len(txt) - num):
        Str = txt[i]
        for j in range(i + 1,i + num):
            Str = Str + txt[j]
        if Str not in Map:
            Map[Str] = 1
        else :
            Map[Str] += 1

    return Map

if __name__ == '__main__':
    if checkUsage():
        usage()
    txt = importData()
    txt = txt.replace("\n","")
    txt = txt.replace(" ","_")
    txt = txt.replace("\"","")
    txt = txt.replace("\'","")
    if argv[2] == "check":
        print(txt)
        print(len(txt))
        exit()
    fp2 = fileOpen(argv[3],'w')
    Map = mkMap(txt,int(argv[2]))
    for k, v in sorted(Map.items(), key=lambda x:x[1], reverse=True):
        fp2.write(k + "\t" + str(v) + "\n")
        #print(k + ": " + str(v))
