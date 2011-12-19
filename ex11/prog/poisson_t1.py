# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Ex11, Task1: Poissons Equation
-------------------------------------------------------------------------------
Explanation:
    The task is to solve the above problem using the fnite difference method.
    
How this code works:
    

Notes / Convention:



-------------------------------------------------------------------------------
@author: Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
    v1 2011-12-12   basic implementation
 
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

p = array([0.5,0.5]) #position of charge
box = [0,1] #size of box: [ xmin=ymin, xmax = ymax ]
N = 21. #number of points along one axis
gridpnts, dx = linspace(box[0],box[1],N, endpoint=True, retstep=True)
epsilon = 10e-10

def JacobiRelax(field):
    grid = zeros([N,N])
    steps = 0
    delta = 1
    while delta > epsilon:
        steps += 1
        delta = 0
        grid_new = zeros([N,N])    
        for i, xi in enumerate(gridpnts):
            if xi == 0 or xi == 1:
                continue
            for j, yj in enumerate(gridpnts):
                if yj == 0 or yj == 1:
                    continue
                
                grid_new[i][j] = (grid[i+1][j]+grid[i-1][j]+grid[i][j+1]+grid[i][j-1]) / 4. + dx*dx*field[i][j]/4.
                dif = abs(grid[i][j] - grid_new[i][j])
                if dif>delta:
                    delta = dif
        grid = grid_new

    print 'steps', steps
    
    plt.subplot(3,3,1)
    CS = plt.contour(gridpnts,gridpnts,grid)
    plt.clabel(CS, inline=1, fontsize=10)
    plt.title('Contour JacobiRelax')

    plt.subplot(3,3,2)
    CS = plt.contour(gridpnts,gridpnts,log(grid))
    plt.clabel(CS, inline=1, fontsize=10)
    plt.title('Contour JacobiRelax (log)')

    plt.subplot(3,3,3)
    plt.imshow(grid, origin="lower")
    plt.colorbar()
    plt.title('Values JacobiRelax')
    
    plt.subplot(3,3,7)
    px,py = gradient(grid)
    plt.quiver(gridpnts,gridpnts,px,py)
    plt.title('Gradients JacobiRelax')
    
    return grid

    
def GaussSeidel(field):
    grid = zeros([N,N])
    steps = 0
    delta = 1
    while delta > epsilon:
        steps += 1
        delta = 0
        for i, xi in enumerate(gridpnts):
            if xi == 0 or xi == 1:
                continue
            for j, yj in enumerate(gridpnts):
                if yj == 0 or yj == 1:
                    continue
                oldval = grid[i][j]
                grid[i][j] = (grid[i+1][j]+grid[i-1][j]+grid[i][j+1]+grid[i][j-1]) / 4. + dx*dx*field[i][j]/4.
                dif = abs(grid[i][j] - oldval)
                if dif>delta:
                    delta = dif

    print 'steps', steps
    
    plt.subplot(3,3,4)
    CS = plt.contour(gridpnts,gridpnts,grid)
    plt.clabel(CS, inline=1, fontsize=10)
    plt.title('Contour GaussSeidel')

    plt.subplot(3,3,5)
    CS = plt.contour(gridpnts,gridpnts,log(grid))
    plt.clabel(CS, inline=1, fontsize=10)
    plt.title('Contour GaussSeidel (log)')
    
    
    plt.subplot(3,3,6)
    plt.imshow(grid, origin="lower")
    plt.colorbar()
    plt.title('Values GaussSeidel')
    
    plt.subplot(3,3,9)
    px,py = gradient(grid)
    plt.quiver(gridpnts,gridpnts,px,py)
    plt.title('Gradients GaussSeidel')
    
    return grid


def main():

    nx = floor(p[0]/(box[1]/N))
    ny = floor(p[1]/(box[1]/N))
    field=zeros([N,N])    
    field[nx][ny] = 1./(dx*dx)
    
    #print gridpnts
    #print field
    
    print 'jacobi'
    g1 = JacobiRelax(field)
    print 'GaussSeidel'
    g2 = GaussSeidel(field)
    
    plt.subplot(3,3,8)
    plt.imshow(g1-g2, origin="lower")
    plt.colorbar()
    plt.title('Differences (values)')
    plt.show()
        
 
    
    
    
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