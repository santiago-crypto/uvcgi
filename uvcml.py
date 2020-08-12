import uvc
from uvc import coord,IS,dist,distaxis,DirectField
import math
xend=30
yend=30
zend=100

radio=1.21
long_lamp=81.3
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


uvc.setup(xend,yend,zend)
uvc.distancias(lampx1,lampy1,lampz1,p2,x2,y2,z2)                      #calcula las distancias al eje para cada coordenada
#Calculamos una Intensidad a cada superficie
uvc.IS_calc(dist,radio,intensidad_sup)
uvc.distancia_axis(lampx1,lampy1,lampz1,p2,x2,y2,z2,lampx2,lampy2,lampz2)                  #calcula la distancia en el eje para cada coordenada
uvc.intensidad_directa(long_lamp,radio,IS,dist,distaxis)              #Calcula el campo de intensidades directa para cada coordenada
print('Promedio de intensidad: '+str(round(uvc.promedio())))

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
#k = 0.37700/100  #factor correccion para llevarlo a cm2/microJ
#k=0.0008528 #promedio autores 2020
k=0.0005522 #Inagaki 2020
#La intensidad se encuentra en microW/cm2
#dimensionalmente el tiempo esta en segundos

t=math.log(s)/(-1*k*uvc.promedio())
print('tiempo para D99.99= '+str(round(t,3))+' segundos')


#el valor experimental 1 J/cm2
exp=1.5*(10**6) #factor de corrección para llevarlo a microJ/cm2
#La intensidad se encuentra en microW/cm2
t_e=exp/uvc.promedio()

print('tiempo para 1 J/cm2= '+str(round(t_e,3))+' segundos')

