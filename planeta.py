#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

class Planeta(object):

    '''
    Es un objeto al cual hay que darle ciertos parametros (condiciones
    iniciales), que tiene metodos de resolucion integrados para su
    ecuacion de movimiento asociada.
    '''
    global G,M,cte
    G=1.0
    M=1.0
    cte=G*M

    def __init__(self, condicion_inicial, alpha=0, mass=1.0):
        '''
        __init__ es un método especial que se usa para inicializar las
        instancias de una clase.

        Ej. de uso:
        mercurio = Planeta([x0, y0, vx0, vy0])
        print(mercurio.alpha)
        0.
        '''
        self.y_now=condicion_inicial
        self.t_now= 0.0
        self.alpha= alpha
        self.mass= mass #mass
    def edm(self):
        '''
        Implementa la ecuación de movimiento, como sistema de ecuaciónes de
        primer orden. Lo hace en la forma de  funcion y entrega un array,
        al cual no le hemos sacado mucho el jugo porque resulta realmente
        confuso.
        '''
        x,y,vx,vy= self.y_now
        fx=lambda x,y: cte*x/((x**2+y**2)**2)*(2*self.alpha-np.sqrt(x**2+y**2))
        fy=lambda x,y: cte*y/((x**2+y**2)**2)*(2*self.alpha-np.sqrt(x**2+y**2))

        return np.array([vx, vy, fx, fy])

    def avanza_euler(self, dt):
        '''
        Toma la condición actual del planeta y avanza su posicion y velocidad
        en un intervalo de tiempo dt usando el método de Euler explícito. El
        método no retorna nada, pero re-setea los valores de self.y_now.
        '''
        x0,y0,vx0,vy0= self.y_now
        fx=self.edm()[2]
        fy=self.edm()[3]

        xn=x0+ dt*vx0
        yn=y0+ dt*vy0

        vxn=vx0+ dt*fx(x0,y0)
        vyn=vy0+ dt*fy(x0,y0)

        self.y_now= xn,yn,vxn,vyn

        pass

    def avanza_rk4(self, dt):
        '''
        Similar a avanza_euler, pero usando Runge-Kutta 4.
        hacer como array si hay tiempo, se me fundio el cerebro intentando
        se deberia poder hacer en como 4 lineas.
        '''
        x0,y0,vx0,vy0= self.y_now
        fx=self.edm()[2]
        fy=self.edm()[3]

        #RK1
        rx1=dt*vx0;         ry1=dt*vy0
        vx1=dt*fx(x0,y0);   vy1=dt*fy(x0,y0)

        #rk2
        rx2=dt*(vx0+ rx1*0.5);        ry2=dt*(vy0+ ry1*0.5)
        vx2=dt*fx(x0+ rx1*0.5,y0+ ry1*0.5);  vy2=dt*fy(x0+ rx1*0.5,y0+ ry1*0.5)

        #rk3
        rx3=dt*(vx0+ rx2*0.5);        ry3=dt*(vy0+ ry2*0.5)
        vx3=dt*fx(x0+ rx2*0.5,y0+ ry2*0.5);  vy3=dt*fy(x0+ rx2*0.5,y0+ ry2*0.5)

        #rk4
        rx4=dt*(vx0+ rx3);        ry4=dt*(vy0+ ry3)
        vx4=dt*fx(x0+ rx3,y0+ ry3);  vy4=dt*fy(x0+ rx3,y0+ ry3)

        xn=x0+ (rx1+rx2*2+rx3*2+rx4)/6.0
        yn=y0+ (ry1+ry2*2+ry3*2+ry4)/6.0
        vxn= vx0+ (vx1+vx2*2+vx3*2+vx4)/6.0
        vyn= vy0+ (vy1+vy2*2+vy3*2+vy4)/6.0

        self.y_now= xn,yn,vxn,vyn

        pass

    def avanza_verlet(self, dt):
        '''
        Similar a avanza_euler, pero usando Verlet.
        '''
        x0,y0,vx0,vy0= self.y_now
        fx=self.edm()[2]
        fy=self.edm()[3]
        xn= x0 + vx0*dt +fx(x0,y0)*0.5*dt**2
        yn= y0 + vy0*dt +fy(x0,y0)*0.5*dt**2
        vxn=vx0+ (fx(x0,y0)+ fx(xn,yn))*0.5*dt
        vyn=vy0+ (fy(x0,y0)+ fy(xn,yn))*0.5*dt
        self.y_now= xn,yn,vxn,vyn

        pass

    def energia_total(self):
        '''
        Calcula la enérgía total del sistema en las condiciones actuales.
        Resulta quizas demas explicarle al lector que la energia total es
        la suma de la energia cinetica y la potencial gravitatoria
        '''
        x0,y0,vx0,vy0= self.y_now
        return 0.5*self.mass*(vx0**2 +vy0**2)+ cte*self.mass*(self.alpha-np.sqrt(x0**2+y0**2))/(x0**2+y0**2)
        pass
