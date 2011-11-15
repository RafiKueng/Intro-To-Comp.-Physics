# -*- coding: utf-8 -*-
"""
-------------------------------------------------------------------------------
Ex07: Diffusion limited aggregation
-------------------------------------------------------------------------------
Explanation:
    Diffusion limited aggregation (DLA) describes the process of aggregating
    particles, forming a cluster, in the case where the single particle
    diffusion is the dominating mechanism. Within this model one starts with
    a seed point (or seed surface). In the following, in each step a particle
    is released from the outside and performs a random walk until it reaches
    the perimeter of the structure, where it is attached to the structure
    (or seed surface). This can be implemented using continuous space or on a
    lattice (for the freezing of ice, a triangular lattice often is used).
    
    
How this code works:
    see:    
    http://www.ifb.ethz.ch/education/IntroductionComPhys/2011-11-08_Ex07.pdf
    

Notes / Convention:
    the grid has its O in the middle, and it stays there, it can grow around
    in + and - direction

    exercise lession notes:


-------------------------------------------------------------------------------
@author: Rafael Kueng
-------------------------------------------------------------------------------

HISTORY:
    v1 2011-11-14   basic implementation
 
BUGS / TODO:


LICENSE:
    none
    
-------------------------------------------------------------------------------
"""

from numpy import array, pi, sqrt, sin, cos
import matplotlib as mp
import random as rnd
import pylab as pl

class cluster(object):
    def __init__():
        pass
    
class abstractGrid(object):
    def __init__():
        pass
        
        
        
class twoDGrid(abstractGrid):
    def __init__():
        pass
    
    
    
    
    
class squareGrid(object):
    def __init__(self, dim):
        self.r_rel = 1.1 # how far away (in terms of r from figure) will the particle be released 
        self.r_esc = 1.5 # how far away (in terms of r from figure) is a particle considered to be escaped

        self.grid = [[1]] #seed in the middle
        self.gridExpand(13)  #init a 19*19 field
        self.npart = 1
        self.step = 0
        self.r = 3 # radius of figure (init to 3)
        self.offset = len(self.grid)//2 #offset for grid element access
        
    def gridExpand(self, n):
        """Expands the grid to all sides by n places"""
        #print self.grid
        n = int(n)
        l = len(self.grid)
        for col in self.grid:
            col[l:] = [0]*n
            col[:0] = [0]*n
        eRow = [0]*(l+2*n)
        #print eRow
        self.grid[l:] = [[0]*(l+2*n) for i in range(n)] #[eRow] * n
        self.grid[:0] = [[0]*(l+2*n) for i in range(n)] #[eRow] * n
        #print self.grid
        
    def printGrid(self):
        
        m = array(self.grid)
        print m
        pl.imshow(m, interpolation='nearest')
        pl.grid(True)
        pl.show()
    
    def __str__(self):
        return array(self.grid).__str__()

    def __repr__(self):
        return array(self.grid).__str__()
    
    def addParticle(self):
        """Try to add one"""
        self.step += 1
        #choose starting pos
        alpha = rnd.random() * 2*pi
        x = int(cos(alpha) * self.r_rel * self.r + 0.5)
        y = int(sin(alpha) * self.r_rel * self.r + 0.5)
        pos = array([x,y])
        
        while True:

            #pos = choice(grid.getNeighbours())
            pos += array(rnd.choice([[-1,0],[+1,0],[0,-1],[0,+1]]))
            dist = self.getDist(pos)
            #print pos, dist, self.r, self.r_esc * self.r

            if  dist > self.r_esc * self.r :
                #print "abort: particle escaped"
                return False

            sum = self.getNeigbourSum(pos)

            if sum > 0:
                self.gridAdd(pos, self.step)
                self.update(pos)
                self.npart += 1
                #print "success:", pos, self.step, self.npart, self.r
                return True
                

    
    def add(self, n=1):
        """Add n for sure"""
        for i in range(n):
            print "adding particle:", i
            while not self.addParticle():
                pass
        #self.grid.__repr__()
            
    def getNeigbourSum(self, pos):
        sum = 0
        for i in [[-1,0],[+1,0],[0,-1],[0,+1]]:
            #print '   ',pos+array(i),self.gridGet(pos+array(i))
            sum += self.gridGet(pos+array(i))
        return sum

            
    def gridAdd(self, pos, val):
        pos_index = pos + array([1,1])*self.offset
        #print 'adding', val, pos, pos_index
        self.grid[pos_index[0]][pos_index[1]] = val

    def gridGet(self, pos):
        pos_index = pos + array([1,1])*self.offset
        #print '   gridget stat:', pos, pos_index, self.r, self.r*self.r_esc, self.getDist(pos)
        return self.grid[pos_index[0]][pos_index[1]]
        
    def getDist(self, pos):
        return sqrt(sum(pos**2))
            #in a perfect world i would use squarred distances to save sqrt's....
    
    def update(self, pos):
        r_new = self.getDist(pos)
        if self.r < r_new:
            #print ' updating r:', self.r, r_new
            self.r = r_new+1 # +1 is small offset, only important for small r
        if len(self.grid)//2 <= self.r*self.r_esc+10:  # +3 for safty
            addcells = 10 #int(r_new*self.r_esc - len(self.grid)//2) *2
            self.gridExpand(addcells) #grow by a healthy amount, so
                    # you dont have to grow all the time, but arent'too big all the time
            self.offset = len(self.grid)//2
            print '   expanding grid to:', len(self.grid)
    
    

def main():
    pass



def cmdmain(*args):
    try:
        main()
        print (
'''
REPORT:


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