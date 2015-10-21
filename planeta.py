#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Planeta(object):
    G=1.0
    M=1.0
    cte=G*M
    '''
    Complete el docstring.
    '''

    def __init__(self, condicion_inicial, alpha=0):
        '''
        __init__ es un método especial que se usa para inicializar las
        instancias de una clase.

        Ej. de uso:
        mercurio = Planeta([x0, y0, vx0, vy0])
        print(mercurio.alpha)
        0.
        '''
        self.y_actual = condicion_inicial
        self.t_actual = 0.
        self.alpha = alpha
        self.m = 1.0 #mass
    def ecuacion_de_movimiento(self):
        '''
        Implementa la ecuación de movimiento, como sistema de ecuaciónes de
        primer orden.
        '''
        x,y,vx,vy= self.y_actual #r y r' ahora
        fx=lambda x,y,t: (cte*x/(x**2+y**2)**2)*(np.sqrt(x**2+y**2) - 2*self.alpha)
        fy=lambda x,y,t: (cte*y/(x**2+y**2)**2)*(np.sqrt(x**2+y**2) - 2*self.alpha)
        ###fx = #...(lambda x: x*2)(3) lambda x: x*2
        # fy = ...

        return [vx, vy, fx, fy]

    def avanza_euler(self, dt):
        '''
        Toma la condición actual del planeta y avanza su posicion y velocidad
        en un intervalo de tiempo dt usando el método de Euler explícito. El
        método no retorna nada, pero re-setea los valores de self.y_actual.
        '''
        dy = dt*(self.ecuacion_de_movimiento())
        self.y_actual += dy
        self.t_actual += dt
        pass

    def avanza_rk4(self, dt):
        '''
        Similar a avanza_euler, pero usando Runge-Kutta 4.
        '''
        rk1=self.ecuacion_de_movimiento()
        rk2=self.ecuacion_de_movimiento(dt*rk1/2.0)
        rk3=self.ecuacion_de_movimiento(dt*rk2/2.0)
        rk4=self.ecuacion_de_movimiento(dt*rk3)

        dy= dt*(rk1 +rk2*2 +rk3*2 +rk4)/6.0
        self.y_actual +=dy
        self.t_actual +=dt
        pass

    def avanza_verlet(self, dt):
        '''
        Similar a avanza_euler, pero usando Verlet.
        '''
        x,y,vx,vy = self.y_actual
        Y= x,y #posicion
        V= vx,vy
        f=self.ecuacion_de_movimiento()
        dYn = V*dt+ dt**2*f[2:]/2.0
        dVn = dt*((f[:1])+f(xn,yn,self.t_actual+dt))/2.0

        self.y_actual += dYn,dVn
        self.t_actual += dt
        pass

    def energia_total(self):
        '''
        Calcula la enérgía total del sistema en las condiciones actuales.
        '''
        x,y,vx,vy= self.y_actual
        return 0.5*m*(vx**2 +vy**2)+ cte*m*(self.alpha-np.sqrt(x**2+y**2))/(x**2+y**2)
        pass
