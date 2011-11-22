# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Ex08: Newton Integration
-------------------------------------------------------------------------------
Explanation:
    
    
How this code works:
    http://www.ifb.ethz.ch/education/IntroductionComPhys/2011-11-15_Ex08.pdf
    

Notes / Convention:
    there are ready to use objects to handle matrixes in python / numpy,
    which i don't use, since i suppose it's demanded that we implement
    them ourselves...


-------------------------------------------------------------------------------
@author: Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
    v1 2011-11-22   basic implementation
 
BUGS / TODO:


LICENSE:
    none
    
-------------------------------------------------------------------------------
"""
from os import sys
from numpy import array, pi, sqrt, sin, cos
import matplotlib as mp
import random as rnd
import pylab as pl


class newtonraphson(object):
    """implementation of an N dimensional newton-raphson solver"""
    
    def __init__(self, equation, x_init, max_step = 1000):
        self.equation = equation
        self.x_init = x_init
        self.max_step = max_step
        
    def solve(self):
        return result

    def get_max(self):
        pass
        
    def get_min(self):
        pass
        
    def get_extr(self):
        pass

        
class abstract_function(object):
    """Abstract class of an example:
    Supply the following functions:
    diff(self, X, n): partially differentiate at point X in dimension n
    """
    def __init__(self):
        raise NotImplementedError( "implement __init__()" )
        
    def diff(self, X, n):
        raise NotImplementedError( "implement diff()" )
        
    def get_jacobian(self):
        raise NotImplementedError( "implement get_jacobian()" )


class exp2d(abstract_function):
    """implementation of abstract function
    of form f(x, y) = exp( -(x-a)**2 - (y-b)**2)"""
    
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.equ = lambda x, y: exp( -(x-a)**2 - (y-b)**2)
        
    def diff(self, X, n):
        pass
        
    


            
def main():
    pass
    


def cmdmain(*args):
    try:
        main()
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