"""
-------------------------------------------------------------------------------
Hard spheres in a 3d box: Calculating the average distance between particles
-------------------------------------------------------------------------------
Explanation:
    http://www.ifb.ethz.ch/education/IntroductionComPhys/2011-10-25_Ex05.pdf

How this code works:
    

Notes / Convention:

 
-------------------------------------------------------------------------------
Rafael Kueng
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


class ConfigError(Exception):
    def __init__(self):
        #self.value = value
        pass
    def __str__(self):
        #return repr(self.value)
        return 'Could not find a configuration'




def main():
    """
    Solutions to the given tasks will be prepared here

    reminder:
        M: number of runs
        L: edge length of box 
        R: radius of spheres
        N: dimension
        n: number of particles to be placed in the box
    """
   

    
    print '''
    Task 1:
        Vary the number M of confgurations and plot dmean versus the number
        M to check the convergence of the integral.
    '''

    L, R, N, n = [100, 1, 3, 100]
#    M_vec = range(1,50,10)
#    dmean_vec = [dmean(M, L, R, N, n) for M in M_vec]

    M_max = 50
    M_vec=range(1,M_max+1)
    dmean_vec, dm = dmean2(M_max, L, R, N, n)


    f1 = pl.figure()   
    pl.plot(M_vec,dmean_vec)
    pl.title('Task 1: d_mean versus the number of configurations M')
    pl.xlabel('M')
    pl.ylabel('d_mean')



    print '''
    Task 2:
        Vary the number n of particles to check the infuence of the
        dimensionality of the integral on the convergence.
    '''
   
    M, L, R, N = [5, 1000, 1, 1]
    n_vec = range(2,11,1) + range(20,201,20)

    dmean_vec = [dmean(M, L, R, N, n) for n in n_vec]
    
#    print len(M_vec), len(dmean_vec)

    f2 = pl.figure()   
    pl.plot(n_vec,dmean_vec)
    pl.title('Task 2: d_mean versus the number n of particles')
    pl.xlabel('n')
    pl.ylabel('d_mean')


    print '''
    Task 3:
        Choose different volume fractions! What are the highest volume
        fractions you can achieve?
    '''
    M, L, N, n = [5, 500, 3, 50]
    
    R_max = int(np.ceil((L**3*3/(4.*n*np.pi) )**(1./3)))
    R_vec = range(1,R_max+2,2)

    dmean_vec = [dmean(M, L, R, N, n) for R in R_vec]

    volfrac = (n * 4/3.*np.pi*np.array(R_vec)**3) / float(L**3)

    print R_vec
    print R_max    
    
    try:
        id = dmean_vec.index(0.0)
        frc = volfrac[id]
    except ValueError:
        print "no max found "
    else:
        print "Max achieveable volume fraction: ", frc

    f3 = pl.figure()
    pl.plot(volfrac,dmean_vec)
    pl.title('Task 3: d_mean versus the different volume fractions nu')
    pl.xlabel('vol fraction nu')
    pl.ylabel('d_mean')


    pl.show()





def genConfiguration(
    L = 10,   # edge length of box 
    R = 1,      # radius of spheres
    N = 3,      # dimension
    n = 100      # number of particles to be placed in the box
    ):
    """
    gerreates a particulat configuration
    """
    #print 'genConf'
    
    list_of_points = []    
    
    rnd.seed()
    
    # fill the box with spheres, stop then finished or too much tries needed
    cnt = 0 # loop counter
    while True:
        cnt+=1
        if cnt > n * 100:
            #print "did not find a possible solution with",cnt,"tries: aborting"
            #return []
            raise ConfigError()
            
        if len(list_of_points) >= n:
            #print "successfully finished populating the box with spheres"
            break
        
        
        point = np.array([rnd.uniform(0+R,L-R) for x in range(N)], dtype=float)
        
        if volumeCondition(point, list_of_points, R):
            list_of_points.append(point)
    
    
    return list_of_points
    
        
        
        
def volumeCondition(pnt1, list_of_points, radius):
    """
    Checkts, whether the shpere at ptn1 with radius overlaps with any
    of the points in list_of_points
    """
    for pnt2 in list_of_points:
        if (np.sqrt(((pnt1-pnt2)**2).sum())<radius):
            #print 'rejecting...'
            return False
    return True

    
def dkmean(config):
    """
    calculates the d_mean of a given configuration
    d_mean = 2*1 / (n(n-1)) * SUM_(i<j) d_ij
    with d_ij = dist(pi, pj)
    """
    #print 'dkmean'
    sum=0
    n=len(config)

    for j, pj in enumerate(config):
        for i, pi in enumerate(config[0:j]):
            sum+=np.sqrt(((pi-pj)**2).sum())

    return sum * ( 2*1 / float((n*(n-1))) )


def dmean(M, L, R, N, n):
    """
    Creates M configurations k, gets the d^k_mean for each
    and returns the total d_mean, with
    d_mean = 1 / m * SUM_{k=1}^{M} d^k_mean
    """
    print 'd_mean:       (',M, L, R, N, n,')'
    print ''.join(['    [','_'*M,']','\b'*(M+1)]),
    
    dmean = 0
    for i in range(M):
        sys.stdout.write('*')
        try:        
            config = genConfiguration(L, R, N, n)
        except ConfigError:
            print '\n    ABORT: could not find a configuration...\n'
            return 0
        else:
            dmean += dkmean(config)
            
    print '\n'
    return dmean / float(M)
        

def dmean2(M, L, R, N, n):
    """
    Creates M configurations k, gets the d^k_mean for each
    and returns the total d_mean, with
    d_mean = 1 / m * SUM_{k=1}^{M} d^k_mean
    and a list with d_mean for all configs k, with k = 1 ... M
    """
    print 'Dmean:       (',M, L, R, N, n,')'
    print ''.join(['    [','_'*M,']','\b'*(M+1)]),
    
    dmean = 0
    dmeanlist = []
    for i in range(M):
        sys.stdout.write('*')
        try:        
            config = genConfiguration(L, R, N, n)
        except ConfigError:
            print '\n    ABORT: could not find a configuration...\n'
            return 0
        else:
            dmean += dkmean(config)
            dmeanlist.append(dmean/float(i+1))
            
    print '\n'
    
    return dmeanlist, dmean / float(M)



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