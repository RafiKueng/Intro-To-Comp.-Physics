#include <iostream>

using namespace std;

int main()
{
	int n = 10000; //no of random numbers
	int c = 16807;
	int p = 2147483647;
	int x = 1;  //seed

	float z0, z1;
    int i=0;

	while (i<n)
	{
 		x = (c*x)%p;
		z0 = (x / (float)p)*2-1;

		x = (c*x)%p;
		z1 = (x / (float)p)*2-1;

		if (z0*z0+z1*z1<=1)
		{
            i++;
            cout << z0 << " " << z1 << " "<< i<<endl;
        }
	}
	return 0;
}
