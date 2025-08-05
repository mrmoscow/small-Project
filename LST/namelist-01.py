#!/usr/bin/python

import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import LST

#           name ra ram ras +-dec

class JD():
    def __init__(self,year,month,day,hour,mins,sec):
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        self.hour = int (hour)
        self.mins = int (mins)
        self.sec = float (sec)
        self.JD=LST.CaltoJD(year,month,day,hour,mins,sec)
        print (year,month,day,hour,mins,sec,"JD=",self.JD)
        self.nighList=np.linspace(self.JD-1,self.JD+1,500)
        self.yearList=np.zeros(shape=(11,500))
        for i in range(11) :
            #print(i-5,month+i-5)
            year2=year
            month2=month+i-5
            if (month+i-5) <=0:
                year2=year-1
                month2=month+i-5+12
            elif (month+i-5)>12:
                year2= year+1
                month2=month+i-5-12
            JD2=LST.CaltoJD(year2,month2,1,0,0,0)
            self.yearList[i,:]=np.linspace(JD2-1,JD2+1,500)
    def toJD(name):
        return 30

source00=[]
with open('3c_catalog', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        #print(row)
        d=row[0].split()
        for i in range (1,7):
            d[i]=float(d[i])
        #name=d[0]
        source00.append([d[0],d[1],d[2],d[3],d[4],d[5],d[6]])
        #print(namelist[0],namelist[1],namelist[2])

print(source00)

sourcelist=[["3c84",3,19,48.1601,+41,30,42.103],
            ["3c454.3",22,53,57.7480,+16,8,53.5630]]


print (sourcelist)
print (sourcelist[1][0])

time1=JD(2020,1,1,0,0,0)
#print (time1.year,time1.JD)
print (time1.yearList)


year=2019
month=10
for i in range(11) :
    #print(i-5,month+i-5)
    year2=year
    month2=month+i-5
    if (month+i-5) <=0:
        year2=year-1
        month2=month+i-5+12
    elif (month+i-5)>12:
        year2= year+1
        month2=month+i-5-12
#JD=500.2
#nighList=np.linspace(JD-1,JD+1,500)
#yearList=np.zeros(shape=(2,500))
#yearList[0,:]=
#print (yearList)
#print(i-5,month+i-5,year,month2,year2)

print (LST.normalize0toN(370,360))
print (LST.normalize0toN(200,24))
