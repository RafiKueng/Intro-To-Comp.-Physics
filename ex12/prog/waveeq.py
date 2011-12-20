# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Ex12: Wave Equation
-------------------------------------------------------------------------------
Explanation:
    The task is to solve the wave eq using the finite difference method.
    
How this code works:
    

Notes / Convention:



-------------------------------------------------------------------------------
@author: Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
    v1 2011-12-20   basic implementation
 
BUGS / TODO:


LICENSE:
    none
    
-------------------------------------------------------------------------------
"""

from os import sys
from numpy import *
import matplotlib as mp
import matplotlib.pyplot as plt
import pylab as pl
import random as rnd


class wave_eq(object):
    def __init__(self, field, field_old, b):
        #self.x = x
        self.u = field
        self.u_old = field_old
        self.b = b
       
        
        
    def step(self):
        b = self.b
        u = self.u
        u_old = self.u_old
        #u_new = array([0]*len(u))
        
        #print 'inside step'
        #print u
        #print u_old
        
        #overwrite the t-dt array (u_old) with the new (t+dt) values
        for i in range(0,len(u)-1):
            u_old[i] = 2*(1-b)*u[i] + b*(u[i+1] + u[i-1]) - u_old[i]
        u_old[len(u)-1] = 2*(1-b)*u[len(u)-1] + b*(u[0] + u[len(u)-2]) - u_old[len(u)-1]
        
        
        # u_old is u_new, u_new is u_old
        self.u_old = u
        self.u = u_old
        
    def run(self, nsteps):
        for i in range(nsteps):
            self.step()



class wave_eq_simple(object):
    def __init__(self, field, field_old, b):
        #self.x = x
        self.u = field
        self.u_old = field_old
        self.b = b
       
        
        
    def step(self):
        b = self.b
        u = self.u
        u_old = self.u_old
        
        #overwrite the t-dt array (u_old) with the new (t+dt) values
        for i in range(0,len(u)-1):
            u_old[i] = u[i+1] + u[i-1] - u_old[i]
        u_old[len(u)-1] = u[0] + u[len(u)-2] - u_old[len(u)-1]
        
        
        # u_old is u_new, u_new is u_old
        self.u_old = u
        self.u = u_old
        
    def run(self, nsteps):
        for i in range(nsteps):
            self.step()        
        
        


def task1():
    '''demonstration'''
    
    #TASK 0: Demo
    L = 1000 #length, using boundary condition u(x+L)=u(x)
    dx = 1.
    dt = 0.1
    t_max = 100
    c = +10
    
    b = (c*dt/dx)**2
    
    #init fields
    x = arange(0,L+dx/2.,dx) #[0, .... , L], consider 0 = L

    #starting conditions
    field_t = exp(-(x-10)**2) #starting condition at t0
    field_tmdt = exp(-(x-c*dt-10)**2) #starting condition at t0-dt
    
    eq1 = wave_eq(field_t, field_tmdt, b)
    
    plt.ion()
    plot, = plt.plot(x, field_t)
    
    for t in arange(0,t_max,dt):
        print 'outer loop, t=',t
        eq1.step()
        plot.set_ydata(eq1.u)
        plt.draw()
    
def task2():
    '''analysis of b'''
    
    L = 200 #length, using boundary condition u(x+L)=u(x)
    dx = 1.
    #dt = 0.1
    #t_max = 10
    #c = 5.
    

    
    #init fields
    x = arange(0,L+dx/2.,dx) #[0, .... , L], consider 0 = L

    #starting conditions

    
    c_range = linspace(-20,20,50)
    dt_range = linspace(-1,1,50)
    #c_range = [5,10.,15.]
    #dt_range = [0.1]
    
    res = [[0]*len(dt_range) for _ in c_range]
    
    for ic, c in enumerate(c_range):
        print ic, 'of 49 done'
        for idt, dt in enumerate(dt_range):
        
            #print ic, c, idt, dt
            b = (c*dt/dx)**2
            
            field_org = exp(-(x-100)**2) #starting condition at t0
            
            field_t = exp(-(x-100)**2) #starting condition at t0
            field_tmdt = exp(-(x-c*dt-100)**2) #starting condition at t0-dt


            eq = wave_eq(field_t, field_tmdt, b)
            eq.run(10) #do 10 steps and then compare the waveforms
            
            diff = field_org-eq.u
                
            res[ic][idt] = abs(sum(diff))
            
            #print flank_org, flank, flank+c/dt, sum(diff)
            
            #plt.subplot(5,1,1)
            #plt.plot(x[200:801],diff)
            #plt.subplot(5,1,2)
            #plt.plot(x[200:801],field_org[200:801])
            #plt.subplot(5,1,3)
            #plt.plot(x[200:801],eq.u[200:801])
            #plt.subplot(5,1,4)
            #plt.plot(x,field_org)
            #plt.subplot(5,1,5)
            #plt.plot(x,eq.u)
            #plt.show()
            
    #print res
    #plt.imshow(array(res).T, interpolation=None)
    plt.pcolor(c_range, dt_range, log(array(res)).T, vmin=-10, vmax=10)
    #cmap = plt.cm.get_cmap('jet', 10)
    plt.colorbar()
    #plt.axis()
    plt.title('Log of divergence/difference of moved curve [log(sum(diff()))]')
    plt.xlabel('c')
    plt.ylabel('dt')
    plt.show()
 
 
def task2b():
    '''demonstration'''
    
    #TASK 0: Demo
    L = 200 #length, using boundary condition u(x+L)=u(x)
    dx = 1.
    dt = 0.5
    t_max = 50
    c = -10
    
    b = (c*dt/dx)**2
    
    #init fields
    x = arange(0,L+dx/2.,dx) #[0, .... , L], consider 0 = L

    #starting conditions
    field_t = exp(-(x-100)**2) #starting condition at t0
    field_tmdt = exp(-(x-c*dt-100)**2) #starting condition at t0-dt
    
    eq1 = wave_eq(field_t, field_tmdt, b)
    
    #plt.ion()
    #plot, = plt.plot(x, field_t)
    
    for t in arange(0,t_max,dt):
        #print 'outer loop, t=',t
        eq1.step()
        #plot.set_ydata(eq1.u)
        #plt.draw()
        
    plt.plot(x, field_t)
    plt.show()
        
        
        
def task3(fn_t, fn_tmdt, c):
    '''demonstration'''
    
    L = 1000 #length, using boundary condition u(x+L)=u(x)
    dx = 1.
    dt = 0.5
    t_max = 100
    #c = -10
    
    b = (c*dt/dx)**2
    
    #init fields
    x = arange(0,L+dx/2.,dx) #[0, .... , L], consider 0 = L

    #starting conditions
    field_t = fn_t(x,dt) #starting condition at t0
    field_tmdt = fn_tmdt(x,dt) #starting condition at t0-dt
    
    eq1 = wave_eq_simple(field_t, field_tmdt, b)
    
    plt.ion()
    plot, = plt.plot(x, field_t)
    
    for t in arange(0,t_max,dt):
        print 'outer loop, t=',t
        eq1.step()
        plot.set_ydata(eq1.u)
        plt.draw()
        
        
def main():
    print 'TASK 1\n'
    task1()
    
    print 'TASK 2\n'
    task2()
    
    task2b()
    
    print 'TASK 3 - example with sinus wave, fixed for t<0'
    l=4*pi/1000.
    fn_t = lambda x,dt: sin(l*x)
    fn_tmdt = lambda x,dt: sin(l*x)
    c=10
    task3(fn_t, fn_tmdt, c)

    
def cmdmain(*args):
    try:
        main()
    except:
        raise
        # handle some exceptions
    else:
        return 0 # exit errorlessly     
        

def classmain():
    print 'call main()'
    

        
if __name__ == '__main__':
    sys.exit(cmdmain(*sys.argv))
else:
    classmain()