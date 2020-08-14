import uvc as uv
import uvcml 
import math
#parametros de la lampara
radio=1.21
long_lamp=81.5
intensidad_sup=117

#parametros de la caja
xend=30
yend=30
zend=85

#Posición de la lampara
lampx1=0
lampy1=27
lampz1=0

lampx2=0
lampy2=27
lampz2=81


x2=lampx2-lampx1
y2=lampy2-lampy1
z2=lampz2-lampz1
p2=x2*x2+y2*y2+z2*z2


data=[]

def tiemp(valores,coord):
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
	print('El promedio de intensidades: '+str(round(uv.promedio(valores))))
	t=math.log(s)/(-1*kv*uv.promedio(valores))

#el valor experimental 1 J/cm2
	exp=3*(10**6) #factor de corrección para llevarlo a microJ/cm2
#La intensidad se encuentra en microW/cm2

	t_e=exp/uv.promedio(valores)


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

	tmin=math.log(s)/(-1*kv*Imin)
	t_emin=exp/Imin

	return tmin, t_emin




for inc in range(3):
	aaa,coorde= uvcml.Matriz3d(xend,yend,zend,lampx1+inc,lampy1,lampz1,p2,x2,y2,z2,lampx2+inc,lampy2,lampz2)
	t1,t2=tiemp(aaa,coorde)
	data.append([inc,uv.promedio(aaa),t1,t2])
	print(inc)

import csv 
with open('sawers.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerows(data)

print(data)
