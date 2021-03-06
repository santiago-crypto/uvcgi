import uvc as uv
import numpy as np
import math

xend=30
yend=30
zend=85

radio=1.21
long_lamp=81.5
intensidad_sup=117


lampx1=0
lampy1=0
lampz1=0

lampx2=0
lampy2=0
lampz2=81

x2=lampx2-lampx1
y2=lampy2-lampy1
z2=lampz2-lampz1
p2=x2*x2+y2*y2+z2*z2




def tiempito(valores,coord):
	"""

   Analisis de los tiempos necesarios para matar al virus
 covid19 para el valor promedio mediante un modelo lineal, 
 para una esterilizacion del 90%.  t_teo

 	En segunda instancia se calcula el tiempo que llevaria 
 a la intensidad promedio del sistema el valor recomendado por
 el cdc 1 J/cm2 t_exp

"""


	target=99.99

	s=1-target/100
#constante específica del virus m2/J
#k = 0.37700/100  #factor correccion para llevarlo a cm2/microJ sarscov1
#k=0.0008528 #promedio autores 2020
	kv=0.0005522 #Inagaki 2020 
#La intensidad se encuentra en microW/cm2
#dimensionalmente el tiempo esta en segundos

	t=math.log(s)/(-1*kv*uv.promedio(valores))
	print('El promedio de intensidades: '+str(round(uv.promedio(valores))))
	print('Computo de tiempo optimo para el promedio de Intensidades')
	print('tiempo para D99.99= '+str(round(t,3))+' segundos')
#el valor experimental 1 J/cm2
	exp=3*(10**6) #factor de corrección para llevarlo a microJ/cm2
#La intensidad se encuentra en microW/cm2

	t_e=exp/uv.promedio(valores)

	print('tiempo para 1 J/cm2= '+str(round(t_e,3))+' segundos')


#calculo de los tiempos teorico y experimental, para un plano especifico.
#considerando el plano de interes en Y=2

	Z1=[]

	for n in range(len(coord)):
		i,j,k = coord[n]
		if (j==1):
			if (k==round((lampz2-lampz1)/2)):
				Z1.append(valores[n])

#La menor intensidad a lo largo del eje perpendicular
#a lo largo del centro de la lampara se la considerara 
#como el valor a optimizar en tiempo
	Imin=min(Z1)
	print('La menor intensidad a la altura de la bandeja es: '+str(round(Imin,2))+'microW/cm2')

	print('Analisis de tiempos optimos en la bandeja')
	tmin=math.log(s)/(-1*kv*Imin)
	print('tiempo para D99.99= '+str(round(tmin,5))+' segundos')

	t_emin=exp/Imin
	print('tiempo para 1 J/cm2= '+str(round(t_emin,3))+' segundos')
	return tmin, t_emin



	

def Matriz3d(xend,yend,zend,lampx1,lampy1,lampz1,p2,x2,y2,z2,lampx2,lampy2,lampz2):
	coord=uv.setup(xend,yend,zend)
	dist=uv.distancias(coord,lampx1,lampy1,lampz1,p2,x2,y2,z2)                      #calcula las distancias al eje para cada coordenada
#Calculamos una Intensidad a cada superficie
	IS=uv.IS_calc(dist,radio,intensidad_sup)
	distaxis=uv.distancia_axis(coord,lampx1,lampy1,lampz1,p2,x2,y2,z2,lampx2,lampy2,lampz2)    #calcula la distancia en el eje para cada coordenada
	DirectField=uv.intensidad_directa(long_lamp,radio,IS,dist,distaxis)              #Calcula el campo de intensidades directa para cada coordenada
	return DirectField, coord
	



if __name__=='__main__':
	
	aaa,coorde=Matriz3d(xend,yend,zend,lampx1,lampy1,lampz1,p2,x2,y2,z2,lampx2,lampy2,lampz2)
	tiempito(aaa,coorde)
