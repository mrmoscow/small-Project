#!/usr/bin/python

import datetime
import numpy as np

now=datetime.datetime.now()
print "now:", now
print "hour:",now.hour,"minutes",now.minute,"second",now.second
print "Year",now.year,"Mon",now.month,"date",now.day

print"================"

def dmstodec(dd,mm,ss,Dir="N"):
   dec=dd+(mm/60.)+(ss/3600.)
   if Dir == "S" or Dir == "W":
       return -1.0*dec
   else:
       return dec
def dectodms(dec):
   mm = (dec - int(dec))*60          #convert fraction hours to minutes
   ss = (mm - int(mm))*60      #convert fractional minutes to seconds
   hh = int(dec)
   mm = int(mm)
   ss = int(ss)
   return [hh,mm,ss]

def CaltoJD(year=0,month=0,day=0,hour=0,minute=0,second=0,now=""):
    DUT1=-0.1514 #2019,Sep,20
    if now == "now":
       utcn=datetime.datetime.utcnow()
       year=utcn.year
       month=utcn.month
       day=utcn.day
       hour=utcn.hour
       minute=utcn.minute
       second=utcn.second+DUT1 
    ut=float(hour)+float(minute)/60.+float(second)/3600.
    JD = (367*year) - int((7*(year+int((month+9)/12)))/4)+int((275*month)/9)+day + 1721013.5 + (ut/24)
    return JD

def getLST(LAT,LON,JD):
    GMST = 18.697374558 + 24.06570982441908*(JD - 2451545)
    GMST = GMST % 24
    LON=LON/15.0
    LST=GMST+Long
    if LST < 0:
	LST= LST+24
    return LST

def getHA(LAT,LON,JD,RA):
    LAT=getLST(LAT,LON,JD)
    HA=(LST-RA+360.0) % 360
    return HA

def getAzEL(RA,Dec,JD,LAT,LON):
    HA=getHA(LAT,LON,JD,RA)*360./24.
    sinEL=np.sin(DEC*np.pi/180.)*np.sin(LAT*np.pi/180.)+np.cos(DEC*np.pi/180.)*np.cos(LAT*np.pi/180.)*np.cos(HA*np.pi/180.)
    EL=np.arcsin(sinEL)
    cosaz=(np.sin(DEC*np.pi/180.)-(np.sin(EL)*np.sin(LAT*np.pi/180.)))/np.cos(EL)/np.cos(LAT*np.pi/180.0)
    Az=np.arccos(cosaz)
    return Az*-180./np.pi,EL*180/np.pi

#print dmstodec(155,28,40.8,"W")
#print dectodms(23.8)

utcnow=datetime.datetime.utcnow()
print "utcnow:",utcnow
ut=utcnow.hour+float(utcnow.minute)/60.0+float(utcnow.second)/3600.0
print"UT",ut,dectodms(ut)
JD = (367*utcnow.year) - int((7*(utcnow.year+int((utcnow.month+9)/12)))/4)+int((275*utcnow.month)/9) + utcnow.day + 1721013.5 + (ut/24)
print "JD", JD
print "New JD",CaltoJD(now="now")
print  "oldJD",CaltoJD(utcnow.year,utcnow.month,utcnow.day,utcnow.hour,utcnow.minute,utcnow.second)

#The Longitude of Honolulu
LAT=19.8243
Long=-(155+(28.0/60.0)+(40.8/3600.0))
#print(Long)
RA=dmstodec(00,45,30.2)
DEC=dmstodec(41,55,47.4)
print "RA =",RA," DEC =",DEC

'''
LST = 100.46 + 0.985647 * d + long + 15*UT
d    is the days from J2000, including the fraction of a day
 J2000 is 2451545
UT   is the universal time in decimal hours
long is your longitude in decimal degrees, East positive.
'''

GMST = 18.697374558 + 24.06570982441908*(JD - 2451545)
GMST = GMST % 24
Long=Long/15
LST=GMST+Long
if LST < 0:
     LST= LST+24
HA=(LST-RA+360.0) % 360
LSTmm = (LST - int(LST))*60          #convert fraction hours to minutes
LSTss = (LSTmm - int(LSTmm))*60      #convert fractional minutes to seconds
LSThh = int(LST)
LSTmm = int(LSTmm)
LSTss = int(LSTss)
print "LST in Hawaii", LST,"or",LSThh,":",LSTmm,":",LSTss
print "LST in Hawaii",LST, "or",dectodms(LST)
print "LsT in Hawaii",getLST(LAT,Long,JD) ,"or",dectodms(getLST(LAT,Long,JD))
print "HA is", HA,getHA(LAT,Long,JD,RA)


'''
Local Mean Sidereal Time

Hour Angle

The hour angle (HA) is the angle between an observer's meridian projected onto the celestial sphere and the right ascension of a celestial body. It is used in coordinate conversion.

HA = LMST - RA 
Conversion of HA and DEC into ALT and AZ

Using the RA, DEC and HA for the object, and the latitude (LAT) of the observing site, the following formulas give the ALT and AZ of the object at the time and longitude that was used to calculate HA.

'''
HA=HA*360/24.0
x = np.cos(HA * (np.pi / 180.0)) * np.cos(DEC* (np.pi / 180.0))
y = np.sin(HA * (np.pi / 180.0)) * np.cos(DEC* (np.pi / 180.0))
z = np.sin(DEC * (np.pi / 180.0))

xhor= x*np.cos((90.-LAT)*(np.pi/180.0))-z*np.sin((90.-LAT)*(np.pi/180.0))
yhor= y
zhor= x*np.sin((90.-LAT)*(np.pi/180.0))+z*np.cos((90.-LAT)*(np.pi/180.0))

az = np.arctan2(yhor, xhor) * (180.0/np.pi)+180.
alt = np.arcsin(zhor) * (180.0/np.pi)

sinalt=np.sin(DEC*np.pi/180.)*np.sin(LAT*np.pi/180.)+np.cos(DEC*np.pi/180.)*np.cos(LAT*np.pi/180.)*np.cos(HA*np.pi/180.)
alt2=np.arcsin(sinalt)
cosaz=(np.sin(DEC*np.pi/180.)-(np.sin(alt2)*np.sin(LAT*np.pi/180.)))/np.cos(alt2)/np.cos(LAT*np.pi/180.0)
az2=np.arccos(cosaz)

print "AZ",az, "or", az-360.,az2*180./np.pi,dectodms(az2*180./np.pi)
print "AZ",getAzEL(RA,DEC,JD,LAT,Long)[0]
print "El",alt,alt2*180./np.pi,dectodms(alt2*180./np.pi)
print "EL",getAzEL(RA,DEC,JD,LAT,Long)[1]
