
import math
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.special import yv
from scipy.stats import linregress
directory = "C:\\Users\\user\\Documents\\DLAfiles"

def BuildNames(minSeed,maxSeed,maxPoints,metric):
    fileNames = []
    for seed in range(minSeed,maxSeed+1):
        fileName = str(seed)+"-"+str(maxPoints)+"-output"+str(metric)+".txt"
        fileNames.append(fileName)
    return fileNames

def AvRad(minSeed,maxSeed,maxPoints,metric=1):
    fileNames = BuildNames(minSeed,maxSeed,maxPoints,metric)
    averageRadByPointCount = []
    filesSearched = 0

    for filename in os.listdir(directory):
        if filename in fileNames:
           numPoints = 0 #this is numPoints - 1 for indexing
           #print(filename)
           if filesSearched == 0:
               filesSearched+=1
               for line in open(os.path.join(directory,filename),'r'):
                   x,y = line.split(':')
                   radius = distance(float(x),float(y),metric)
                   averageRadByPointCount.append(radius)
           else:
               filesSearched+=1
               for line in open(os.path.join(directory,filename),'r'):
                   x,y = line.split(':')
                   radius = distance(float(x),float(y),metric)
                   averageRadByPointCount[numPoints] += (radius - averageRadByPointCount[numPoints])/filesSearched # rolling average of radius for given number of points
                   numPoints+=1
    return range(1,maxPoints+1),averageRadByPointCount
    
def Plot(X,Y):
    plt.figure(dpi=300)
    plt.scatter(X,Y,s=1,linewidths=0,marker=',')

def LogPlot(X,Y):
    X=[math.log(x) for x in X]
    Y=[math.log(y) for y in Y]
    slope, intercept, r_value, p_value, std_err = linregress(X,Y)
    #Plot(X,Y)
    return slope
    

def PlotCluster(seed,maxPoints,metric,maxlines=0):
    XVals = []
    YVals = []
    filename = str(seed)+"-"+str(maxPoints)+"-output"+str(metric)+".txt"
    if maxlines>0:
        savename = str(seed)+"-"+str(maxlines)+"-output"+str(metric)+".png"
    else:    
        savename = str(seed)+"-"+str(maxPoints)+"-output"+str(metric)+".png"
    linecount=0
    maxdist = 0
    for line in open(os.path.join(directory,filename),'r'):
        linecount+=1
        if maxlines>0:
            if linecount>maxlines:
                break
        xVal,yVal = line.split(':')
        XVals.append(float(xVal))
        YVals.append(float(yVal))
    #savename = str(seed)+"-"+str(linecount-1)+"-output"+str(metric)+".png"
    Plot(XVals,YVals)
    plt.gca().set_aspect('equal')
    minY,maxY = plt.ylim()
    minX,maxX = plt.xlim()
    bound = max(abs(minX),abs(minY),abs(maxX),abs(maxY))
    plt.xlim(-bound,bound)
    plt.ylim(-bound,bound)
    plt.savefig(os.path.join(directory,'figures',savename))
    plt.show()

def DistanceAnalyse(seed,maxPoints,metric = 1):
    filename = str(seed)+"-"+str(maxPoints)+"-output"+str(metric)+".txt"
    pairs = []
    for line in open(os.path.join(directory,filename),'r'):
        xVal,yVal = line.split(':')
        pairs.append((float(xVal),float(yVal)))
    for pair in pairs:
        if pair == (2.987474, -3.012526):
            t = 2
        dist = 10000
        for pair2 in pairs:
            if pair2==pair:
                continue
            if abs(pair[0]-pair2[0])+abs(pair[1]-pair2[1]) < dist:
                dist = abs(pair[0]-pair2[0])+abs(pair[1]-pair2[1])
        print(dist,pair)

def Regression(minSeed,maxSeed,maxPoints,metric):
    fileNames = BuildNames(minSeed,maxSeed,maxPoints,metric)
    dataPointsRadius = []
    numPoint=[]
    for filename in os.listdir(directory):
        if filename in fileNames:
            pointNum=1
            for line in open(os.path.join(directory,filename),'r'):
                numPoint.append(pointNum)
                pointNum+=1
                x,y = line.split(':')
                radius = distance(float(x),float(y),metric)
                dataPointsRadius.append(float(radius))
    LogPlot(numPoint,dataPointsRadius)
    plt.show()
         
def distance(x,y,metric):
    if metric==1:
        return abs(x)+abs(y)
    elif metric == 2:
        return math.sqrt(abs(x)^2+abs(y)^2)
    else:
        print("invalid metric")
        input()
        return 0

def Compare(minSeed,maxSeed,maxPoints):
    X1,Y1 = AvRad(minSeed,maxSeed,maxPoints,1)
    X2,Y2 = AvRad(minSeed,maxSeed,maxPoints,2)
    LogPlot(X1,Y1)
    LogPlot(X2,Y2)
    plt.show()
    
def Dimension(seed,maxPoints,metric,maxLines=0):
    if maxLines == 0:
        maxLines=maxPoints
    filename = str(seed)+"-"+str(maxPoints)+"-output"+str(metric)+".txt"
    xPts = []
    yPts = []
    radius = 1
    lineNum=0
    for line in open(os.path.join(directory,filename),'r'):
        if lineNum == maxLines:
            break
        lineNum+=1
        xVal,yVal = line.split(':')
        xVal=float(xVal)
        yVal=float(yVal)
        radius = max(Dist_2(xVal,yVal),radius)
        xPts.append(lineNum)
        yPts.append(radius)
    return LogPlot(xPts,yPts)
    #plt.show()

def Dist_2(xVal,yVal):
        return math.sqrt(xVal*xVal+yVal*yVal)
    
def Dist_1(xVal,yVal):
        return abs(xVal)+abs(yVal)
        
    
def RangeDimension(minSeed,maxSeed,maxPoints,metric,dimension=Dimension):
    linecount = 0
    ave = 0
    for seed in range(minSeed,maxSeed):
        dim = dimension(seed,maxPoints,metric)
        print(dim)
        ave= (linecount*ave+dim)/(linecount+1)
        linecount+=1
    return ave
    
def Rotation(seed,maxPoints,metric,maxLines=0):
    ave = 0
    if maxLines == 0:
        maxLines = maxPoints
    linecount=0
    filename = str(seed)+"-"+str(maxPoints)+"-output"+str(metric)+".txt"
    for line in open(os.path.join(directory,filename),'r'):
        if linecount>maxLines+1:
            break
        xVal,yVal = line.split(':')
        xVal=abs(float(xVal))
        yVal=abs(float(yVal))
        if xVal < yVal:
            ave = (linecount*ave+arctan(yVal,xVal))/(linecount+1)
        else:
            ave= (linecount*ave+arctan(xVal,yVal))/(linecount+1)
        linecount+=1
    return ave

def RotationRange(minSeed,maxSeed,maxPoints,metric):
    linecount = 0
    ave = 0
    maxRot =0
    minRot = 1000
    for seed in range(minSeed,maxSeed):
        rot = Rotation(seed,maxPoints,metric)
        print(rot)
        maxRot=max(rot,maxRot)
        minRot=min(rot,minRot)
        ave= (linecount*ave+rot)/(linecount+1)
        linecount+=1
    return ave,maxRot,minRot

def DimensionIntervals():
    filename = str(997344471)+"-"+str(5000000)+"-output"+"Triangle"+".txt"
    xPts = []
    yPts = []
    lineNum=0
    radius = 1
    for line in open(os.path.join(directory,filename),'r'):
        lineNum+=1
        xVal,yVal = line.split(':')
        xVal=float(xVal)
        yVal=float(yVal)
        radius = max(Dist_2(xVal,yVal),radius)
        xPts.append(lineNum)
        yPts.append(radius)
        if lineNum % 1000000 == 0:
            print(LogPlot(xPts,yPts))



def PlotAll(minSeed,maxSeed,maxPoints,metric):
    XVals = []
    YVals = []
    maxbound=0
    for seed in range(minSeed,maxSeed):
        filename = str(seed)+"-"+str(maxPoints)+"-output"+str(metric)+".txt"
        for line in open(os.path.join(directory,filename),'r'):
            xVal,yVal = line.split(':')
            xVal=float(xVal)
            yVal=float(yVal)
            XVals.append(xVal)
            YVals.append(yVal)
            maxbound=max(abs(xVal),abs(yVal),maxbound)
    savename =str(minSeed)+"-"+str(maxSeed)+"-"+str(maxPoints)+"-output"+str(metric)+".png"
    Plot(XVals,YVals)
    plt.gca().set_aspect('equal')
    minY,maxY = plt.ylim()
    minX,maxX = plt.xlim()
    bound = max(abs(minX),abs(minY),abs(maxX),abs(maxY))
    plt.xlim(-bound,bound)
    plt.ylim(-bound,bound)
    plt.xticks([])
    plt.yticks([])
    plt.savefig(os.path.join(directory,'figures',savename))
    plt.show()

def DimensionGyration(seed,maxPoints,metric,maxLines = 0):
    if maxLines == 0:
        maxLines=maxPoints
    filename = str(seed)+"-"+str(maxPoints)+"-output"+str(metric)+".txt"
    xPts = []
    yPts = []
    radius = 1
    lineNum=0
    for line in open(os.path.join(directory,filename),'r'):
        if lineNum == maxLines:
            break
        lineNum+=1
        if lineNum==1:
            continue
        xVal,yVal = line.split(':')
        xVal=float(xVal)
        yVal=float(yVal)
        dist=Dist_2(xVal,yVal)
        radius = ((lineNum-1)*radius+dist*dist)/lineNum
        xPts.append(lineNum)
        yPts.append(math.sqrt(radius))
    return LogPlot(xPts,yPts)
def arctan(xVal,yVal):
    if xVal == 0:
        return 0
    return math.atan(yVal/xVal)
if __name__ == '__main__':
    #DimensionIntervals()
    #print(RotationRange(767526740,767526800,500000,"1"))
    #PlotAll(43786500,43786560,500000,"SL")
    #print(Rotation(17859141,5000000,"Sl"))
    #print(1/RangeDimension(6436920,6436980,200000,"1"))
    #print(1/RangeDimension(997344470,997344500,500000,"SnapNear"))
    PlotCluster(9933734,5000000,"SnapAlways")
    #print(Rotation(9933734,5000000,"SnapAlways"))
    #for i in [1000000,2000000,3000000,4000000,5000000]:
    #    print(Dimension(17859141,5000000,"SL",i))

    