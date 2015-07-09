#include <stdio.h>
#include <stdlib.h>

#include "bbobStructures.h"
#include "benchmarksdeclare.h"
#include "benchmarks.h"

int main(int argc, char **argv)
{

	int i,j;
	FILE *out;
	TwoDoubles res;
	isInitDone = 0;
	trialid = 3;

	out = fopen("res_data", "w");

	DIM = argc - 1;
	double *X = (double*)malloc(DIM*sizeof(double));

	for(i = 0; i < DIM; i++){
		X[i] = atof(argv[i+1]);
		//printf("%e ", X[i]);
	}
	//printf("\n");

	initbenchmarks();
	initbenchmarkshelper();
	res = f24(X);

	//printf("Res is %lf\n", res.Fval);
	fprintf(out,"%e\n",res.Fval);

	fclose(out);

  	return 0;	
}
