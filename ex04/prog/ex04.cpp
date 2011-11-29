/*
 * Based upon the previous handed in ex02.cpp
 *
 * Rafael Kueng
 */

#include "latticeview.h"

#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sstream>
#include <time.h>
#include <math.h>

using namespace std;

//const int DIM = 40;

#define _sig_tree "\33[42m\33[30m/\\\33[0m"
#define _sig_fire "\33[43m\33[31mWW\33[0m"
#define _sig_ash  "\33[40m\33[71m[]\33[0m"
#define _sig_empty "\33[40m\33[30m  \33[0m"

#define _sig_black "\33[40m\33[37m  \33[0m"
#define _sig_white "\33[47m\33[30m  \33[0m"

// constants
const int empty =  0; // empty dead space
const int tree  =  1; // occupied place by tree
const int fire  =  2; // (or greater) tree on fire
const int ash   = -2; // burnt stuff changes sign to <0

//global var
//int DIM = 0; // will be set by userinput

//functions
int * genLat(const int _DIM, float p, int seed);
float getNr(string text);
int printLatticeColor(int * lat, int dim);
int printLatticeBW(int * lat, int dim);
int printLatticeNr(int * lat, int dim);
int forestfire(int * lat, int dim, bool animate, int * lifetime_fire, int * shortest_path);
void wait(int msec);
void measure(int dim, float p, int seed, int * res);

int * convert4PPM(int* lat, int dim);
int * simplifyLat(int * lat, int dim);
int * findPercolationBurning(int* lat, int dim);
int * deepcopy(int * orglat, int dim);
int * sandbox(int * lat, int dim, int * r, int * d, int step);



int main(void)
{
    const int dim = getNr(string("\n\nInput Dimension N for Task 1 and 2:\n   N = "));
    float p = getNr(string("Input population probability:\n"
                           "  (in decimals, NOT procents)\n   p = "));

    // ------------------------------------------------
    // T A S K 1
    // ------------------------------------------------
    // Fractal dimension of the percolating cluster
		
    // generate a lattice
    //cout << "before init loop"<<endl;

    int * lat;

    // generate clusters until perculating cluster is found or too many tries
    int i = 0;
    int limit_tries = 100;
    do {
      i++;
      if (i>limit_tries)
      {
        cout << "could not find a perculating cluster after "<<i<<" tries.\nABORTING PROGRAM\n\n";
        return 0;
      }
      lat = genLat(dim, p, i);
      lat = findPercolationBurning(lat, dim);
    } while (!lat); // repeat while nullpointer returned...

    cout << "\n T A S K    1 :\nGenerated lattice: (will be saved as task1.ppm)\n";
    //printLatticeBW(lat, dim); //screen output
    Print_lattice(convert4PPM(lat, dim), dim, dim, dim, dim, "task1.ppm"); //file output
    lat = simplifyLat(lat, dim);
    Print_lattice(convert4PPM(lat, dim), dim, dim, dim, dim, "task2.ppm"); //file output
    
    int step = 1;
    int * r = new int[dim/(2*step)];
    int * d = new int[dim/step];
    
    int mid = dim/2;

    for (i = 0; i<dim/(2*step); i++)
    {
      r[i] = i*step;
      d[2*i+0] = mid-i*step;
      d[2*i+1] = mid+i*step;
      //cout << "sandboxing: r:"<<r[i]<<" d1:"<<d[2*i+0]<<" d2:"<<d[2*i+1]<<" mid:"<<mid<<" dim:"<<dim<<" inx:"<<2*i+0<<"\n";
    }

    int * nr = sandbox(lat, dim, r, d, i);
    
    return 0;
}

int * sandbox(int * lat, int dim, int * r, int * d, int nsteps)
{
  string filename1 = "data1.dat";
  string filename2 = "data2.dat";

  int * nr = new int[nsteps];

  float * dlogr = new float[nsteps-1];
  float * dlogM = new float[nsteps-1];
  float * slope = new float[nsteps-1];
	float slopesum = 0;
	int slopen = 0;

  int sum, cnt;

  ofstream myfile1;
  ofstream myfile2;
  myfile1.open (filename1.c_str());
  myfile2.open (filename2.c_str());

  //header, for filewriting
  myfile1 << "r;log{r};M(r);log(M(r));TotFields\n";
  myfile2 << "d log(r);d log(M(r));slope d log(r) / d log(M(r))\n";
  
  for (int i = 1; i<nsteps; i++)
  {
    //cout << "counting round: "<<i<<" d1:"<<d[2*i+0]<<" d2:"<<d[2*i+1]<<" r:"<<r[i]<<" inx: "<<2*i+0<<"\n";
    sum = cnt = 0;
    nr[i] = 0;
    for (int k = d[2*i+0]; k <= d[2*i+1]; k++)
    {
      for (int l = d[2*i+0]; l <= d[2*i+1]; l++)
      {
        cnt++;
        nr[i] += lat[k+dim*l];
        //cout << "   nr: "<<nr[i]<<" lat: "<< lat[k+dim*l]<<" @: ("<< k<<"/"<<l <<"; "<<k+dim*l <<") cnt:"<<cnt<<"\n";
      }
    }
    //cout << "  active: "<< nr[i] << " of " << cnt <<"\n";
    //cout << d[2*i+1]-d[2*i+0]+1 <<";"  << log(d[2*i+1]-d[2*i+0]+1) <<";" << nr[i] << ";"  << log(nr[i]) << ";" << cnt <<"\n";
    //cout << d[2*(i-1)+1]-d[2*(i-1)+0]+1 <<";"  << log(d[2*(i-1)+1]-d[2*(i-1)+0]+1) <<";" << nr[(i-1)] << ";"  << log(nr[(i-1)]) << ";" << cnt <<"\n";    
    //for slope calculation
    if (i>1)
    {
      dlogr[i-1] = log( d[2*(i-1)+1]-d[2*(i-1)+0]+1 ) - log( d[2*i+1]-d[2*i+0]+1 ) ;
      //cout << dlogr[i-1];
      dlogM[i-1] = log(nr[i-1]) - log(nr[i]);
      slope[i-1] = dlogM[i-1] / dlogr[i-1];
      myfile2 << dlogr[i-1] <<";"<< dlogM[i-1] <<";"<< slope[i-1] <<"\n";
			slopesum += slope[i-1];
			slopen++;
    }
    
    // for fileout:
    myfile1 << d[2*i+1]-d[2*i+0]+1 <<";"  << log(d[2*i+1]-d[2*i+0]+1) <<";" << nr[i] << ";"  << log(nr[i]) << ";" << cnt <<"\n";
  }
	cout <<"\nAverage slope: "<<slopesum/slopen<<"\n";
  myfile1.close();
  myfile2.close();
  return nr;
}



int * findPercolationBurning(int * orglat, int dim)
{
  bool foundperc;
  int step_burned, burning, ii;
  int * lat;
	int tmp1, tmp2;
	
	cout << "Checking perculation...\n   ";
  
  for (ii = 0; ii<dim; ++ii)
  {
    //cout << "set field " << ii << " on fire (" << orglat[ii] << ")\n";
		cout<<"\n"<<ii<<"/"<<dim-1<<"|";

		tmp1 = 1;
		tmp2 = 1;
		
		if (ii==0) {tmp1=0; tmp2 = -1;}

    if (orglat[ii] == 1 && orglat[ii-tmp1] != tmp2)
    {
      lat = deepcopy(orglat, dim);
      lat[ii] = 2; // set this field on fire

      // lets see what the fire does...
      int step = 2;

      while (true)
      {
				cout<<".";
				cout.flush();
        step_burned = 0;
        burning = 0;
        for (int i=0; i<dim; ++i)
        {
          for (int j = 0; j<dim; ++j)
          {
            if(lat[i+j*dim] == step)
            {
              burning++;
              //cout << "step " << step << " i,j "<<i<<";"<<j<<endl;
              //check north
              if (i-1>=0 and lat[(i-1)+j*dim]==1) //if exists (real index), is occupied >0 and not burning ==1
              {
                lat[(i-1)+j*dim] = step+1;
                step_burned++;
              }
              //check east
              if (j+1<dim and lat[(i)+(j+1)*dim]==1) //if exists (real index), is occupied >0 and not burning ==1
              {
                lat[(i)+(j+1)*dim] = step+1;
                step_burned++;
              }
              //check south
              if (i+1<dim and lat[(i+1)+j*dim]==1) //if exists (real index), is occupied >0 and not burning ==1
              {
                lat[(i+1)+j*dim] = step+1;
                step_burned++;
              }
              //check west
              if (j-1>=0 and lat[(i)+(j-1)*dim]==1) //if exists (real index), is occupied >0 and not burning ==1
              {
                lat[(i)+(j-1)*dim] = step+1;
                step_burned++;
              }
              //extinguish the fire on this tree
              lat[i+j*dim] *= -1;
            }
          }
        }
        if (burning==0) break;
        step++;

      }
      //cout << "   burning: "<<burning<<"; step: "<<step<<"\n";

      for (int i=0;i<dim;++i)
      {
        //cout <<"num "<<lat[i+dim*(dim-1)]<<"    "<<*shortest_path<< endl;
        if (lat[i+dim*(dim-1)] < 0)
        {
          cout <<"\n\nThis one perculates! (starting place: " << ii << ")\n"; //<<orglat[0]<<";"<<lat[0];
          //delete[] orglat;
          //orglat = lat;
          return lat;
        }
      }
      
      delete[] lat;
    }  
  }
  cout<<"\n\nThis one doesnt perculate\nI'll try again and again, you can press ctrl+c to abort...\n";
	cout.flush();
	wait(1500);
  return 0;
}


int * deepcopy(int * orglat, int dim)
{
  int * nlat = new int[dim*dim];
  for (int i=0; i<dim*dim; ++i)
  {
    nlat[i] = orglat[i];
  }
  return nlat;
}


int * convert4PPM(int * lat, int dim)
{
    int * nlat = new int[dim*dim];
    for (int i=0; i<dim; ++i)
    {
        for (int j = 0; j<dim; ++j)
        {
            //cout << lat[i+dim*j];
            if (lat[i+dim*j]< 0) nlat[i+dim*j] = 3; //ashes = black
            if (lat[i+dim*j]==0) nlat[i+dim*j] = 0; //not occupied = white
            if (lat[i+dim*j]>=2) nlat[i+dim*j] = 2; //burning = red
            if (lat[i+dim*j]==1) nlat[i+dim*j] = 1; //tree = green
            //cout << " >> " << nlat[i+dim*j]<<endl;
        }
     }
    return nlat;
}

int * simplifyLat(int * lat, int dim)
// highlight perculating block, set other stuff to 0
{
    int * nlat = new int[dim*dim];
    for (int i=0; i<dim; ++i)
    {
        for (int j = 0; j<dim; ++j)
        {
            //cout << lat[i+dim*j];
            if (lat[i+dim*j]< 0) nlat[i+dim*j] = 1; // highlight perculating block
            else nlat[i+dim*j] = 0; // other stuff
            //cout << " >> " << nlat[i+dim*j]<<endl;
        }
     }
    return nlat;
}

void measure(int m_dim, float m_p, int m_seed, int * m_res)
{
    int * m_lat;
    m_lat = genLat(m_dim, m_p, m_seed);
    //res[0] = new int();
    //res[1] = new int();
    forestfire(m_lat, m_dim, false, &(m_res[0]), &(m_res[1]));
    //cout << " in msr: r0 "<<m_res[0]<<"  "<<m_res[1]<<endl;
    delete[] m_lat;
}

int forestfire(int * lat, int dim, bool animate, int * lifetime_fire, int * shortest_path)
{
    //cout << "Forestfire"<<endl;
    int i, j; //counters

    //set first row on fire
    for (i = 0; i<dim; ++i)
    {
        lat[i] = lat[i]*2;
    }

    int step = 2;
    int step_burned, burning;
    while (true)
    {
        if (animate)
        {
            //make some free space...
            for (int i = 0; i<40; ++i)
                cout << endl;
            printLatticeColor(lat, dim);
            wait(200);
        }
        step_burned = 0;
        burning = 0;
        for (int i=0; i<dim; ++i)
        {
            for (int j = 0; j<dim; ++j)
            {
                if(lat[i+j*dim] == step)
                {
                    burning++;
                    //cout << "step " << step << " i,j "<<i<<";"<<j<<endl;
                    //check north
                    if (i-1>=0 and lat[(i-1)+j*dim]==1) //if exists (real index), is occupied >0 and not burning ==1
                    {
                        lat[(i-1)+j*dim] = step+1;
                        step_burned++;
                    }
                    //check east
                    if (j+1<dim and lat[(i)+(j+1)*dim]==1) //if exists (real index), is occupied >0 and not burning ==1
                    {
                        lat[(i)+(j+1)*dim] = step+1;
                        step_burned++;
                    }
                    //check south
                    if (i+1<dim and lat[(i+1)+j*dim]==1) //if exists (real index), is occupied >0 and not burning ==1
                    {
                        lat[(i+1)+j*dim] = step+1;
                        step_burned++;
                    }
                    //check west
                    if (j-1>=0 and lat[(i)+(j-1)*dim]==1) //if exists (real index), is occupied >0 and not burning ==1
                    {
                        lat[(i)+(j-1)*dim] = step+1;
                        step_burned++;
                    }
                    //extinguish the fire on this tree
                    lat[i+j*dim] *= -1;
                }
            }
        }
        if (burning==0) break;
        step++;

    }
    //printLatticeNr(lat);
    *shortest_path =  0;
    for (i=0;i<dim;++i)
    {
        //cout <<"num "<<lat[i+dim*(dim-1)]<<"    "<<*shortest_path<< endl;
        if (lat[i+dim*(dim-1)] < 0)
        {
            if (*shortest_path<=0 or -1*lat[i+dim*(dim-1)] < *shortest_path)
            {
                *shortest_path = -1*lat[i+dim*(dim-1)];
            }
        }
    }
    *shortest_path = *shortest_path - 1;
    *lifetime_fire = step - 2;
    //if(animate) cout << "lifetime fire: " << *lifetime_fire <<"; shortest path: "<<*shortest_path<<endl;
    return 0;
}

int * genLat(const int _DIM, float p, int seed=0)
{
    #ifdef WIN32
      srand(  seed );
    #else
      srand48( seed );
    #endif

    double rnd;
    
    int * lat = new int[_DIM*_DIM];
    for (int i=0; i<_DIM; ++i)
    {
        for (int j = 0; j<_DIM; ++j)
        {
          #ifdef WIN32
            rnd = double(rand())/RAND_MAX;
          #else
            rnd = drand48();
          #endif
            if (rnd < p)
                lat[i+_DIM*j] = tree;
            else
                lat[i+_DIM*j] = empty;
        }
     }
    return lat;
}



float getNr(string text) {
    //cout << "getting input";
    // safe version for getting int input, source: http://www.cplusplus.com/forum/articles/6046/
    string input = "";
    float myNumber = 0.0;

    while (true) {
        cout << text;
        getline(cin, input);

        // This code converts from string to number safely.
        stringstream myStream(input);
        if (myStream >> myNumber)
            break;
        cout << "Invalid number, please try again" << endl;
    }
    cout << "You entered: " << myNumber << endl << endl;

    return myNumber;
}


int printLatticeColor(int * lat, int dim)
{
    for (int i=0; i<dim; ++i)
    {
        for (int j = 0; j<dim; ++j)
        {
            if (lat[i+dim*j] == empty)     cout << _sig_empty;
            else if (lat[i+dim*j] == tree) cout << _sig_tree;
            else if (lat[i+dim*j] >= fire) cout << _sig_fire;
            else if (lat[i+dim*j] <= ash)  cout << _sig_ash;
        }
        cout << endl;
    }
    return 0;
}

int printLatticeBW(int * lat, int dim)
{
    for (int i=0; i<dim; ++i)
    {
        for (int j = 0; j<dim; ++j)
        {
            if (lat[i+j*dim]==0)
                {cout << _sig_black;}
            else
                {cout << _sig_white;}
        }
        cout << endl;
    }
    return 0;
}

int printLatticeNr(int * lat, int dim)
{
    int fac;
    //make some free space...
    for (int i = 0; i<20;++i)
    {
        cout << endl;
    }

    for (int i=0; i<dim; ++i)
    {
        for (int j = 0; j<dim; ++j)
        {
            if (lat[i+j*dim]<0) fac = -1;
            else fac=1;
            if (lat[i+j*dim]<10 and lat[i+j*dim]>-10)
                {cout << " " << lat[i+j*dim]*fac;}
            else
                {cout << lat[i+j*dim]*fac;}
            cout << ",";
        }
        cout << endl;
    }
}

void wait(int msec)
{
    clock_t endwait;
    endwait = clock () + (msec * CLOCKS_PER_SEC)/1000 ;
    while (clock() < endwait) {}
}
