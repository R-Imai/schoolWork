# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#   Name:		MFCC.py
#	Author:		R.Imai
#	Created:	2016 / 06 / 22
#	Last Date:	2016 / 07 / 24
#	Note:
#-------------------------------------------------------------------------------
import random
import numpy as np

class HMM:
    def __init__(self, transProb, stayProb, valProb, label):
        self.transProb = transProb  #次に行く確率
        self.stayProb = stayProb    #居座る確率
        self.label = label
        self.valProbList = valProb
        self.setValProb(valProb)      #出力確率
        self.state = 0
        self.stateNum = len(transProb)
        self.valNum = len(valProb)

    def showState(self):
        for i in range(self.stateNum):
            print("----------pot" + str(i) + "----------")
            print("\t----------")
            for label in self.label:
                print("\t" + label + ": " + str(self.valProb[i][label]))
            print("\t----------")
            print("trans probability" + str(self.transProb[i]))
            print("stay probability" + str(self.stayProb[i]))
            print("------------------------")

    def setValProb(self, valprob):
        self.valProb = [{} for i in range(len(valprob))]
        for j in range(len(valprob)):
            for i in range(len(self.label)):
                self.valProb[j][self.label[i]] = valprob[j][i]


    def forward(self, inputModel):
        colLen = self.stateNum
        rowLen = len(inputModel) - colLen + 1
        workspace = [[0 for i in range(colLen)] for j in range(rowLen)]
        #print(str(len(workspace)) + ", " + str(len(workspace[0])))
        #print(workspace[colLen - 1][rowLen - 1])
        calcSpace = [0, 0]
        workspace[0][0] = self.valProb[0][inputModel[0]]
        for i in range(1, rowLen):
            #print(str(i) + "/" + str(rowLen))
            workspace[i][0] = workspace[i - 1][0]*self.stayProb[0]*self.valProb[0][inputModel[i]]
        for j in range(1, colLen):
            #print(str(j) + "/" + str(colLen))
            workspace[0][j] = workspace[0][j - 1]*self.transProb[j - 1]*self.valProb[j][inputModel[j]]
        for i in range(1, rowLen):
            for j in range(1, colLen):
                calcSpace[0] = workspace[i - 1][j]*self.stayProb[j]*self.valProb[j][inputModel[i + j]]
                calcSpace[1] = workspace[i][j - 1]*self.transProb[j - 1]*self.valProb[j][inputModel[i + j]]
                workspace[i][j] = sum(calcSpace)
        return workspace[rowLen - 1][colLen - 1]*self.transProb[len(self.transProb) - 1]

    def vitarbi(self, inputModel):
        colLen = self.stateNum
        rowLen = len(inputModel) - colLen + 1
        workspace = [[0 for i in range(colLen)] for j in range(rowLen)]
        #print(str(len(workspace)) + ", " + str(len(workspace[0])))
        #print(workspace[colLen - 1][rowLen - 1])
        calcSpace = [0, 0]
        workspace[0][0] = self.valProb[0][inputModel[0]]
        for i in range(1, rowLen):
            #print(str(i) + "/" + str(rowLen))
            workspace[i][0] = workspace[i - 1][0]*self.stayProb[0]*self.valProb[0][inputModel[i]]
        for j in range(1, colLen):
            #print(str(j) + "/" + str(colLen))
            workspace[0][j] = workspace[0][j - 1]*self.transProb[j - 1]*self.valProb[j][inputModel[j]]
        for i in range(1, rowLen):
            for j in range(1, colLen):
                calcSpace[0] = workspace[i - 1][j]*self.stayProb[j]*self.valProb[j][inputModel[i + j]]
                calcSpace[1] = workspace[i][j - 1]*self.transProb[j - 1]*self.valProb[j][inputModel[i + j]]
                workspace[i][j] = max(calcSpace)
        return workspace[rowLen - 1][colLen - 1]*self.transProb[len(self.transProb) - 1]


    def outputSimu(self):
        output = []
        state = 0
        while state != self.stateNum:
            pick = random.random()
            for i in range(self.valNum):
                if pick < sum(self.valProbList[state][:i + 1]):
                    output.append(self.label[i])
                    break

            #動くかどうするか
            judge = random.random()
            if judge < self.transProb[state]:
                state += 1
        #print(output)
        return output
