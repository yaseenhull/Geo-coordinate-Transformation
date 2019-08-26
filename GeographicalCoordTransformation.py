# -*- coding: utf-8 -*-
"""
Created on Fri Sep 02 12:02:02 2016

@author: Yaseen Hull

Extra-terrestrial coordinate transformations (Geographical coordinates)
"""

import math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#print ax.azim
#ax.view_init(azim=60)

f = open("DATA.txt","r")
data = f.read() 
spl = data.splitlines()
list1 =[]
list2 =[]
list3 =[]
X=[]
Y=[]
Z=[]
f.close()

f2 = open("DATA3.txt","w")
for i in range(len(spl)):
    if spl[i] == 'TWO LINE MEAN ELEMENT SET':
        list1.append(spl[i+3])
        list2.append(spl[i+4])
#f2.write('sat'+'\t'+'EpochYear'+'\t'+'EDay'+'\t'+'EHour'+'\t'+'EMin'+'\t'+'ESec'+'\t'+'Inclination'+'\t'+'RightAscension'+'\t'+'Eccentricity'+'\t'+'Perigee'+'  \t'+'MeanAnomoly'+'\t'+'MeanMotion'+'\t'+'RevsNo'+' '+'\t'+'\t'+'RadPs'+'\t'+'\t'+'\t'+'TrueAnomoly'+'\n'+'\n')



for i in range(len(list1)):
    
    position1 = list1.pop(0)
    
    EpochYear = float(position1[18:20]) #correction to tut1a
    EpochDay = float(position1[20:32]) #correction to tut1a  
    EDay = int(EpochDay)
    EHour = int((EpochDay - EDay)*24)
    EMin = int((((EpochDay - EDay)*24 -EHour))*60)
    ESec = int((((((EpochDay - EDay)*24 -EHour))*60) - EMin)*60)
    
    position2 = list2.pop(0)
    
    Inclination = math.radians(float(position2[9:16]))
    RightAscension = math.radians(float(position2[17:26]))
    Eccentricity = float(position2[27:33])*(10**-7)
    Perigee = math.radians(float(position2[34:42]))
    MeanAnomoly = float(position2[43:51])
    MeanMotion = float(position2[52:63])    
    RevsNo = float(position2[64:69])
    
    pie = math.pi
  

    RadPs = (MeanMotion*(2*math.pi))/(86400)
    T = (2*pie)/RadPs
    M = math.radians(MeanAnomoly)
    E = M
    
    def Efunction(X):
        global E
        E = M +e*math.sin(X)
    
        return E;
        
    e = Eccentricity
    iteration = 5

    while iteration > 0:
        iteration -=1
        EccentricA = Efunction(E)
    
    #print EccentricA
    Ft = (((1-e**2)**0.5)*math.sin(EccentricA))
    Fb = (math.cos(EccentricA)-e)
    TrueAnomoly = math.atan(Ft/Fb)
    #print TrueAnomoly
    
    
    if Ft >0 and Fb<0:
        TrueAnomoly = TrueAnomoly + math.pi
    elif Ft<0 and Fb<0:
        TrueAnomoly = TrueAnomoly + math.pi
    elif Ft <0 and Fb>0:
        TrueAnomoly = TrueAnomoly+2*(math.pi)
    else:
        TrueAnomoly= TrueAnomoly
    #print TrueAnomoly
    G = 6.674*math.pow(10,-11) #gravitational force
    M = 5.972*math.pow(10,24) #mass of Earth
    a = (((T**2.)*G*M)/(4*(pie**2)))**(1/3.0) #recalculated a 
    r = (a*(1-(e**2))/(1+(e*(math.cos(TrueAnomoly)))))
    b = math.sqrt((a**2)-(a**2)*(e**2))#recalculated b
   
        
    x = r*(math.cos(TrueAnomoly))
    y = r*(math.sin(TrueAnomoly))
    z = 0    
    #print(x,y,z)
    
    xRp = (x*(math.cos(-1*Perigee))) + (y*(math.sin(-1*Perigee))) #rotation about z-axis , angle of perigee
    yRp = -1*x*(math.sin(-1*Perigee)) + (y*math.cos(-1*Perigee))
    zRp = z    
     
    xRi = xRp
    yRi = zRp*(math.sin(-1*Inclination)) + (yRp*math.cos(-1*Inclination)) #rotation about x-axis, angle of inclination 
    zRi = zRp*(math.cos(-1*Inclination)) - (yRp*math.sin(-1*Inclination))    
    
    xRa = (xRi*(math.cos(-1*RightAscension))) + (yRi*(math.sin(-1*RightAscension))) #rotation about z-axis, angle of rightascension
    yRa = -1*xRi*(math.sin(-1*RightAscension)) + (yRi*math.cos(-1*RightAscension))
    zRa = zRi 
    
    f2.write('sat'+str([i+1])+'\t'+str(xRa)+'\t'+str(yRa)+'\t'+str(zRa)+'\t'+str(a)+'\t'+str(b)+'\t'+str(e)+'\n')
    
    X.append(xRa)
    Y.append(yRa)
    Z.append(zRa) 
    #print (round(xRa,5),'\t',round(yRa,5),'\t',round(zRa,5))
    
   
for i in range(len(X)): #plot each point + it's index as text above
    ax.scatter(X[i],Y[i],Z[i], color='b', marker = 'o') 
    ax.text(X[i],Y[i],Z[i],  '%s' % (str(i+1)), size=10, zorder=1, color='k')
    
    
    #f2.write("Satellite coordinates in RA system"+'\n'+'\n'+'\t'+"Xra"+'\t'+"Yra"+'\t'+"Zra"+'\n')
       
    
ax.set_xlabel('x axis') 
ax.set_ylabel('y axis')
ax.set_zlabel('z axis')
    
plt.show()

    #print(xRa,yRa,zRa)
 
    
    
    

    
