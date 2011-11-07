# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Icing
-------------------------------------------------------------------------------
Explanation:

How this code works:
    

Notes / Convention:


    exercise lession:
        1 sweep = L**2 single spin sweeps
        S_i,j = S_i,j+z*L
        S_i,j = S_i+y*L,j     with y, z in ZZ
        
        M = 1 / N * SUM_{i=1}^{N = L**2}
 
-------------------------------------------------------------------------------
@author: Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
    v1 2011-11-01   basic implementation
 
BUGS / TODO:
    * 

LICENSE:
    none
    
-------------------------------------------------------------------------------
"""


import sys
import numpy as np
import random as rnd
import matplotlib as mp
import pylab as pl


def main():
    
    n_sites = 10
    dim = 2
    
    rnd.seed(42)
    
    config = np.matrix(zeros([n_sites]*dim), dtype=bool)
    energy = np.matrix(zeros([n_sites]*dim), dtype=bool)


    while True:
        x,y = [rnd.randint(n_sites, n_sites), rnd.randint(n_sites, n_sites)]
        config[x,y] = not config[x,y]
        for i in range(-1,1.1):
            E_old += enegry[x+i, y+j]
            enegry[x+i, y+j] = E_new = 
            
        for j in range(-1,1.1)
            config[x+i, y+j] = 
 












def cmdmain(*args):
    try:
        #print "Starting Program"
        main()
        #print "ending programm"
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