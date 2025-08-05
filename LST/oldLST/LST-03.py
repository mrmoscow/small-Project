#!/usr/bin/python

import datetime
import numpy as np
import matplotlib.pyplot as plt
import LST

timezone=-10
tz=timezone
timezoneday=timezone/24.0
#JD=LST.CaltoJD(now="now")
print " JD now is ",LST.CaltoJD(now="now")
JD=LST.CaltoJD(2020,1,1,0,0,0)
print "Cal JD on",JD
JDList=np.linspace(JD-1,JD+1,500)
#print JDList

#The Longitude of Nobeyama
#LAT=LST.dmstodec(35,56,30,"N")
#LON=LST.dmstodec(138,28,33,"E")
#timezone=9

#The Longitude of Honolulu
LAT=LST.dmstodec(19,49,27)
LON=LST.dmstodec(155,28,41,"W")
timezone=-10

#The location of Lulin
#LAT=LST.dmstodec(23,28,9,"N")
#LON=LST.dmstodec(120,52,22,"E")
#timezone=+8

tz=timezone
timezoneday=timezone/24.0

print "The observator position is LAT=",LAT,"LON=",LON

#3c84    0319+415        03:19:48.1601   +41:30:42.103
#RA=LST.dmstodec(3,19,48.1601)
#DEC=LST.dmstodec(41,30,42.103)
#3c454.3 2253+161        22:53:57.7479   +16:08:53.560
RA=dmstodec(22,53,57.7479)
DEC=dmstodec(16,8,53.560)
#RA=dmstodec(22,53,57.7479)
#DEC=dmstodec(16,8,53.560)

#GL1771
#RA=LST.dmstodec(15,25,47.56)
#DEC=LST.dmstodec(-36,13,54.3)

print "The source position is RA =",RA," DEC =",DEC
print "LST is ",LST.getLST(LAT,LON,JD) ,"or",LST.dectodms(LST.getLST(LAT,LON,JD))
print "HA is", LST.getHA(LAT,LON,JD,RA)
print "AZ",LST.getAzEL(RA,DEC,JD,LAT,LON)[0],LST.getAzEL(RA,DEC,JD,LAT,LON)[0]+360.
print "EL",LST.getAzEL(RA,DEC,JD,LAT,LON)[1]

ELList=[]
UTCList=[]
#print (JD,np.floor(JD)-0.5)
for i in JDList:
    ELList.append(LST.getAzEL(RA,DEC,i,LAT,LON)[1])
    UTCList.append((i-np.floor(JD)-0.5)*24)
    #print (i, (i-np.floor(JD)-0.5)*24)
#print ELList
fig, ax = plt.subplots()
ax.plot(UTCList, ELList,c='green', linewidth=1,label='stat')
ax.set_xlim(-12-tz,12-tz)
ax.axvline(x=-12-tz)
ax.axvline(x=12-tz)
ax.set_xticks([-tz-12,-tz-9,-tz-6,-tz-3,-tz,-tz+3,-tz+6,-tz+9,-tz+12])

#ax.set_ylim(0,90)
ax.axhline(y=0)
#ax.set_xlim(-12,12)
ax.set_xlabel('UTC Hours')
ax.set_ylabel('Altitude')
ax.grid('on', which='major', axis='x')
ax.grid('on', which='major', axis='y')


ax2 = ax.twiny()
ax2.set_xlabel("Local Hours")
#ax2.set_xlim(-12,12)
ax2.set_xticks([-tz-12,-tz-9,-tz-6,-tz-3,-tz, -tz+3, -tz+6,-tz+9,-tz+12])
ax2.set_xticklabels(['12','15','18','21','24/0','3','6','9','12'])

plt.show()
