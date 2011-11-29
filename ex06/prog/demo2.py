try:
    from numpy import *
except:
    from Numeric import *
    
from pylab import *
from random import random

hold(False)

class IsingModel:
    """
    
        http://pygments.org/demo/811/
    	TITLE
	Description
   
	Methods:
	-----------------------------------------------------------------------------------------
	Randomizer()
	: Randomizes the lattice created during ___init___ with -1's and 1's.
	
	getHamiltonian()
	: Loops over the entire lattice and calculates the total energy. 
	  Periodic boundary conditions are included in the calculation.

	Prob()
	: Returns the probability that a value deltaE > 0 should be accepted.
	  The probabillity is originally calculated during __init__

	Step(steps,equilibrated=0)
	: Flips a random spin in the lattice and calculates the change in energy.
	  The change is accepted if it is negative. If it's positive, it's accepted 
	  with a probabillity Prob(deltaE).
	  
   	  If equilibrated is set at 1, then the total energy, magnetic susceptibility and
	  total magnetization is appended to the according lists created in __init__

	Solver(steps)
	: Loops over different temperature values while calculating and returning the heat
	  capacity, magnetic susceptibility and total magnetization. Start with a new system
	  at each temperature.

	SingleSolver(steps)
	: Loops over different temperature values while calculating and returning the heat
	  capacity, magnetic susceptibility and total magnetization. Unlike the Solver() this
	  function will use the final lattice from the previous loop as equilibrium point -
	  saving a lot of calculations.

	PlotProperties(steps)
	: Utilizes Solver() and plots the results to files.

	-----------------------------------------------------------------------------------------
    """

    def __init__(self, J=1, T=3, nx=20, ny=20, d=2, B=0):
        self.nx        = nx			      #	Lattice dimension			
        self.ny        = ny			      # Lattice dimension
        self.J         = float(J)		      # Spin interaction force
        self.T         = float(T)		      # System temperature
        self.Q         = J/T			      # A constant Q used throughout the simulation
        self.lattice   = zeros([self.nx,self.ny])     # Create lattice of 0's    
        self.lattice   = self.randomizer()            # Randomize lattice
        self.Energy    = self.getHamiltonian()        # Get start energy
        self.ProbArray = exp(-array([4,8]) * self.Q)  # Probabilities for deltaE > 0
        self.Elist     = []                           # List for energies         
        self.Xlist     = []			      # List for susceptibility
	self.Mlist     = []                           # List for total magnetization       
        

    def randomizer(self):
        for i in range(self.nx):
            for j in range(self.ny):
                self.lattice[i][j] = 2*int(round(random()))-1;
        return self.lattice

    
    def getHamiltonian(self):
        H = 0;
        for i in range(self.nx):
            for j in range(self.ny):
               H += self.lattice[i][j]*self.lattice[i-1][j] + \
                    self.lattice[i][j]*self.lattice[i][j-1] 	# Spin interaction taking periodic
	return -self.J * H				    	# boundary conditions into account.	
        

    
    def Prob(self,deltaE):
        if (deltaE == 4):
            return self.ProbArray[0]
        elif (deltaE == 8):
            return self.ProbArray[1]
    
        
    def step(self, steps=100000, equlibrated=0):
        for k in range(steps):
            i = int(round(self.nx*random()-0.5))
            j = int(round(self.ny*random()-0.5))
            self.lattice[i][j] *= -1
            deltaE = -(self.lattice[i-(self.nx-1)][j] + \
                      self.lattice[i][j-(self.ny-1)]  + \
                      self.lattice[i-1][j]            + \
                      self.lattice[i][j-1])           * \
                      self.lattice[i][j]              * 2	 			# Interaction sum for changing one spin
            
            if ((deltaE*self.J <= 0) or (self.Prob(deltaE) > random())):
                self.Energy += deltaE * self.J		  				# Accept step
            else:
                self.lattice[i][j] *= -1						# Reject spin flip; return to original configuration
    	    
	    if (equlibrated == 1):
		self.Elist.append(self.Energy)						# Append total energy to list
               	self.Xlist.append(float(sum(sum(self.lattice)))/(self.nx*self.ny))	# Append magnetization to list



    def Solver(self, steps=100000):
        CvValues = []			# Contain the values of heat capacity at different T's
	XValues  = []			# Contain the values of magnetic susceptibility
	MValues  = []			# Contain the values of total magnetization
	Index    = 0			# Loop index

        Trange = arange(0.1,self.T,0.1)	# Temperature range to loop through

        for i in Trange:
            self.__init__(self.J,i)
            self.step()
	    self.step(steps,1)

	    ## Calculate total magnetization
	    M = average(array(self.Xlist))
	    
	    if (Index != 0):
		while (abs(M) < 0.7*abs(MValues[-1])):	
		    self.__init__(self.J,i)
		    self.step(); self.step(steps,1)
		    M = average(array(self.Xlist))

	    ## Calculate value of heat capacity
            E2 = average(array(self.Elist)**2)                       
            E = average(array(self.Elist))**2                        
            Cv = 1.0/((self.nx*self.ny))*((self.J/i)**2)*(E2-E)  
            CvValues.append(Cv)
	    
	    ## Calculate magnetic susceptibility
            X = average(array(self.Xlist))**2
            X2 = average(array(self.Xlist)**2)
            X = (self.J*(X2-X))/i
            XValues.append(X)
	    
	    Index += 1
	    MValues.append(M)
            print 'Total Magnetization appended:', M,' at T = ',i, 'E:', average(array(self.Elist))
        return (Trange,CvValues,XValues,MValues)



    def SingleSolver(self, steps=100000):
        CvValues 	= []
	XValues  	= []
	MValues  	= []
	Index    	= 0
	LatticeStorage  = 0
	Trange 		= arange(0.1,self.T,0.025)

        for i in Trange:
            self.__init__(self.J,i)

	    if (Index == 0):
		self.step()			## Equilibrate the lattice
	    else:
		self.lattice = LatticeStorage	## Use previous lattice as equilibrium point

	    self.step(steps,1)			## Do equilibrium steps

	    ## Calculate total magnetization
	    M = average(array(self.Xlist))

	    ## Calculate value of heat capacity
            E2 = average(array(self.Elist)**2)                       
            E = average(array(self.Elist))**2                        
            Cv = 1.0/((self.nx*self.ny))*((self.J/i)**2)*(E2-E)  
            CvValues.append(Cv)
	    
	    ## Calculate magnetic susceptibility
            X = average(array(self.Xlist))**2
            X2 = average(array(self.Xlist)**2)
            X = (self.J*(X2-X))/i
            XValues.append(X)
	    
	    Index += 1
	    LatticeStorage = self.lattice
	    MValues.append(abs(M))
            print 'Total Magnetization appended:', abs(M),' at T = ',i
        return (Trange,CvValues,XValues,MValues)

	

    def PlotProperties(self, steps=100000):
	P = self.Solver(steps)
	Titles = ['HeatCapacity','MagneticSusceptibility','TotalMagnetization']
	for i in range(len(P)-1):
		plot(P[0],P[i+1],'ro')
		savefig('Total300000_%s.png' % (Titles[i]))
        
       
geo = IsingModel();   
geo.PlotProperties()