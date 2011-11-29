# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Ex09, Task 1: Random walk
-------------------------------------------------------------------------------
Explanation:
    Simulates the randomwalk for arbitraty stepfunction in arbitrary dimensions
    
    instance the class randomwalk and call it to do everything (inkl plots).
    
    rndwk = randomwalk(stepfn, n_steps,
                       n_tries=10000, gridwidth=None, n_bins=100)
    rndwk()
    
How this code works:
    one can create an object of class randomwalk and pass it a step function
    on init.
    the stepfuncin is expected to accept the actual position and stepnr, and
    return a vector (array) of dim n contiaining the next step (deltas)
    
    X_i+1 = stepfn(X_i, i) + X_i
    
    See in main for some example stepfunctions.
    
    To determine, on how many dimenstion we should work, the stepfn is called
    once at the beginning, and the length of the returned array determines the
    dimension of the whole affair...
    
    Due to class, instances and quite a few function calls, it's not very
    fast, but quite portable...
    

Notes / Convention:



-------------------------------------------------------------------------------
@author: Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
    v1 2011-11-23   basic implementation for comp.sci module
    v2 2011-11-28   adjusted to ex09, task1 intro.comp.phys., cleaned up
 
BUGS / TODO:
*   reenable binning, histogram and plotting functions


LICENSE:
    none
    
-------------------------------------------------------------------------------
"""

from os import sys
from numpy import *
import matplotlib as mp
import pylab as pl
import random as rnd


class randomwalk(object):
    """
    stepfn
        should return the next step. it can possibly depend on the
        actual position X and the nr of steps, but for true random
        walk it shouldn't, of corse...
        stepfn(X, i)
    n_steps
        one random walk constis of n_steps steps
    n_tries
        do n_tries random walks
    n_bins = 100:
        number of bins for the histogram. only for manual binning in continous
        space; if fixed grid (grid_with set to some value, discrete space) is
        used: n_bin = n_steps, regardless of value set here.
    grid_with = None:
        this problem us usung descrete space, if set to some value
        size of steps in unit directions, aka size of grid of possible position,
        set to None if continous space, then n_bins is used
    """

    def __init__(self, stepfn, n_steps, n_tries=10000, grid_with = None, n_bins = 100):

        self.stepfn = stepfn
        self.dim = len(stepfn()) #length of the vector the stepfn returns...
        self.n_steps = n_steps
        self.n_tries = n_tries
        self.n_bins = n_bins
        self.grid_with = grid_with
        
        #self.result = []
        self.result_dist2 = []
        self.result_element = [[] for i in range(self.dim)]
        
        self.dist_bin = None
        self.dist_d_bin = None
        self.dist_hist = None
        
        self.element_bin = None
        self.element_d_bin = None
        self.element_hist = None
        
    def __call__(self):
        self.nWalks()
        self.genHistogram()
        self.plot()
        
        
        
    def walk(self):
        X = zeros(self.dim, dtype=float)

        for i in range(self.n_steps):
            X += self.stepfn(X, i)
        
        #self.result.append([sqrt(sum(X**2))] + [X])
        self.result_dist2.append(sum(X**2))
        #[self.result_element[i].append(X[i]) for i in range(self.dim)]
            
    def nWalks(self):
        mean_r2 = 0
        mean_r22 = 0
    
        for i in range(self.n_tries):
            X = zeros(self.dim, dtype=float)

            for i in range(self.n_steps):
                X += self.stepfn(X, i)
            
            sm = sum(X**2)
            mean_r2 += sm
            mean_r22 += sm*sm
            
            
            self.result_dist2.append(sum(X**2))
            #[self.result_element[i].append(X[i]) for i in range(self.dim)]
            
        mean_r2 /= self.n_tries
        mean_r22 /= self.n_tries
        delta = sqrt(1./self.n_tries* ( mean_r22 -  mean_r2**2) )

        return mean_r2, delta

'''        
    def genHistogram(self):
        max_dist = max(self.result_dist)
        max_element = max( [max(self.result_element[i]) for i in range(self.dim)] )#total max in all dimensions
        n_events = len(self.result_dist)*1.0
            
            
        #print max_dist, self.n_bins
        
        if self.grid_with == None:
            dist_bin, dist_d_bin = linspace(0, max_dist, self.n_bins, retstep=True)
            element_bin, element_d_bin = linspace(-max_element, max_element, self.n_bins, retstep=True)
        else:
            # this part still has some bugs
            offset = (self.n_steps%2)/2.
            element_d_bin = dist_d_bin = self.grid_with*2
            dist_bin = arange(0, dist_d_bin*(self.n_steps+1), dist_d_bin) - (0.5+offset)*dist_d_bin
            
            element_bin  = arange(-self.grid_with*(self.n_steps),
                                    self.grid_with*(self.n_steps+2+(0.5-offset)),
                                    element_d_bin) - (0.5+offset)*element_d_bin
       
        
        
        dist_hist = histogram(self.result_dist, dist_bin)[0] / n_events
        
        element_hist = [[] for i in range(self.dim)]
        for i in range(self.dim):
            element_hist[i] = histogram(self.result_element[i], element_bin)[0] / n_events 


        #print element_d_bin
        #print '\n'
        #print element_bin
        #print '\n'        
        #print element_hist[0]
        #print '\n'   

        
        self.dist_bin = dist_bin
        self.dist_d_bin = dist_d_bin
        self.dist_hist = dist_hist
        
        self.element_bin = element_bin
        self.element_d_bin = element_d_bin
        self.element_hist = element_hist
        
        
    def plot(self, plot_distr = True):
        """
        plots the results
        plot_distr = True plots the theoretical results with a red line..
        """
        #print 'plot:', self.dist_bin[:-1],self.dist_hist
        
        pl.figure()
        pl.subplot(self.dim+1,1,1)
        pl.bar(self.dist_bin[:-1],self.dist_hist, width=self.dist_d_bin)
        
        if plot_distr:
            distrange = linspace(self.dist_bin[0], self.dist_bin[-1], 1000)
            elementrange = linspace(self.element_bin[0], self.element_bin[-1], 1000)
            
            maxwell = 2*distrange/float(self.n_steps)*exp(-distrange**2/float(self.n_steps))
            gauss = 1/(pi*self.n_steps)*exp(-elementrange**2/float(self.n_steps))
            
            pl.plot(distrange, maxwell, 'r:')
            
        
        for i in range(self.dim):
            pl.subplot(self.dim+1,1,i+2)
            pl.bar(self.element_bin[:-1],self.element_hist[i], width=self.element_d_bin)
            pl.xlim(self.element_bin[0], self.element_bin[-1])
            
            if plot_distr:
                pl.plot(elementrange, gauss, 'r:')

        pl.show()
            
'''        

def main(n_tries):
    if n_tries == None:
        n_tries = 500

    # Some demonstation step funkctions.
    
    #1d, discrete, go left or right, equal prob
    stepfn = lambda x=0, y=0: array([rnd.choice([-1,1])])
    
    #2d, discrete, go 1 north, east, south or west with equal prob.
    stepfn_nesw = lambda x=0, y=0: array(rnd.choice([[-1,0],[1,0],[0,1],[0,-1]]))
    
    #3d, discrete, go one up/down/left/right/front/back
    stepfn_3d = lambda x=0, y=0: array(rnd.choice([[-1,0,0],[1,0,0],[0,1,0],[0,-1,0], [0,0,-1],[0,0,1]]))
    
    #2d, continous, steplength 1, any direction
    def stepfn_anydir2d(x=0, y=0):
        beta = rnd.random()*2*pi
        return array([cos(beta), sin(beta)])

    #2d dicrete, next nearest neighbours,
    #variable steplength (1 odr sqrt(2)), n, ne, e, se, s, sw, w, nw, or 0 (stand still)
    stepfn_nn = lambda x=0, y=0: array(rnd.choice([[0,0], [1,1],[1,-1],[-1,1],[-1,-1], [-1,0],[1,0],[0,1],[0,-1]]))
        
    n_steps = [3,4,5,6,7,8,9,] + range(10,20,2) + range(20,100,5)
    res_r2 = []
    res_d = []
    res_p = []
        
    for N in n_steps:
        rndwk = randomwalk(stepfn_anydir2d, N, n_tries, None, 100)
        r2, d = rndwk.nWalks()
        p = d*1./r2
        res_r2.append(r2)
        res_d.append(d)
        res_p.append(p)
        print 'N=%3.0f, <R2>=%7.2f, delta=%5.2f, error=%4.1f%%' % (N, r2, d, p*100)
        
    pl.figure()
    pl.subplot(311)
    pl.plot(n_steps, res_r2)
    pl.plot([n_steps[0],n_steps[-1]],[n_steps[0]-1,n_steps[-1]-1],'r:')
    pl.title("<R^2>, delta, error vs N, for %1.0f random walks"%n_tries)
    pl.xlabel("")
    pl.ylabel("<R^2>")

    pl.subplot(312)
    pl.plot(n_steps, res_d)
    pl.xlabel("")
    pl.ylabel("delta")
 
    pl.subplot(313)
    pl.plot(n_steps, res_p)
    pl.xlabel("N steps")
    pl.ylabel("error")
 
    pl.show()
    
def main2():
    #2d, continous, steplength 1, any direction
    def stepfn_anydir2d(x=0, y=0):
        beta = rnd.random()*2*pi
        return array([cos(beta), sin(beta)])

        
    n_steps = 20
    n_tries = [10, 50] + range(100,1000,100) + range(1000, 10000, 1000) + [10000, 20000, 50000,100000]
    
    res_r2 = []
    res_d = []
    res_p = []
        
    for M in n_tries:
        rndwk = randomwalk(stepfn_anydir2d, n_steps, M, None, 100)
        r2, d = rndwk.nWalks()
        p = d*1./r2
        res_r2.append(r2)
        res_d.append(d)
        res_p.append(p)
        print 'M=%5.0f, <R2>=%7.2f, delta=%5.2f, error=%4.1f%%' % (M, r2, d, p*100)
        
    pl.figure()
    pl.subplot(311)
    pl.semilogx(n_tries, res_r2)
    #pl.plot([n_tries[0],n_steps[-1]],[n_steps[0]-1,n_steps[-1]-1],'r:')
    pl.title("<R^2>, delta, error vs M random walks, for %2.0f steps"%n_steps)
    pl.xlabel("")
    pl.ylabel("<R^2>")

    pl.subplot(312)
    pl.semilogx(n_tries, res_d)
    pl.xlabel("")
    pl.ylabel("delta")
 
    pl.subplot(313)
    pl.semilogx(n_tries, res_p)
    pl.semilogx([10,100000], [0.01, 0.01],'r:')
    pl.xlabel("M tries")
    pl.ylabel("error")
 
    pl.show()   
    
    
def cmdmain(*args):
    try:
        if len(args) == 2:
            main(int(args[1]))
        else:
            main2()
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