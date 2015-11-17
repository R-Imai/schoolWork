# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#   Name:		NewtonRaphsonMethod.py
#	Author:		R.Imai
#	Created:	2015 / 10 / 28
#	Last Date:	2015 / 10 / 30
#	Note:	ニュートン・ラプソン法
#           コマンドライン引数は数式,初期値
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

ACCURACY = 0.00000001
NMAX = 25
palette = ["#ff0000","#0000ff","#00ff00","#ff8c00","#a600ff","#ff61d7","#1e90ff","#77ff77","#ffff77","#d71a80","#be0b0d","#1a0099","#0e8154","#96781c","#6c128b","#f9a8e4","#9cceff","#a5f0a5","#eff78d","#dc9adf"]

checker = True
detect = 0
coe = []
eq = []

def compileArg():
    global coe
    global eq

    Line = []
    String = re.split(r"[-]",argv[1])
    if argv[1].startswith("-"):
        String.pop(0)
        String[0] = "-" + String[0]
    #print(String)
    for i in range(1,len(String)):
        String[i] = "-" + String[i]
    for line in String:
        Line.extend(re.split(r"[+]",line))
    String = []
    for line in Line:
        element = re.split(r"[/]",line)
        for i in range(1,len(element)):
            element[i] = "/" + element[i]
        String.append(element)
    Line = []
    Element = []
    for element in String:
        for line in element:
            line = line.replace("**","p")
            Element.extend(re.split(r"[*]",line))
        Line.append(Element)
        Element = []
    #print (Line)

    for line in Line:
        if line[0].replace(".","").replace("-","").isdigit():
            if len(line) > 1 and line[1].replace(".","").replace("/","").isdigit():
                coe.append(float(line[0])/float(line[1].replace("/","")))
                line.pop(0)
                line.pop(0)
            else :
                coe.append(float(line[0]))
                line.pop(0)
        elif line[0].startswith("-"):
            line[0] = line[0].replace("-","")
            coe.append(-1.0)
        else :
            coe.append(1.0)
    #print(coe)

    for line in Line:
        subList = []
        for element in line:
            if "cos" in element:
                subList.append("c")
                subList.append(element.replace("cos",""))
            elif "sin" in element:
                subList.append("s")
                subList.append(element.replace("sin",""))
            elif "tan" in element:
                subList.append("t")
                subList.append(element.replace("tan",""))
            elif "p" in element:
                exp = re.split(r"[p]",element)
                subList.append("p"+exp[0])
                subList.append(exp[1])

            elif element.startswith("x"):
                subList.append("1")
                subList.append(element)
        eq.append(subList)
    #print(Line)
    #print(eq)

def compileEq(operator,contents,x):
    if contents == "x":
        num = x
    elif contents.replace(".","").replace("-","").isdigit():
        num = float(contents)
    elif contents.replace("x","").replace(".","").replace("-","").isdigit():
        num = x*float(contents.replace("x",""))
    else :
        print ("varue error:"+contents)
        exit()

    if operator == "c":
        result = np.cos(num)
    elif operator == "s":
        result = np.sin(num)
    elif operator == "t":
        result = np.tan(num)
    elif operator == "px":
        result = pow(x,num)
    elif "p" in operator:
        result = pow(float(operator.replace("p","")),num)
    elif operator == "1":
        result = num
    else :
        print("value error:"+operator)

    return result

def eqation(x):
    ans = 0
    cnt = 0
    for item in eq:
        result = coe[cnt]
        for i in range(0,int(len(item)/2)):
            result *= compileEq(item[2*i],item[2*i+1],x)
        ans += result
        cnt += 1
    return ans

def differential(x):
    return (eqation(x) - eqation(x - 0.000000001)) / 0.000000001

def calc(x):
    global checker
    global detect
    delta = - eqation(x[len(x)-1]) / differential(x[len(x)-1])
    x.append(x[len(x)-1] + delta)
    if abs(delta) < ACCURACY:
        checker = False
        detect = 1
    return x

def Plot(ans):
    print ("ploting...")
    x1 = [min(ans)-5.0]
    #x1 = [-40]
    y1 = [eqation(x1[0])]
    for i in range(int((min(ans)-5.0)*10-1),int((max(ans)+5.0)*10)):
    #for i in range(-400,400):
        x1.append(i*0.1)
        y1.append(eqation(i*0.1))

    plt.figure(figsize=(16, 9))
    plt.subplot(111)
    plt.plot(x1,y1,label = argv[1]+"=0",color = 'k')
    for i in range(len(ans)-1):
        endPoint = [min([ans[i],ans[i+1]]),max([ans[i],ans[i+1]])]
        liner = []
        plt.plot(ans[i],eqation(ans[i]),"o",color = palette[(i)%len(palette)])
        liner.append(eqation(ans[i]) - (ans[i] - endPoint[0]) * differential(ans[i]))
        liner.append(eqation(ans[i]) - (ans[i] - endPoint[1]) * differential(ans[i]))
        #print(liner)
        plt.plot(endPoint,liner,"--",label = str(i+1)+" times calc result",color = palette[(i)%len(palette)])
    plt.axhline(0,color = 'r',)
    #plt.xlim(-40,30)
    #plt.ylim([-7,7])
    plt.xlabel("x-axies")
    plt.ylabel("y-axies")
    plt.legend(loc='best')
    plt.show()
    #plt.savefig("Fig6.png")


def printf(ans):
    if detect == 1:
        print("the answer is : " + str(ans) + "\n")
    elif detect == 2:
        print("error : exceeded the limit number of trials.")
    elif detect == 3:
        print("error : divided by 0.")

if __name__ == '__main__':
    compileArg()
    #print(coe)
    #print(eq)
    n = 0
    x = calc([float(argv[2])])
    n += 1

    while checker:
        #print(x[len(x)-1])
        x = calc(x)
        n += 1
        if(n > NMAX):
            checker = False
            detect = 2;
    for ans in x:
        print(ans)
    printf(x[len(x)-1])

    Plot(x)
    #print(eqation(x[len(x)-1]))
