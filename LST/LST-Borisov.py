#!/usr/bin/python

import datetime
import numpy as np
import matplotlib.pyplot as plt
import LST


#JD=LST.CaltoJD(now="now")
print "Now JD",LST.CaltoJD(now="now")
JD=LST.CaltoJD(2019,10,31,8,0,0)
print  "JD in .",JD
#print JDList

#The Longitude of Honolulu
LAT=LST.dmstodec(19,49,27)
LON=LST.dmstodec(155,28,41,"W")
#LAT=LST.dmstodec(30,0,0,)
#LON=LST.dmstodec(130,0,0,"W")
timezone=-10.0
JDList=np.linspace(int(JD)-timezone/24.0,int(JD)-timezone/24.0+0.999,240)

print "The LAT & LON of observ is", LAT,LON

'''
3c84    0319+415        03:19:48.1601   +41:30:42.103
RA=dmstodec(3,19,48.1601)
DEC=dmstodec(41,30,42.103)

3c454.3 2253+161        22:53:57.7479   +16:08:53.560
RA=dmstodec(22,53,57.7479)
DEC=dmstodec(16,8,53.560)
RA=dmstodec(22,53,57.7479)
DEC=dmstodec(16,8,53.560)
'''
RA=LST.dmstodec(10,21,15.42)
DEC=LST.dmstodec(8,26,22.6)
print "RA =",RA," DEC =",DEC

print "LST in Obser",LST.getLST(LAT,LON,JD) ,"or",LST.dectodms(LST.getLST(LAT,LON,JD))

print "HA is", LST.getHA(LAT,LON,JD,RA)

print "AZ",LST.getAzEL(RA,DEC,JD,LAT,LON)[0],LST.getAzEL(RA,DEC,JD,LAT,LON)[0]-360.
print "EL",LST.getAzEL(RA,DEC,JD,LAT,LON)[1]

AZList=[]
ELList=[]
HAList=[]
LTList=[]
for i in JDList:
    AZList.append(LST.getAzEL2(RA,DEC,i,LAT,LON)[0])
    ELList.append(LST.getAzEL2(RA,DEC,i,LAT,LON)[1])
    HAList.append(LST.getHA(LAT,LON,i,RA))
    LTList.append(((i*24.0+timezone) % 24)-12)
    print i,LTList[-1],AZList[-1] ,ELList[-1],HAList[-1]
#print ELList

fig, (ax1,ax2) = plt.subplots(2,1)
ax1.plot(LTList,ELList,c='green', linewidth=1,label='stat')
ax2.plot(LTList,HAList,c='green')
ax2.set_ylim(-15,15)
plt.show()
