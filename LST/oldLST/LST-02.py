#!/usr/bin/python

import datetime
import numpy as np


def dmstodec(dd,mm,ss,Dir="N"):
   dec=np.abs(dd)+(np.abs(mm)/60.)+(np.abs(ss)/3600.)
   if Dir == "S" or Dir == "W":
       sign=-1.0
   else:
       if dd<0 or mm<0 or ss<0:
           sign=-1.
       else:
          sign=1
   return dec*sign

def dectodms(dec):
   mm = (dec - int(dec))*60          #convert fraction hours to minutes
   ss = (mm - int(mm))*60      #convert fractional minutes to seconds
   hh = int(dec)
   mm = int(mm)
   ss = int(ss)
   return [hh,mm,ss]

def CaltoJD(year=0,month=0,day=0,hour=0,minute=0,second=0,now=""):
    DUT1=-0.153 #2019,Sep,30
    if now == "now":
       utcn=datetime.datetime.utcnow()
       year=utcn.year
       month=utcn.month
       day=utcn.day
       hour=utcn.hour
       minute=utcn.minute
       second=utcn.second+DUT1 
    ut=float(hour)+float(minute)/60.+float(second)/3600.
    JD = (367*year) - int((7*(year+int((month+9)/12)))/4)+int((275*month)/9)+day + 1721013.5 + (ut/24.0)
    return JD


def getLST2(LAT,LON,JD):
    GMST = 18.697374558 + 24.06570982441908*(JD - 2451545)
    GMST = GMST % 24
    LON=LON/15.0   # degree to hours
    LST=GMST+LON
    if LST < 0:
        LST= LST+24
    return LST

def getLST(LAT,LON,JD):
    JD0=np.floor(JD)
    uth=(JD-JD0)*86400
    T=(JD-2451545.)/36525.
    T0=(JD0-2451545.)/36525.
    GMST=24110.54841+8640184.812866*T0+1.00273*uth+0.093104*T*T-0.0000062*T*T*T
    GMST=(GMST/3600.+12) % 24
    LON=LON/15.0   # degree to hours
    LST=GMST+LON
    if LST < 0:
        LST= LST+24
    return LST

def getHA(LAT,LON,JD,RA):
    LST=getLST(LAT,LON,JD)
    HA=(LST-RA+24.0) % 24
    return HA

def getAzEL(RA,DEC,JD,LAT,LON):
    HA=getHA(LAT,LON,JD,RA)*360./24.
    sinEL=np.sin(DEC*np.pi/180.)*np.sin(LAT*np.pi/180.)+np.cos(DEC*np.pi/180.)*np.cos(LAT*np.pi/180.)*np.cos(HA*np.pi/180.)
    EL=np.arcsin(sinEL)
    cosaz=(np.sin(DEC*np.pi/180.)-(np.sin(EL)*np.sin(LAT*np.pi/180.)))/np.cos(EL)/np.cos(LAT*np.pi/180.0)
    Az=np.arccos(cosaz)
    return Az*-180./np.pi,EL*180/np.pi



print "Now JD",CaltoJD(now="now")
JD=CaltoJD(2019,1,18,20,0,18)
print  "JD in .",JD

#The Longitude of Honolulu
#LAT=dmstodec(19,49,27)
#LON=dmstodec(155,28,41,"W")
LAT=dmstodec(30,0,0,)
LON=dmstodec(130,0,0,"W")

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
RA=dmstodec(17,15,10.38)
DEC=dmstodec(26,51,51.9)
print "RA =",RA," DEC =",DEC

print "LST in Obser",getLST(LAT,LON,JD) ,"or",dectodms(getLST(LAT,LON,JD))

print "HA is", getHA(LAT,LON,JD,RA)

print "AZ",getAzEL(RA,DEC,JD,LAT,LON)[0],getAzEL(RA,DEC,JD,LAT,LON)[0]+360.
print "EL",getAzEL(RA,DEC,JD,LAT,LON)[1]
