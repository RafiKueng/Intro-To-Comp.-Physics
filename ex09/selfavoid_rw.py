# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Ex09, Task2: Self avoiding Random walk
-------------------------------------------------------------------------------
Explanation:
    http://www.ifb.ethz.ch/education/IntroductionComPhys/2011-11-22_Ex09.pdf

    Simulates the Self Avoiding RandomWalk (sarw) in 3 dimensions
    (small modifications let it run in 2d)
    
    instance the class sarw and call it to do everything and return
    mean_R2 and delta.
    
    sarndwk = sarw(steplength=1, n_steps = 10, n_tries=5000)
    sarndwk()


How this code works:
    It uses a kd tree for storing the path of the point, and gets a list of
    the nearest neigbours within a distance (2*r) from the point. if this
    list is empty (no other point in a radius of 2r) there's no overlapping
    of the spheres.
    

Notes / Convention:
    please note the source of the kd tree, see kdtree.py
    i'm used to kd trees, but i felt it's quite an overkill to implement it
    myself, so i hope you're ok with my aproach of taking one and modifying it
    for my needs. I used kdtrees quite heavily in my bachelors thesis
    (the haloviz part of https://hpcforge.org/projects/pv-astro/)



-------------------------------------------------------------------------------
@author: Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
    v1 2011-11-23   basic implementation random walk
    v2 2011-11-28   modification for self avoidance, stipping down unused parts
 
BUGS / TODO:
*   NO dead end dedetion, handling (especially in 2d this could be a major
    problem causing never ending loops)


LICENSE:
    none
    kdtree.py: GPLv3
    
-------------------------------------------------------------------------------
"""

from os import sys

from numpy import *

import matplotlib
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import pylab
import pylab as pl

import random as rnd

import kdtree


class sarw(object):
    """
    self avoiding random walk
    
    steplength
        how long is a step
    n_steps
        one random walk constis of n_steps steps
    n_tries
        do n_tries random walks
    """

    def __init__(self, steplength = 1, n_steps=10, n_tries=5000):

        self.dim = 3 #length of the vector the stepfn returns...
        self.steplength = steplength
        self.n_steps = n_steps
        self.n_tries = n_tries
        
        self.n_bins = 100

        self.result_dist2 = []
        self.result_element = []

        self.dist_bin = None
        self.dist_d_bin = None
        self.dist_hist = None
        
        self.element_bin = None
        self.element_d_bin = None
        self.element_hist = None
        
    def __call__(self):
    
        mean_R2, delta = self.nWalks()
        print '<R^2> =', mean_R2, '\n   delta =', delta, '\n   (error: ',  100.*delta/mean_R2,'%)'
        self.genHistogram()
        self.plot()
        
        
    def walk(self, paint=False):
        """does one randomwalk with n_steps. saves the result to the
        classes list and returns it
        returns [distance, array([x,y,z])]
        """
        X = zeros(self.dim, dtype=float)
        tree = kdtree.create([X])

        for i in range(self.n_steps):
            successful = False
            while True:
                phi = rnd.random()*2*pi
                psi = rnd.random()*2*pi # for 2d set psi to 0
                
                dX = array([sin(phi)*cos(psi),
                            cos(phi),
                            sin(phi)*sin(psi)]) * 2
                X_new  = X+dX
                #print dX, X_new
                
                #check if this new point is within the sphere of other
                if len(tree.search_nn_dist(X_new, 2*self.steplength)) == 0:
                    X = X_new
                    tree.add(X)
                    tree = tree.rebalance()
                    #print "   accepted"
                    break
        self.result_dist2.append(sum(X**2))
        self.result_element.append(X)
        
        if paint:
            """This only makes sense if solving the 2d prob..."""
            circles = []
            for i, p in enumerate(list(kdtree.level_order(tree))):
                circles.append(Circle(p.data, self.steplength))
            
            fig=pylab.figure()
            ax=fig.add_subplot(111)
            colors = 100*pylab.rand(len(circles))
            p = PatchCollection(circles, cmap=matplotlib.cm.jet, alpha=0.4)
            p.set_array(pylab.array(colors))
            ax.add_collection(p)
            pylab.colorbar(p)

            pylab.show()
            
        return sum(X**2), X
            
    def nWalks(self):
        mean_R2 = 0
        mean_R22 = 0
        
        for i in range(self.n_tries):
            dist2, point = self.walk()
            #print dist2, point
            
            mean_R2 += dist2
            mean_R22 += dist2**2
            
        mean_R2 /= 1.0*self.n_tries
        mean_R22 /= 1.0*self.n_tries
        
        delta = sqrt(1./self.n_tries*( mean_R22 - mean_R2**2 ))
        
        return mean_R2, delta, delta*1./mean_R2
        
    def genHistogram(self):
        max_dist = max(self.result_dist2)
        max_element = max( [max(self.result_element[i]) for i in range(self.dim)] )#total max in all dimensions
        n_events = len(self.result_dist2)*1.0
            
            
        #print max_dist, self.n_bins
        
        dist_bin, dist_d_bin = linspace(0, max_dist, self.n_bins, retstep=True)
        element_bin, element_d_bin = linspace(-max_element, max_element, self.n_bins, retstep=True)
        
        dist_hist = histogram(self.result_dist2, dist_bin)[0] / n_events
        
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
        
        
    def plot(self):
        """
        plots the results
        """
        #print 'plot:', self.dist_bin[:-1],self.dist_hist
        
        pl.figure()
        pl.subplot(1,1,1)
        pl.bar(self.dist_bin[:-1],self.dist_hist, width=self.dist_d_bin)
        
        pl.show()
            
        

def main():
    n_tries = 500
    n_steps = range(10,41,2)
    plotting = False
    
    res_R2 = []
    res_d = []
    res_p = []
    
    for N in n_steps:
        rndwk1 = sarw(1, N, n_tries)
        r2, d, p = rndwk1.nWalks()
        res_R2.append(r2)
        res_d.append(d)
        res_p.append(p)
        print 'N=%3.0f, <R2>=%7.2f, delta=%5.2f, error=%4.1f%%' % (N, r2, d, p*100)

    if plotting == True:
        pl.figure()
        pl.subplot(3,1,1)
        pl.plot(n_steps, res_R2)
        pl.title('<R^2> vs n_{steps}')
        pl.subplot(3,1,2)
        pl.plot(n_steps, res_d)
        pl.title('\delta vs n_{steps}')
        pl.subplot(3,1,3)
        pl.plot(n_steps, res_p)
        pl.title('error vs n_{steps}')
        pl.show()

        


        
def cmdmain(*args):
    try:
        main()
    except:
        raise
        # handle some exceptions
    else:
        return 0 # exit errorlessly     
        

def classmain():
    print '''instance the class sarw and call it to do everything and return
mean_R2 and delta.
   
>>> sarndwk = sarw(steplength=1, n_steps = 10, n_tries=5000)
>>> sarndwk()
'''
    

        
if __name__ == '__main__':
    sys.exit(cmdmain(*sys.argv))
else:
    classmain()