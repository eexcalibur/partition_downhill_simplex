#include <math.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
   int    i, nInputs, count;
   double X[100],Y;
   FILE   *fIn  = fopen(argv[1], "r");
   FILE   *fOut, *fsample;

   if (fIn == NULL)
   {
      printf("Simulator ERROR - cannot open in/out files.\n");
      exit(1);
   }

   fscanf(fIn, "%d", &nInputs);
   for (i = 0; i < nInputs; i++) fscanf(fIn, "%lg", &X[i]);

   fsample=fopen("sampling_data", "aw");
   for (i=0; i<nInputs; i++) fprintf(fsample, "%1.6e ", X[i]);
   fprintf(fsample, "\n");

   Y = 0.0;
   fOut = fopen(argv[2], "w");
   fprintf(fOut, " %24.16e\n", Y);
   fclose(fOut);
   fclose(fsample);

   return 0;
}
