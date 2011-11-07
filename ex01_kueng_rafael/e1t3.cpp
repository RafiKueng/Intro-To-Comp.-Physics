#include <iostream>
#include <stdlib.h>

using namespace std;

#define nBin 10

int main()
{
    //init stuff
    int n = 1000; //no of random numbers

    float bin[nBin];
    int count[nBin];

    for (int i=0;i<nBin;i++)
    {
        bin[i]=0;
        count[i]=0;
    }

    // init fisrt rng
/*    int c = 1017;
	int p = 8191;
	int x = 154;  //seed
*/
    //init 2nd rng
    srand(06707046); //my legi nr

    // init 3rd rng
    int c = 3;
	int p = 31;
	int x = 1;  //seed

	float z0;
	int binNr;

	for (int i = 0; i<n;i++)
	{
		// 1st and 3dr rng
		x = (c*x)%p;
		z0 = x / (float)p;

        //2nd rng
        //z0 = rand() / (float)RAND_MAX;


        binNr = ((int)(z0*nBin))%nBin;

        bin[binNr]+=z0;
        count[binNr]++;
	}

    float npi = n/(float)nBin;
    float chi2 = 0;

    for (int i=0; i<nBin; i++)
    {
        bin[i]/=count[i];
        cout << i << " " << bin[i]<< " " << count[i]<<endl;
        chi2 += (count[i]-npi)*(count[i]-npi)/npi;
    }

    cout <<"np_i: "<<npi<<" chi2: "<<chi2<<endl;
	return 0;
}
