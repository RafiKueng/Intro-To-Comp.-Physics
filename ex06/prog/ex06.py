# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Icing Model
-------------------------------------------------------------------------------
Explanation:
    Simulates an assembly of atoms with spin up / down to simulate
    magnetic behavour around T_crit 

How this code works:
    see:    
    http://www.ifb.ethz.ch/education/IntroductionComPhys/2011-11-01_Ex06.pdf
    

Notes / Convention:

    exercise lession notes:
        1 sweep = L**2 single spin sweeps
        S_i,j = S_i,j+z*L
        S_i,j = S_i+y*L,j     with y, z in ZZ
        
        M = 1 / N * SUM_{i=1}^{N = L**2} ???


-------------------------------------------------------------------------------
@author: Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
    v1 2011-11-01   some drafts
    v2 2011-11-08   basic implementation
 
BUGS / TODO:
    * check energy calculation, theres probably an error in there

LICENSE:
    none
    
-------------------------------------------------------------------------------
"""


import sys
import numpy as np
import random as rnd
import matplotlib as mp
import pylab as pl


def init_grid(n_sites, state):
    """
    Set state =
        -1 every point spin down
        0 to randomize the init grid
        +1 every point spin up
        +2 alternating spins
    """
    
    #init everthing to state
    grid = np.array(np.ones([n_sites]*2), dtype=np.int8)*state

    if state == 0:
        for i in range(n_sites):
            for j in range(n_sites):
                grid[i,j] = rnd.choice([-1,1])
    elif state == 2:
        for i in range(n_sites):
            for j in range(n_sites):
                grid[i,j] = (i*j)
        grid = grid%2*2-1
        
    
    return grid

def get_energy(grid):
    E = 0
    n = len(grid)
    for i in range(n):
        for j in range(n):
            E += grid[i][j]*grid[i-1][j] + grid[i][j]*grid[i][j-1]
    return E

def get_mag(grid):
    n = len(grid)
    mag = sum(sum(grid))
        
    mag /= float(n*n)
    #print mag
    return mag

def icing(T = 2.27, n_sites = 20, n_sweeps = 20, grid = None):
    
    if grid == None:
        grid = init_grid(n_sites,-1)
    
    sweeps = steps = 0
    rnd.seed(42)
 
    #precalculate the exp function values for speed
    #{-8: 0.000/T, 0: 1.0/T, -4: 0.018/T, 4: 54.598/T, 8: 2980.958/T}
    exp_dict = dict([[2*x , np.exp(2.*x/T)] for x in range(-4,5,2)])
    
    #uses int by def
    energy = get_energy(grid)
    energy_list = []
    energy_list.append(energy)
    
    mag = get_mag(grid)
    mag_list = []
    mag_list.append(mag)

    step_list = []
    step_list.append(0)
    steps += 1
    
    while steps < n_sites**2 * n_sweeps:
        #plot.set_data(grid)
        #pl.draw()        

        x = rnd.randrange(0, n_sites)
        y = rnd.randrange(0, n_sites)
        
        grid[x,y] *= -1

        dE = (grid[(x+1)%n_sites, y] +
              grid[(x-1)%n_sites, y] +
              grid[x, (y+1)%n_sites] +
              grid[x, (y-1)%n_sites]) * -2 * grid[x,y]
        
       
        if dE <= 0 or exp_dict[-dE] > rnd.random():
            energy += dE
            step_list.append(steps)
            energy_list.append(energy)
            mag_list.append(get_mag(grid))
        
        else:
            grid[x,y] *= -1
            
        steps += 1
       
    #pl.plot(energy_list)    
    #pl.show()
    #pl.plot(mag_list)    
    #pl.show()
    #pl.matshow(grid)
    #pl.show()
    #print energies
    #print step_list    
    
    return grid, energy_list, mag_list, step_list
    

def main(n_sites = 20):
    Temprange = np.arange(0.1, 4.1, 0.1)
    
    n_sweeps = 100

    Energy = []
    Magnetisation = []
    
    for j, T in enumerate(Temprange):
        if j == 0:
            grid, energy_list, mag_list, step_list = icing(T, n_sites, n_sweeps)
        else:
            grid, energy_list, mag_list, step_list = icing(T, n_sites, n_sweeps/2., grid)
        
        M = np.average(np.array(mag_list))
        E = np.average(np.array(energy_list))
        
        pl.plot(step_list, mag_list,'ro')
        pl.title('Evolution of Magnetisation')
        pl.xlabel('StepNr')
        pl.ylabel('Magnetisation')
        pl.savefig('steps/size_%s_magnetisation_at_T_%s.png' % (n_sites, T))
        pl.close()
        
        pl.plot(step_list, energy_list, 'ro')
        pl.title('Evolution of Energy')
        pl.xlabel('StepNr')
        pl.ylabel('Energy')
        pl.savefig('steps/size_%s_energy_at_T_%s.png' % (n_sites, T))
        pl.close()
        
        print 'at T=', T, ': E=',E,'M=',M
        
        Magnetisation.append(M)
        Energy.append(E)
        
    pl.plot(Temprange, Magnetisation, 'ro')
    pl.title('Temperature vs. Magnetisation')
    pl.xlabel('Temperature K/k_B')
    pl.ylabel('Magnetisation')
    pl.savefig('size_%s_evol_of_Magnetisation.png'% n_sites)
    #pl.show()
    pl.close()

    pl.plot(Temprange, Energy, 'ro')
    pl.title('Temperature vs. Energy')
    pl.xlabel('Temperature K/k_B')
    pl.ylabel('Energy')
    pl.savefig('size_%s_evol_of_Energy.png'% n_sites)
    #pl.show()
    
    print 'check the png files in the folder and the ones in the steps subfolder\n'








def cmdmain(*args):
    try:
        main(10)
        main(20)
        main(40)
        print (
'''
REPORT:

It can be seen, that if we start below T_crit =~ 2.269: the system tends to
a magnetisation, depending on the starting conditions, either +1 odr -1.
For starting temperatures above T_crit, the magnetisation vanishes,
independend of the starting position. At least, this is expected...
In my simulation, the mag. vanishes a little later (0.5 around T=2.4). And
the resulting magnetisation below T_crit has alwasy the same sign, actually
it should be random near +/- 1. 

The size of the grid didn't change much of the simulation (tested with 10, 20
and 40), the plots look almost the same, exept the turning point for the
magnetisation is shifted slighlty to lower T, near T_crit with bigger sizes.
Also, the curve for the Magnetisation gets smoother for T > T_crit for
bigger sized grids. (see in the 10 size grid around T = 2.5)

There seems to be an error with the Energy calculation, it shootes over the
possible maximum, but I'm a bit too tired for finding the error..

Rafael Kueng
''')
        
    except:
        raise
        # handle some exceptions
    else:
        return 0 # exit errorlessly     
        

def classmain():
    print '[display notes if imported as a class]'
    

        
if __name__ == '__main__':
    sys.exit(cmdmain(*sys.argv))
else:
    classmain()