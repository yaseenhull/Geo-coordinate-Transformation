# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 16:11:18 2016

@author: Yaseen Hull

Extra-terrestrial coordinate transformations (Geographical coordinates)
"""
 
import math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

f = open("DATA3.txt","r")
data =f.read()
spl =data.splitlines()
coords = {}
values =[]
X =[]
Y=[]
Z=[]
par ={}
parm ={}
i=0
while i < len(spl): 
    for i in spl:
        values = i.split('\t')
        sat =  values.pop(0)
        values = map(float,values)
        coords[sat]=[round(values.pop(0),3),round(values.pop(0),3),round(values.pop(0),3),values.pop(0), values.pop(0),values.pop(0)]
        val = coords.values()
        key = coords.keys()
        item =coords.items()

f = open("DATA.txt","r")
data = f.read() 
spl = data.splitlines()
list1 =[]
list2 =[]

for i in range(len(spl)):
    if spl[i] == 'TWO LINE MEAN ELEMENT SET':
        list1.append(spl[i+3])
        list2.append(spl[i+4])

f = open("Julian.txt","r")
data = f.read()
spl =data.splitlines()
JulianD = []

for i in range(len(spl)):
    JulianD.append(float(spl[i]))
        
f = open("tut+2b+DATA+XpYp.txt","r")
data = f.read() 
spl = data.splitlines()

xp =[]
yp =[]
corr =[]
sect1 =[]
sect2=[]


i =0
while i !=7:
    sect1.append(spl[58+i:59+i][0])
    i = i+1
    
k = 0
for k in range(len(sect1)):
    
    x = sect1[k]
    corr.append(float(x[49:58]))
    xp.append(float(x[19:26]))
    yp.append(float(x[34:41]))
    k=k+1

j =0
while j !=9:
    sect2.append(spl[86+j:87+j][0])
    j = j+1
    
k = 0
for k in range(len(sect2)):
    
    x = sect2[k]
    corr.append(float(x[54:64]))
    xp.append(float(x[30:37]))
    yp.append(float(x[43:49]))
    k=k+1
    

for i in range(len(JulianD)):
    satNo = "sat"+str([i+1])    
    #correction to tut1a
    JD = JulianD[i]
    
    d = JD - 2451545.0
    T = d/36525
    GMST = 24110.54841 + 8640184.812866*T + 0.093104*(T**2) - 0.0000062*(T**3)
    GAST = GMST + (-0.24) #Equation of Equinoxes
    GDay = int(GAST)
    GHour = ((GAST)/3600)*15
    #print (math.radians(GHour),d,T)
    DDD = int(GHour)
    MMM = int((GHour-DDD)*60)
    SSS = round((((GHour - DDD)*60)-MMM)*60)
      
    items = parm.items()
    position1 = list1.pop(0)
    
    EpochYear = float(position1[18:20]) #correction to tut1a
    EpochDay = float(position1[20:32]) 
 
    for i in range(16):
        if int(EpochDay)==225+i:
            correction = corr[i]
            Xp = xp[i]
            Yp = yp[i]
            ut1 = correction + EpochDay
            
            EDay = int(ut1)
            EHour = int((ut1 - EDay)*24)
            EMin = int((((ut1 - EDay)*24 -EHour))*60)
            ESec = int((((((ut1 - EDay)*24 -EHour))*60) - EMin)*6) 
            
            par[satNo]=[GHour,Xp,Yp]
            update1 = parm.update(par)
            items = parm.items()
            
    #f2.write(satNo+'\t'+str(ut1)+'\t'+str(GMST)+'\t'+str(GAST)+'\t'+str(GHour)+'\n')
    #print JD
for i in range(len(items)):
    for k in range(len(item)):
        if item[k][0] == items[i][0]:
            
            name = item[k][0]
            x = item[k][1][0] 
            y = item[k][1][1]
            z = item[k][1][2]
            a = item[k][1][3]
            b = item[k][1][4]
            e = item[k][1][5]
            
            Gh = math.radians(items[i][1][0])
            xP = (items[i][1][1])/206264.806247
            yP = (items[i][1][2])/206264.806247
            
            #print(name,x,y,z,a,b,Gh,xP,yP)
            
            
            
            Xz = (x*(math.cos(Gh))) + (y*(math.sin(Gh))) #rotation about z-axis , angle of GH
            Yz = -1*x*(math.sin(Gh)) + (y*math.cos(Gh))
            Zz = z 
            
            Xx = Xz
            Yx = Zz*(math.sin(-yP)) + (Yz*math.cos(-yP)) #rotation about x-axis, angle of YP 
            Zx = Zz*(math.cos(-yP)) - (Yz*math.sin(-yP))
            
            Xcts = Xx*(math.cos(-xP))-Yx*(math.sin(-xP))
            Ycts = Yx
            Zcts = Xx*(math.sin(-xP))+Zx*(math.cos(-xP))    
            
            X.append(Xcts)
            Y.append(Ycts)
            Z.append(Zcts) 
            
            longitude = math.atan(Ycts/Xcts)
            
            if Ycts >0 and Xcts<0:
                longitude = longitude + math.pi
            elif Ycts<0 and Xcts<0:
                longitude = longitude + math.pi
            elif Ycts <0 and Xcts>0:
                longitude = longitude+2*(math.pi)
            else:
                longitude= longitude
            
            longitude = math.degrees(longitude)
            
            DD = int(longitude)
            MM = int((longitude-DD)*60)
            SS = round((((longitude - DD)*60)-MM)*60)
            
            #print(name,Xcts,Ycts,Zcts)
            print Zcts
            p = math.sqrt((Xcts**2)+(Ycts**2))
            No = a
            N = No
            ho = math.sqrt((Xcts**2)+(Ycts**2)+(Zcts**2))-math.sqrt(a*b)
            h = ho
    
        def Efunction(x,y):
            
            lat = math.atan((Zcts/p)*((1-((e**2)*x)/(x+y))**-1))
            global N
            N = (a/math.sqrt(1-(e**2)*(math.sin(lat))**2))
            global h
            h = (p/math.cos(lat))-x
            
    
            return N,h;
        
        
        iteration = 20

        while iteration > 0:
            iteration -=1
            (n,H) = Efunction(N,h)
    latitude = math.degrees(math.atan((Zcts/p)*((1-((e**2)*n)/(n+H))**-1)))
    height = H
    
    D = int(latitude)
    M = int((latitude-D)*60)
    S = round((((latitude - D)*60)-M)*60)
    
    #print(name+'\t'+str(D)+'\t'+str(M)+'\t'+str(S)+'\t'+str(DD)+'\t'+str(MM)+'\t'+str(SS)+'\t'+str(height)+'\n')
for i in range(len(X)): #plot each point + it's index as text above
    ax.scatter(X[i],Y[i],Z[i], color='b', marker = 'o') 
    ax.text(X[i],Y[i],Z[i],  '%s' % (str(i+1)), size=10, zorder=1, color='k')
    
    
    
    
ax.set_xlabel('x axis') 
ax.set_ylabel('y axis')
ax.set_zlabel('z axis')
    
plt.show()   
    