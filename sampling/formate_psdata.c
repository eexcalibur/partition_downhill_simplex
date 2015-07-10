#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#define num_sampling 810
#define num_para 3
#define num_var 1

int main(int argc, char **argv)
{
	FILE *sa_fp, *para_fp, *var_fp;
	double para;
	double variable;

	sa_fp=fopen("sa_data", "wr");
	para_fp=fopen("paras", "r");
	var_fp=fopen(argv[1], "r");
	
	fprintf(sa_fp,"PSUADE_IO (Note : inputs not true inputs if pdf ~=U)\n");
	fprintf(sa_fp, "%d %d %d\n", num_para, num_var, num_sampling);
	for(int i=1; i <= num_sampling; i++)
	{
		fprintf(sa_fp, "%d %d\n", i, num_var);
		for(int j=1; j <= num_para; j++)
		{
			fscanf(para_fp, "%lf ", &para);
			fprintf(sa_fp, "  %1.16e\n", para);
		}
        fscanf(var_fp, "%lf ", &variable);
        fprintf(sa_fp, "  %1.16e\n", variable);
	}
	
	fprintf(sa_fp,"PSUADE_IO  \n \
PSUADE  \n \
INPUT  \n \
   dimension = 3  \n \
   variable 1 H  =   4.0000000000000000e+01   6.0000000000000000e+01  \n \
   variable 2 M  =   6.7000000000000000e+01   7.4000000000000000e+01  \n \
   variable 3 sig  =   2.0000000000000000e+01   4.0000000000000000e+01  \n \
END  \n \
OUTPUT  \n \
   dimension = 1  \n \
   variable 1 Y1  \n \
END  \n \
METHOD  \n \
   sampling = MC  \n \
#  sampling = FACT  \n \
#  sampling = LH  \n \
#  sampling = OA  \n \
#  sampling = OALH  \n \
#  sampling = MOAT  \n \
#  sampling = SOBOL  \n \
#  sampling = LPTAU  \n \
#  sampling = METIS  \n \
#  sampling = FAST  \n \
#  sampling = BBD  \n \
#  sampling = PBD  \n \
#  sampling = FF4  \n \
#  sampling = FF5  \n \
#  sampling = CCI4  \n \
#  sampling = CCI5  \n \
#  sampling = CCIF  \n \
#  sampling = CCF4  \n \
#  sampling = CCF5  \n \
#  sampling = CCFF  \n \
#  sampling = CCC4  \n \
#  sampling = CCC5  \n \
#  sampling = CCCF  \n \
#  sampling = SFAST  \n \
#  sampling = UMETIS  \n \
#  sampling = GMOAT  \n \
#  sampling = GMETIS  \n \
#  sampling = SPARSEGRID  \n \
   num_samples = %d  \n \
   num_replications = 1  \n \
   num_refinements = 0  \n \
   refinement_size = 10000000  \n \
   reference_num_refinements = 0  \n \
#  refinement_type = adaptive  \n \
   randomize  \n \
#  randomize_more  \n \
   random_seed = 41491431  \n \
END  \n \
APPLICATION  \n \
   driver = ./simulator  \n \
   opt_driver = NONE  \n \
   aux_opt_driver = NONE  \n \
#  input_template = NONE  \n \
#  output_template = NONE  \n \
#  max_parallel_jobs = 1  \n \
#  min_job_wait_time = 1  \n \
   max_job_wait_time = 1000000  \n \
#  nondeterministic  \n \
#  launch_only  \n \
#  limited_launch_only  \n \
#  gen_inputfile_only  \n \
#  launch_interval = 1  \n \
#  save_frequency = 1000000  \n \
END  \n \
ANALYSIS  \n \
#  analyzer method = Moment  \n \
#  analyzer method = MainEffect  \n \
#  analyzer method = TwoParamEffect  \n \
#  analyzer method = ANOVA  \n \
#  analyzer method = GLSA  \n \
#  analyzer method = RSFA  \n \
#  analyzer method = MOAT  \n \
#  analyzer method = Sobol  \n \
#  analyzer method = Correlation  \n \
#  analyzer method = Integration  \n \
#  analyzer method = FAST  \n \
#  analyzer method = FF  \n \
#  analyzer method = PCA  \n \
#  analyzer method = ARSM0  \n \
#  analyzer method = FORM  \n \
#  analyzer method = RSMSobol1  \n \
#  analyzer method = RSMSobol2  \n \
#  analyzer method = RSMSobolTSI  \n \
#  analyzer method = Bootstrap  \n \
#  analyzer method = RSMSobolG  \n \
#  analyzer method = ARSMNN  \n \
#  analyzer method = ARSM1  \n \
#  analyzer method = REL  \n \
#  analyzer method = AOPT  \n \
#  analyzer method = GOWER  \n \
#  analyzer method = DELTA  \n \
#  analyzer method = ETA  \n \
#  analyzer method = ARSMG  \n \
   analyzer output_id  = 1  \n \
   analyzer rstype = MARS  \n \
#  analyzer rstype = linear  \n \
#  analyzer rstype = quadratic  \n \
#  analyzer rstype = cubic  \n \
#  analyzer rstype = quartic  \n \
#  analyzer rstype = ANN  \n \
#  analyzer rstype = selective_regression  \n \
#  analyzer rstype = GP1  \n \
#  analyzer rstype = GP2  \n \
#  analyzer rstype = SVM  \n \
#  analyzer rstype = PWL  \n \
#  analyzer rstype = TGP  \n \
#  analyzer rstype = MARSBag  \n \
#  analyzer rstype = EARTH  \n \
#  analyzer rstype = sum_of_trees  \n \
#  analyzer rstype = Legendre  \n \
#  analyzer rstype = user_regression  \n \
#  analyzer rstype = sparse_grid_regression  \n \
#  analyzer regression_wgt_id = -1  \n \
#  graphics  \n \
#  sample_graphics  \n \
   analyzer threshold = 1.000000e+00  \n \
#  analyzer rs_constraint = psData indexFile Lbound Ubound  \n \
#  analyzer moat_constraint = psData indexFile Lbound Ubound  \n \
#  analyzer rs_index_file = indexFile  \n \
#  optimization method = crude  \n \
#  optimization method = txmath  \n \
#  optimization method = appspack  \n \
#  optimization method = minpack  \n \
#  optimization method = cobyla  \n \
#  optimization method = sm  \n \
#  optimization method = mm  \n \
#  optimization method = mm_adaptive  \n \
#  optimization method = bobyqa  \n \
#  optimization method = sce  \n \
#  optimization num_local_minima = 0  \n \
#  optimization use_response_surface  \n \
#  optimization print_level = 0  \n \
#  optimization num_fmin = 0  \n \
#  optimization output_id = 0  \n \
#  optimization max_feval = 10000  \n \
#  optimization deltax = 1.0e-6  \n \
#  optimization fmin = not defined  \n \
#  optimization cutoff = not defined  \n \
#  optimization tolerance = not defined  \n \
   diagnostics 1  \n \
#  file_write matlab  \n \
#  config_file = NONE  \n \
#  use_input_pdfs  \n \
#  constraint_op_and  \n \
#  interactive  \n \
END  \n \
END  \n ", num_sampling);
	
	fclose(sa_fp);
	fclose(para_fp);
	fclose(var_fp);

	return 0;
	
}

