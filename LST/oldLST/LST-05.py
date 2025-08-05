#!/usr/bin/python

import datetime
import numpy as np
import matplotlib.pyplot as plt
import LST



class JD():
    def __init__(self,year,month,day,hour,mins,sec):
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        self.hour = int (hour)
        self.mins = int (mins)
        self.sec = float (sec)
        self.JD=LST.CaltoJD(year,month,day,hour,mins,sec)
        print (year,month,day,hour,mins,sec,'JD=',self.JD)
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


#JD=LST.CaltoJD(now="now")
print "JD now is ",LST.CaltoJD(now="now")
time1=JD(2022,6,25,0,0,0)
print "Cal time",time1.year,time1.month,time1.day,"JD =",time1.JD
JDList=np.linspace(time1.JD-1,time1.JD+1,500)
#print JDList

#The Position of Nobeyama
#LAT=LST.dmstodec(35,56,30,"N")
#LON=LST.dmstodec(138,28,33,"E")
#timezone=+9

#The Location of Honolulu
LAT=LST.dmstodec(19,49,27)
LON=LST.dmstodec(155,28,41,"W")
timezone=-10

#Loation  of Lulin
#LAT=LST.dmstodec(23,28,9,"N")
#LON=LST.dmstodec(120,52,22,"E")
#timezone=+8

tz=timezone

print "The observator position is LAT=",LAT,"LON=",LON

so_list=[["L1287"  ,00,36,45.6500,+63,28,57.9,"red"],
         ["3c84"   ,03,19,48.1601,+41,30,42.103,"green"],
         ["3c459"  ,23,16,35.1925,+04,5,18.2929,"blue"],
         ["3c454.3",22,53,57.7480,+16,8,53.5630,"yellow"]]


n=0
print (so_list)
print (so_list[n],so_list[n][0])
sourcename=so_list[n][0]
#3c84    0319+415        03:19:48.1601   +41:30:42.103
RA=LST.dmstodec(so_list[n][1],so_list[n][2],so_list[n][3])
DEC=LST.dmstodec(so_list[n][4],so_list[n][5],so_list[n][6])


print "The", sourcename, "position is RA =",RA," DEC =",DEC
print "LST is ",LST.getLST(LAT,LON,time1.JD) ,"or",LST.dectodms(LST.getLST(LAT,LON,time1.JD))
print "HA is", LST.getHA(LAT,LON,time1.JD,RA)
print "AZ",LST.getAzEL(RA,DEC,time1.JD,LAT,LON)[0],LST.getAzEL(RA,DEC,time1.JD,LAT,LON)[0]+360.
print "EL",LST.getAzEL(RA,DEC,time1.JD,LAT,LON)[1]

fig, ax = plt.subplots()


for n in range(len(so_list)):
    #print(n)
    RA=LST.dmstodec(so_list[n][1],so_list[n][2],so_list[n][3])
    DEC=LST.dmstodec(so_list[n][4],so_list[n][5],so_list[n][6])
    ELList=[]
    UTCList=[]
#print (JD,np.floor(JD)-0.5)
    for i in JDList:
        ELList.append(LST.getAzEL(RA,DEC,i,LAT,LON)[1])
        UTCList.append((i-np.floor(time1.JD)-0.5)*24)
    ax.plot(UTCList, ELList,c=so_list[n][7], linewidth=1,label=so_list[n][0])
ax.legend(loc='lower right')
ax.set_xlim(-12-tz,12-tz)
ax.axvline(x=-12-tz)
ax.axvline(x=12-tz)
ax.set_xticks([-tz-12,-tz-9,-tz-6,-tz-3,-tz,-tz+3,-tz+6,-tz+9,-tz+12])

ax.set_ylim(0,90)
ax.axhline(y=0)
#ax.set_xlim(-12,12)
ax.set_xlabel('UTC Hours')
ax.set_ylabel('Altitude')
ax.grid('on', which='major', axis='x')
ax.grid('on', which='major', axis='y')


ax2 = ax.twiny()
ax2.set_xlabel('Local Hours')
#ax2.set_xlim(-12,12)
ax2.set_xticks([-tz-12,-tz-9,-tz-6,-tz-3,-tz, -tz+3, -tz+6,-tz+9,-tz+12])
ax2.set_xticklabels(['12','15','18','21','24/0','3','6','9','12'])

plt.show()
print "Remember: Time change!!!!"
