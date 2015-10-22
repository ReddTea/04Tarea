# coding: utf-8
#!/usr/bin/env python
#importamos librerias a usar
from planeta import Planeta
import numpy as np
import matplotlib.pyplot as plt
#definimos un par de parametros que serán importantes en la resolución
# de la tarea
alpha2= 10**(-2.067)
CI= [10,0,0,0.3]

def orbitar(CI,solucion, prt=True):
    '''
    Esta función  es cool, porque le entregas las condiciones iniciales (CI)
    en forma de x0,y0,vx0,vy0, además de un string con el tipo de solución
    que quieres, como 'euler', 'rk4' o 'verlet' y nos devuelve las coordenadas
    x,y y la energia total del planeta. Además de un ploteo de la órbita, apropi-
    adamente labelado y un ploteo de la energía vs el tiempo.
    La ultima parte es para que plotee, el valor default es que
    plotee (true or false).
    Ejemplo de uso:
        orbitar([10,0,0,0.1],'verlet')
        x=[0,0.1,...]
        y=[0,0.3,...]
        energia=[7,8,...]
    '''
    if solucion=='euler':
        n= 2500 #grande y dsps se arregla
    if solucion=='rk4':
        n= 5000 #grande y dsps se arregla
    if solucion=='verlet':
        n=800
    Aiur= Planeta(CI) #se crea el planeta
    if solucion=='verlet_reloaded': #caso especial para la ultima parte
        n=6000
        Aiur= Planeta(CI,alpha=alpha2) #si es el verlet bkn se parcha
    dt= 1 #error si es muy chico
    tmax=n*dt
    x=[] #listas vacias a llenar
    y=[]
    pylon=[] #energia

    x= np.append(x,CI[0]) #llenamos con el primer termino
    y= np.append(y,CI[1])
    pylon= np.append(pylon,Aiur.energia_total())

    for i in range(tmax):   #aca se hace la iteracion del paso
        if solucion=='euler':
            Aiur.avanza_euler(dt)
        if solucion=='rk4':
            Aiur.avanza_rk4(dt)
        if solucion=='verlet' or solucion=='verlet_reloaded':
            Aiur.avanza_verlet(dt)
        xn,yn,vxn,vyn=Aiur.y_now
        x= np.append(x,xn)
        y= np.append(y,yn)
        pylon= np.append(pylon,Aiur.energia_total())
        times=np.linspace(0,tmax,tmax+1)
    if prt==True:
        fig1=plt.figure(1)  #aca se plotea, muy standar
        fig1.clf()
        if solucion=='euler':
            plt.plot(x,y,'r',label= 'Trayectoria metodo Euler')
            plt.title('Trayectoria metodo Euler')
        if solucion=='rk4':
            plt.plot(x,y,'r',label= 'Trayectoria metodo RK4')
            plt.title('Trayectoria metodo RK4')
        if solucion=='verlet' or solucion=='verlet_reloaded':
            plt.plot(x,y,'r',label= 'Trayectoria metodo Verlet')
            plt.title('Trayectoria metodo Verlet')

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.savefig('verlet_rld.png')
        plt.draw()
        plt.show()

        fig2=plt.figure(2)
        fig2.clf()
        plt.plot(times, pylon,'g')
        plt.xlabel('Tiempo')
        plt.ylabel('Energia')
        plt.title('Tiempo vs Energia')
        plt.savefig('verlet_rld_energia.png')
        plt.draw()
        plt.show()
    return x,y,pylon
