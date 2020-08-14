

import numpy as np



def setup(xend,yend,zend):
	setupv=[]
	for j in range(0,xend+1):
		for i in range(0,yend+1):
			for k in range(0,zend+1):
				setupv.append((i,j,k))
	return setupv



def distancias(coord,lampx1,lampy1,lampz1,p2,x2,y2,z2):
    distan=[]
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
        distan.append(d)
    return distan

def distancia_axis(coord,lampx1,lampy1,lampz1,p2,x2,y2,z2,lampx2,lampy2,lampz2):
    distanaxis=[]
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
        distanaxis.append(d)
    return distanaxis



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
	intendirect=[]
	for i in range(len(distaxis)):
		if distaxis[i]<long_lamp:
			tempsum=intensidad(IS[i],long_lamp,radio,dist[i],distaxis[i])
		else:
			db=distaxis[i]-long_lamp
			tempsum=intensBey(IS[i],long_lamp, radio,dist[i],db)
		intendirect.append(tempsum)
	return intendirect

def promedio(DirectField):
	total=0
	for i in DirectField:
		total=total+i
		prom=total/len(DirectField)
	return prom

def IS_calc(dist,radio,intensidad_sup):
	isaura=[]
	for i in dist:
		b=i
		if (i<=radio):
			b=radio+0.0001
		isaura.append(intensidad_sup*(100/b)**2)
	return isaura


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
	
	coord=setup(xend,yend,zend)                           #crea las coordenadas del sistema
	dist=distancias(lampx1,lampy1,lampz1,p2,x2,y2,z2)                      #calcula las distancias al eje para cada coordenada
#Calculamos una Intensidad a cada superficie
	IS=IS_calc(dist,radio,intensidad_sup)
	distaxis=distancia_axis(lampx1,lampy1,lampz1)    #calcula la distancia en el eje para cada coordenada
	DirectField=intensidad_directa(long_lamp,radio,IS,dist,distaxis)              #Calcula el campo de intensidades directa para cada coordenada
	print('Promedio de intensidad: '+str(round(promedio(DirectField))))

#Para poder mostrar en unidades relativas, normalizamos el vector DirectField
	DirectField1=np.divide(100*DirectField,max(DirectField))