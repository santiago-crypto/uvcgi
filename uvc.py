#@RadionTech 
# Calculo de rendimiento UVGI 
#----------------------------------------------------------------------------
''' 
Este programa simula el funcionamiento de un sistema de esterilización basado 
en UVC_GI, considerando el método de cálculo de radiación térmica View Factor 
del libro Radiative Heat Transfer by Michael F. Modest
 
'''

import math 
import numpy as np

#Calculo del Campo de intensidades Directos
#tendremos las siguientes variables para cada punto:

#Un vector que almacena las coordenadas i,j,k en una tupla

coord=[]

# x i ancho  50 cm
# y j alto   50 cm
# z k largo 100 cm
#Empieza variando en el orden i,j,k - i,j,k+1 - i,j+1,k - i+1,j,k
# El tamaño total del vector será:
# Python empieza la indexación en 0
#xend+1*yend+1*zend+1

IS=[]
#distancia hacia el eje de la lámpara para cada coord
dist=[]
#distancias a lo largo del axis de la lámpara para cada coord
distaxis=[]
#Vector de intensidades de la Radiación Directa
DirectField=[]



def setup(xend,yend,zend):
#	setupv=[]
	for j in range(0,xend+1):
		for i in range(0,yend+1):
			for k in range(0,zend+1):
				coord.append((i,j,k))
#	return setupv



def distancias(lampx1,lampy1,lampz1,p2,x2,y2,z2):
    for i,j,k in coord:
        x1=i-lampx1
        y1=j-lampy1
        z1=k-lampz1     
        p1=x1*x1+y1*y1+z1*z1
        if (p1*p2>0):
                dotprod= (x1*x2+y1*y2+z1*z2)/(np.sqrt(p1*p2))
                a=np.arccos(dotprod)
                d=abs(np.sin(a))*np.sqrt(p1)
        else: 
            d = 0
        dist.append(d)

def distancia_axis(lampx1,lampy1,lampz1,p2,x2,y2,z2,lampx2,lampy2,lampz2):
    for i,j,k in coord:
        x1=i-lampx1
        y1=j-lampy1
        z1=k-lampz1     
        p1=x1*x1+y1*y1+z1*z1
        if (p1*p2>0):
            dotprod= (x1*x2+y1*y2+z1*z2)/(np.sqrt(p1*p2))
            a=np.arccos(dotprod)
            posit1=abs(np.cos(a))*np.sqrt(p1)
        else: 
            posit1 = 0.000001
        x3=i-lampx2
        y3=j-lampy2
        z3=k-lampz2   
        p3=x3*x3+y3*y3+z3*z3
        p4=x2*x3+y2*y3+z2*z3
        if(p2*p3>0):
            dotprod= p4/(np.sqrt(p3*p2))
            a=np.arccos(dotprod)
            posit2=np.cos(a)*np.sqrt(p3)
        else:
            posit2 = 0.000001
        d=max(posit1,posit2)
        distaxis.append(d)



def VFCylinder(l, r, h):
    # l= distaxis, r=radius, h=dist
    if(h<r):
        h=r+0.000001 #siempre esta afuera del foco
    H=h/r
    L=l/r
    if(L==0):
        L=0.000001
    if(H==1):
        H=H+0.000001
    X=(1+H)*(1+H)+L*L
    Y=(1-H)*(1-H)+L*L
    a=np.arctan(L/np.sqrt(H*H-1))/L
    b=(X-2*H)*np.arctan(np.sqrt((X/Y)*(H-1)/(H+1)))/np.sqrt(X*Y)
    c=np.arctan(np.sqrt((H-1)/(H+1)))
    VF=L*(a+b-c)/np.pi*H 
    return VF


def intensidad(IS,arcl,r,x,l):
    #IS,arcl,r son datos de la lampara
    #x es la distancia al eje     -   dist
    #l es la distancia en el eje  -   distaxis
    VF1=VFCylinder(l,r,x)
    VF2=VFCylinder(arcl-l,r,x)
    VF=VF1+VF2
    intense=IS*VF
    return  intense

def intensBey(IS,arcl,r,x,db):
    VF1=VFCylinder(arcl+db,r,x)
    VF2=VFCylinder(db,r,x)
    VF=VF1-VF2
    intense = np.fabs(VF*IS)
    return intense


def intensidad_directa(long_lamp,radio,IS,dist,distaxis):
    for i in range(len(distaxis)):
        if distaxis[i]<long_lamp:
           tempsum=intensidad(IS[i],long_lamp,radio,dist[i],distaxis[i])
                #entradas: IS, arcl,r,x,h
        else:
            db=distaxis[i]-long_lamp
            tempsum=intensBey(IS[i],long_lamp, radio,dist[i],db)
        DirectField.append(tempsum)

def promedio():
    total=0
    for i in DirectField:
        total=total+i
    prom=total/len(coord)
    return prom

def IS_calc(dist,radio,intensidad_sup):
    for i in dist:
        b=i
        if (i<=radio):
            b=radio+0.0001
        IS.append(intensidad_sup*(100/b)**2)
    



if __name__=='__main__':
#Los valores set de la lámpara indican la posición de la lámpara
	print('Coordenadas del inicio de la lámpara')
	print('eje x: ')
	lampx1=int(input())
	print('eje y: ')
	lampy1=int(input())
	print('eje z: ')
	lampz1=int(input())
	print('coordenadas final de la lampara')
	print('eje x: ')
	lampx2=int(input())
	print('eje y: ')
	lampy2=int(input())
	print('eje z: ')
	lampz2=int(input())
	x2=lampx2-lampx1
	y2=lampy2-lampy1
	z2=lampz2-lampz1
	p2=x2*x2+y2*y2+z2*z2

#radio de la lampara en cm
	print('Radio de la lámpara en cm')
	radio=float(input())
#longitud de la lampara en cm
	print('Longitud de arco de la lámpara en cm')
	long_lamp=float(input())
#Intensidad Superficial en microW/cm2
	print('Rating de la lamp 1 metro en microW/cm2')
	intensidad_sup=int(input())
	print("Ancho en cm 'x'")
	xend = int(input())
	print("Alto en cm 'y'")
	yend = int(input())
	print("Largo en cm 'z'")
	zend = int(input())
	
	setup(xend,yend,zend)                           #crea las coordenadas del sistema
	distancias(lampx1,lampy1,lampz1,p2,x2,y2,z2,lampx2,lampy2,lampz2)                      #calcula las distancias al eje para cada coordenada
#Calculamos una Intensidad a cada superficie
	IS_calc(dist,radio,intensidad_sup)
	distancia_axis(lampx1,lampy1,lampz1)    #calcula la distancia en el eje para cada coordenada
	intensidad_directa(long_lamp,radio,IS,dist,distaxis)              #Calcula el campo de intensidades directa para cada coordenada
	print('Promedio de intensidad: '+str(round(promedio())))

#Para poder mostrar en unidades relativas, normalizamos el vector DirectField
	DirectField1=np.divide(100*DirectField,max(DirectField))