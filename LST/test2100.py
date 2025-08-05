import LST as LST
import numpy as np

def julday(year,month,day, hour=0, minute=0, second=0):
    """
    Julian date from month, day, and year.
    Adapted from "Numerical Recipes in C', 2nd edition, pp. 11
    Parameters
    ----------
    month : numpy.ndarray or int32
        Month.
    day : numpy.ndarray or int32
        Day.
    year : numpy.ndarray or int32
        Year.
    hour : numpy.ndarray or int32, optional
        Hour.
    minute : numpy.ndarray or int32, optional
        Minute.
    second : numpy.ndarray or int32, optional
        Second.
    Returns
    -------
    jd : numpy.ndarray or float64
        Julian day.
    """
    month = np.array(month)
    day = np.array(day)

    in_jan_feb = month <= 2
    jy = year - in_jan_feb
    jm = month + 1 + in_jan_feb * 12

    jd = np.int32(np.floor(365.25 * jy) +
                  np.floor(30.6001 * jm) + (day + 1720995.0))
    ja = np.int32(0.01 * jy)
    jd += 2 - ja + np.int32(0.25 * ja)

    jd = jd + hour / 24.0 - 0.5 + minute / 1440.0 + second / 86400.0

    return jd


def leapYear(year):
    if year%4 ==  0:
        if year%100 == 0:
            if year%400 == 0:
                leapyear=1
                #print(f'{year} is leapyear')
            else:
                leapyear=0
                #print(f'{year} is general')
        else:
             leapyear=1
          #print(f'{year} is leapyear')
    else:
        leapyear=0
        #print(f'{year} is general')
    return leapyear


smon=[4,5,9,11]
if 8 in [4,5,9,11]:
    print("Small Month")

#for i in range (1,200,1):
#    print (i, i%60)

#for i in range (2000,3000,1):
   #print(i,leapYear(i))

#2488128.50000 2100,3,1,0,0,0
print('1600,Feb 28, March 1')
print(LST.CaltoJD(1600,2,28,0,0,0),LST.JD_O(1600,2,28,0,0,0),julday(1600,2,28))
print(LST.CaltoJD(1600,3,1,0,0,0),LST.JD_O(1600,3,1,0,0,0),julday(1600,3,1))

print('1800')
print(LST.CaltoJD(1800,2,28,0,0,0),LST.JD_O(1800,2,28,0,0,0),julday(1800,2,28))
print(LST.CaltoJD(1800,3,1,0,0,0),LST.JD_O(1800,3,1,0,0,0),julday(1800,3,1))

print('1983')
print(LST.CaltoJD(1983,2,28,0,0,0),LST.JD_O(1983,2,28,0,0,0),julday(1983,2,28))
print(LST.CaltoJD(1983,3,1,0,0,0),LST.JD_O(1983,3,1,0,0,0),julday(1983,3,1))

print('2000, Feb 28, Feb 29(exist)')
print(LST.CaltoJD(2000,2,28,0,0,0),LST.JD_O(2000,2,28,0,0,0),julday(2000,2,28))
print(LST.CaltoJD(2000,2,29,0,0,0),LST.JD_O(2000,2,29,0,0,0),julday(2000,2,29))

print('2100, Feb 28, Feb 29(no exit), March 1, April 1.')
print(LST.CaltoJD(2100,2,28,0,0,0),LST.JD_O(2100,2,28,0,0,0),julday(2100,2,28))
print(LST.CaltoJD(2100,2,29,0,0,0),LST.JD_O(2100,2,29,0,0,0),julday(2100,2,29))
print(LST.CaltoJD(2100,3,1,0,0,0),LST.JD_O(2100,3,1,0,0,0),julday(2100,3,1))
print(LST.CaltoJD(2100,4,1,0,0,0),LST.JD_O(2100,4,1,0,0,0),julday(2100,4,1))
#print(LST.CaltoJD2(2100,2,29,0,0,0),julday(2100,2,29))
