#include "latticeview.h"

#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sstream>
#include <time.h>

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
int * convertLat(int* lat, int dim);

int main(void)
{
    const int dim = getNr(string("\n\nInput Dimension N for Task 1 and 2:\n"
                                 "  (make sure your console can disply 2*N columns and\n"
                                 "   N rows in order for the graphic output to work properly)\n   N = "));
    float p = getNr(string("Input population probability:\n"
                           "  (in decimals, NOT procents)\n   p = "));

    // ------------------------------------------------
    // T A S K 1
    // ------------------------------------------------
    // generate the output for task one

    // generate a lattice
    //cout << "before init loop"<<endl;

    int * lat;
    lat = genLat(dim, p, 1);

    //cout << "after printing"<<endl;
    cout << "\n T A S K    1 :\nGenerated lattice: (will be saved as task1.ppm)\n";
    printLatticeBW(lat, dim); //screen output
    Print_lattice(convertLat(lat, dim), dim, dim, 500, 500, "task1.ppm"); //file output

    // ------------------------------------------------
    // T A S K 2
    // ------------------------------------------------
    //do the forest fire simulation once with nice graphic animated output

    int * lifetime_fire = new int();
    int * shortest_path = new int();

    cout << "\n...Starting animation Forest Fire (Task 2):"<<endl;
    wait(3000);

    forestfire(lat, dim, true, lifetime_fire, shortest_path);

    wait(1000); for(int i=0;i<40;i++)cout<<endl;

    cout << "\n\n T A S K    2 :\nGenerated lattice: (will be saved as task2.ppm)\n";
    Print_lattice(convertLat(lat, dim), dim, dim, 500, 500, "task2.ppm"); //file output
    printLatticeColor(lat, dim);

    cout << "\nRESULTS: life time: "<< *lifetime_fire<<" ; minimal path length: "<<*shortest_path<<endl;

    //clean up memory
    delete[] lat;
    delete lifetime_fire, shortest_path;


    // ------------------------------------------------
    // T A S K 3
    // ------------------------------------------------
    // crack the numbers, do the stats

    //int * res;// = new * int[2];
    //res = new int[2];
    //res[0]=-1; res[1] = -1;
    //measure(40, 0.8, 1, res);
    //cout << "r0 "<<res[0]<<"  r1 "<<res[1]<<endl;


    int n_trials = 1000;
    float p_step = 0.02;
    string filename = "task3.dat";

    cout << "\n\n T A S K    3 :\n...starting calculations: (results will be saved in "<<filename<<")\n";

    ofstream myfile;
    myfile.open (filename.c_str());
    myfile << "dim" << "; "<<"p" << "; "<< "ave_time"<< "; "<< "ave_time/dim"<< "; "<< "ave_path" << "; "<< "ave_path/dim"<< "; "<<"frac_perc" <<"; "<< "cnt_perc"<<"; "<< "n_trials" << "\n";

    if (true) //for debugging
    {
        cout<<endl;
        int c = 0;
        for (int dim = 10; dim <= 40; dim+=5)
        {
            cout << " ... Calculating all p for Dim = "<<dim<<endl;
            for (float p = 0; p <= 1; p+=p_step)
            {
                int cnt_perc = 0; // counts the number of percolative clusters
                float ave_path = 0.0; // only takes average over those samples that have a shortest path
                float ave_time = 0.0;
                for(int i = 0; i<n_trials; ++i)
                {
                    int * res;// = new * int[2];
                    res = new int[2];
                    measure(dim, p, i, res);
                    if (res[1] > 0)
                    {
                        cnt_perc++;
                        ave_path += res[1];
                    }
                    ave_time += res[0];
                    //cout << "    r0:" << res[0] << "; r1:" << res[1]  << "; t:" <<ave_time<<"; p:"<<ave_path <<"; cnt:"<< cnt_perc<< endl;
                    delete[] res;
                }
                if (cnt_perc>0) ave_path /= cnt_perc;
                else ave_path = 0;
                ave_time /= (float)n_trials;
                float frac_perc = cnt_perc / (float)n_trials;
                float ave_time_pd = ave_time / (float)dim;
                float ave_path_pd = ave_path / (float)dim;
                //cout << dim << "; "<<p   << "; t: "<< ave_time<< "; p: "<< ave_path<< " frac: "<<frac_perc <<"; cnt: "<< cnt_perc<<"; nrun: "<< n_trials << endl;
                myfile << dim << "; "<<p << "; "<< ave_time<< "; "<< ave_time_pd<< "; "<< ave_path << "; "<< ave_path_pd<< "; "<<frac_perc <<"; "<< cnt_perc<<"; "<< n_trials << "\n";
            }
        }
    }

    myfile.close();

    return 0;
}

int * convertLat(int * lat, int dim)
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
    srand48(seed);
    int * lat = new int[_DIM*_DIM];
    for (int i=0; i<_DIM; ++i)
    {
        for (int j = 0; j<_DIM; ++j)
        {
            if (drand48() < p)
                lat[i+_DIM*j] = tree;
            else
                lat[i+_DIM*j] = empty;
        }
     }
    return lat;
}



float getNr(string text) {
    //cout << "getting input";
    // safe version vor getting int input, source: http://www.cplusplus.com/forum/articles/6046/
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
