# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Ex08: Extrema Finder using Newton-Raffson and Secant Methods
-------------------------------------------------------------------------------
Explanation:
    
    
How this code works:
    http://www.ifb.ethz.ch/education/IntroductionComPhys/2011-11-15_Ex08.pdf
    http://www.ifb.ethz.ch/education/IntroductionComPhys/CompPhysScript-2009HS-Updated.pdf
    

Notes / Convention:
    there are ready to use objects to handle matrixes in python / numpy,
    which i do use for the running version of the programm,
    but theres a out commented segment that shows how's done without
    it, and some funcuins are only to implement the matrix functions again...
    
    the starting / initial point has to be really close for the methods to
    converge...


-------------------------------------------------------------------------------
@author: Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
    v1 2011-11-22   basic implementation
 
BUGS / TODO:
    clean up abstract function


LICENSE:
    none
    
-------------------------------------------------------------------------------
"""
from os import sys
from numpy import array, matrix, zeros, exp
import matplotlib as mp
import random as rnd
import pylab as pl



class secant(object):
    """implementation of an N dimensional secant solver"""
    
    def __init__(self, equation, x_init, max_step = 100):
        self.equ = equation
        self.dim = equation.dim
        self.x_init = x_init
        self.max_step = max_step
        self.hj = 10**(-8) #we're using 32bit floats, not doubles 
        
       # print 'init', equation.dim, x_init, max_step
        
        
    def solve(self):
        x=array(self.x_init)
        step=0
        X = matrix(x, dtype=float).T

        #this is the fast pythonic way, using built in stuff...
        for step in range(self.max_step):
            J = matrix(self.getJ(X))
            fx = self.equ.fx(X)
            X = X - (J.I * fx)
        return X            


    def getJ(self, X):
        J = zeros([2,2])
        J[:,0] = (self.equ.fx(X+self.hj*matrix('1;0')) - self.equ.fx(X) ).T / self.hj
        J[:,1] = (self.equ.fx(X+self.hj*matrix('0;1')) - self.equ.fx(X) ).T / self.hj
        return J


class newtonraphson(object):
    """implementation of an N dimensional newton-raphson solver"""
    
    def __init__(self, equation, x_init, max_step = 100):
        self.equ = equation
        self.dim = equation.dim
        self.x_init = x_init
        self.max_step = max_step
        
        #print 'init', equation.dim, x_init, max_step
        
        
    def solve(self):
        x=array(self.x_init)
        step=0
        X = matrix(x, dtype=float).T

        #this is the fast pythonic way, using built in stuff...
        for step in range(self.max_step):
            J = matrix(self.equ.jacobian(x))
            fx = self.equ.fx(X)
            X = X - (J.I * fx)
        return X            

        
        #This would be the manual way
        '''
        for step in range(self.max_step):
            J = self.equ.jacobian(x)
            Jinv = self.invert(J)
            fx = self.equ.fx(x)
            Jxfx = self.mult(Jinv, fx)
            x -= Jxfx
        return x      
        '''        


    def invert(self, M):
        """inverts a 2x2 matrix M using suggested method using lists,
        for other dimensions the native one using matrices"""
        
        if self.dim == 2:
            res = zeros([2,2], dtype=float)
            det = float(abs(M[0,0]*M[1,1]-M[1,0]*M[0,1]))
            res[0][0] =   M[1,1] / det
            res[0][1] = - M[0,1] / det
            res[1][0] = - M[1,0] / det
            res[1][1] =   M[0,0] / det
            return matrix(res)
        else:
            return matrix(M).I
            
    def mult(self, M, X):
        """Multiplies a m*m matrix with a vector of length m
        (again, one could simply use built in functions..)"""

        res = zeros(self.dim)
        for i in range(self.dim):
            for j in range(self.dim):
                res[i] += M[i,j]*X[j]
                
        return res
            
        

        
class abstract_function(object):
    """Abstract class of an example:
    Supply the following functions:
    diff(self, X, n): partially differentiate at point X in dimension n
    jacobian the j matrix
    dim the dimension of the probelm...
    """
    
    def __init__(self):
        raise NotImplementedError( "implement __init__()" )
        
    def fx(self, X, n):
        raise NotImplementedError( "implement diff()" )
        
    def jacobian(self):
        raise NotImplementedError( "implement jacobian()" )
        
    def dim(self):
         raise NotImplementedError( "implement dim()" )
       


class exp2d(abstract_function):
    """implementation of abstract function
    of form f(x, y) = exp( -(x-a)**2 - (y-b)**2)"""
    
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.dim = 2
        self.F = lambda x, y: exp( -(x-a)**2 - (y-b)**2)
        self.f = [None, None]
        self.f[0] = lambda x,y : -2*(x-a) * exp(-(x-a)**2 - (y-b)**2)
        self.f[1] = lambda x,y : -2*(y-b) * exp(-(x-a)**2 - (y-b)**2)

        #define the jacobi matrix elements
        self.df = [[None, None],[None, None]]
        #df0(x,y)/dx
        self.df[0][0] = lambda x,y: (4*a**2-8*a*x+4*x**2-2) * exp(-(x-a)**2 - (y-b)**2)
        #df0(x,y)/dy
        self.df[0][1] = lambda x,y: (4*(x-a)*(y-b)) * exp(-(x-a)**2 - (y-b)**2)
        #df1(x,y)/dx
        self.df[1][0] = lambda x,y: (4*(x-a)*(y-b)) * exp(-(x-a)**2 - (y-b)**2)
        #df1(x,y)/dy
        self.df[1][1] = lambda x,y: (4*b**2-8*b*y+4*y**2-2) * exp(-(x-a)**2 - (y-b)**2)
    
    
    def fx(self, X):
        fx = zeros(self.dim, dtype=float)
        x=X[0]
        y=X[1]
        #print 'fx: ', x, y
        fx[0] = self.f[0](x,y)
        fx[1] = self.f[1](x,y)
        #print 'fx: ',matrix(fx).T
        return matrix(fx).T


    def jacobian(self, X):
        x=X[0]
        y=X[1]
        jac = zeros([self.dim, self.dim], dtype=float)
        jac[0][0] = self.df[0][0](x,y)
        jac[0][1] = self.df[0][1](x,y)
        jac[1][0] = self.df[1][0](x,y)
        jac[1][1] = self.df[1][1](x,y)
        return matrix(jac)
    


            
def main():

    print "\nCreating the function f(x, y) = exp( -(x-a)**2 - (y-b)**2)"
    print "   with a=4, b=6.4\n   starting point: 3.8 / 6.2\n   (using 32bit float)\n"
    
    f = exp2d(4,6.4)
    init = array([3.8,6.2])
 
    nr = newtonraphson(f, init, 100)
    print "Newton-raffson:\n", nr.solve()
    
    sec = secant(f, init, 100)
    print "\nSecant:\n", sec.solve()
    


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