#!/usr/bin/env python
"""\
 ising.py - Play with the Ising model
"""

from math import exp
from random import randrange,choice,random
from numpy import zeros,int
import matplotlib as mp
import pylab as pl

def init_ising_lattice(n):
    lattice = zeros((n,n),int)
    options = [-1,1]
    for i in range(n):
        for j in range(n):
            lattice[i,j] = choice(options)
    return lattice

def energydiff(S0,Sn,J,B): return 2*S0*(B+J*Sn)

def ising(n=200,nsteps=500000,B=0,J=1):
    lattice = init_ising_lattice(n)
    energy = 0
    energies = []
    for step in range(nsteps):
        i = randrange(n)
        j = randrange(n)
        Sn = lattice[(i-1)%n,j]+lattice[(i+1)%n,j]+\
             lattice[i,(j-1)%n]+lattice[i,(j+1)%n]
        dE = energydiff(lattice[i,j],Sn,J,B)
        if dE < 0 or random() < exp(-dE):
            lattice[i,j] = -lattice[i,j]
            energy += dE
            energies.append(energy)
    return lattice,energies

def pil_image(lattice,fname="bs.png"):
    #import Image, ImageDraw
    #n,m = lattice.shape
    #img = Image.new("RGB",(m,n),(255,255,255))
    #draw = ImageDraw.Draw(img)

    #for i in range(n):
    #    for j in range(m):
    #        if lattice[i,j] > 0: draw.point((i,j),(0,0,0))
    #img.save(fname,"PNG")
    return
    

def main():
    import sys,getopt
    opts,args = getopt.getopt(sys.argv[1:],'n:s:b:j:')
    n = 200
    nsteps = 500000
    B = 0
    J = 1
    for key,val in opts:
        if key == '-n': n = int(val)
        elif key == '-s': nsteps = int(val)
        elif key == '-b': B = float(val)
        elif key == '-j': J = float(val)
    lattice,energies = ising(n,nsteps,B,J)
    pil_image(lattice)

    pl.plot(energies)
    pl.show()
    return

def plot(energies):
    from Gnuplot import Gnuplot, Data
    p = Gnuplot()
    d = Data(range(len(energies)),energies)
    p.plot(d)
    return

if __name__ == '__main__': main()