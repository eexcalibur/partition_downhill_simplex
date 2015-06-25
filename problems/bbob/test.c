#include <stdio.h>
#include <stdlib.h>

#include "bbobStructures.h"
#include "benchmarksdeclare.h"
#include "benchmarks.h"

int main(int argc, char **argv)
{

	int i,j;
	int num_samples;
	FILE *in, *out;
	TwoDoubles res;
	isInitDone=0;

	in  = fopen("sampling_data", "r");
	out = fopen("res_data", "w");
	fscanf(in, "%d", &num_samples);
	fscanf(in, "%d", &DIM);
	fscanf(in, "%d", &trialid);


	double *X = (double*)malloc(DIM*sizeof(double));

	for(j = 0; j < num_samples; j++){
		for(i = 0; i < DIM; i++){
			fscanf(in, "%lf", &X[i]);
			printf("%lf ", X[i]);
		}
		printf("\n");

		initbenchmarks();
		initbenchmarkshelper();
		res = f17(X);

		printf("Res is %lf\n", res.Fval);
		fprintf(out,"%lf\n",res.Fval);
	}

	fclose(in);
	fclose(out);

  	return 0;	
}
