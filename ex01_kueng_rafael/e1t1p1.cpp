#include <iostream>

using namespace std;

int main()
{
	int n = 10000; //no of random numbers
	int c = 3;
	int p = 31;
	int x = 1;  //seed

	float z0, z1;

	for (int i = 0; i<n;i++)
	{
		x = (c*x)%p;
		z0 = x / (float)p;

		x = (c*x)%p;
		z1 = x / (float)p;

		cout << z0 << " " << z1 << endl;
	}
	return 0;
}
