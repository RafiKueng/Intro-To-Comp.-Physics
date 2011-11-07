#include <iostream>

using namespace std;

int main()
{
	int n = 10000; //no of random numbers
	int c = 5648;
	int p = 34875;
	int x = 8451;  //seed

	float z0, z1, z2;

	for (int i = 0; i<n;i++)
	{
        x = (c*x)%p;
        z0 = x / (float)p;

        x = (c*x)%p;
        z1 = x / (float)p;

        x = (c*x)%p;
        z2 = x / (float)p;

        cout << z0 << " " << z1 << " " << z2 << endl;
	}
	return 0;
}
