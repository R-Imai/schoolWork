# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        	NomalDistribution.py
# Author:      	R.Imai
# Created:     	2015/10/23
# Last Date:   	2015/10/23
# Note:         正規分布のプロット
#               コマンドライン引数は,μ,σ^2の順
#-------------------------------------------------------------------------------

import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from math import *
import codecs

argv = sys.argv
argNum = len(sys.argv)

def calc(u,sig,x):
    Denom = sqrt(2*pi*sig)
    Numer = exp(-pow(x-u,2)/(2*sig))
    return Numer/Denom

def plot(u,sig):
    x = [u-sqrt(sig)*5]
    y = [calc(u,sig,u-sqrt(sig)*5)]
    for i in range(int((u-sqrt(sig)*5)*10),int((u+sqrt(sig)*5)*10)):
        x.append(i*0.1)
        y.append(calc(u,sig,i*0.1))
    plt.plot(x,y,label = "eqation1")
    plt.xlabel("Measured value")
    plt.ylabel("Probability density")
    #plt.xlim([-30,30])
    #plt.ylim([0,1])
    plt.show()


if __name__ == '__main__':
    plot(int(argv[1]),int(argv[2]))
