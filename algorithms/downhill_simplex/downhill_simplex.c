#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <math.h>

int NDIM;                    //number of dimensions
int NUM_SIM; 
int UPDATE;                  //update sigal
int NMAX;                    //maximum of iterations
FILE *FP_Log;                //log file pointer
char benchmark_path[200];    //benchmark path
char benchmark_case[40];     //benchmark executable file
char benchmark_res[40];      //benchmark result file
double **RANGE_Paras;        //paramers range matrix
double **INIT_Paras;         //parameter initial matrix
double *INIT_Metrics;        //initial results
double **Paras;              //intime parameters matrix
double *Metrics;             //intime metrics matrix
double *PARAS_Sum;           //sum of parameters of each simplex

void downhill_simplex();
void read_config();
void read_init();
void update_status();
void get_paras_sum();
double update_simplex(int, double);
void check_paras_band(double *);
double get_metrics(double *);
void update_log(int, const char *);

int
main(int argn, char **argv)
{
    read_config();
	downhill_simplex();
	return 0;
}

void
read_config()
{
    int i, j;
    FILE *fp_init;
    time_t now;
    struct tm *timenow;
    char log_name[40];


    if(!(fp_init = fopen("downhill_config", "r"))){
        printf("downhill_config file does not exsit!\n");
        exit(1);
    }


    //read max iterator
    fscanf(fp_init, "%d", &NMAX);

    //read parameters dimension
    fscanf(fp_init, "%d", &NDIM);

    //read benchmark configuration
    fscanf(fp_init, "%s", &benchmark_path);
    fscanf(fp_init, "%s", &benchmark_case);
    fscanf(fp_init, "%s", &benchmark_res);
    //printf("%s\n", benchmark_path);
    //printf("%s\n", benchmark_case);
    //printf("%s\n", benchmark_res);

    //allocate parameters range and intinial values
    RANGE_Paras  = (double **)malloc(NDIM * sizeof(double *));
    INIT_Paras   = (double **)malloc((NDIM + 1) * sizeof(double *));
    Paras        = (double **)malloc((NDIM + 1) * sizeof(double *));
    INIT_Metrics = (double *)malloc((NDIM + 1) * sizeof(double));
    Metrics      = (double *)malloc((NDIM + 1) * sizeof(double));
    PARAS_Sum    = (double *)malloc(NDIM * sizeof(double));

    for(i = 0; i < NDIM; i++){
        RANGE_Paras[i] = (double *)malloc(2 * sizeof(double));
    }
    for(i = 0; i < NDIM + 1; i++){
        INIT_Paras[i] = (double *)malloc((NDIM) * sizeof(double));
        Paras[i]      = (double *)malloc((NDIM) * sizeof(double));
    } 

    fclose(fp_init);

    //init log
    time(&now);
    timenow = localtime(&now);
    sprintf(log_name, "simplex_log_%d.%d.%d-%d.%d.%d", timenow->tm_year+1900, \
            timenow->tm_mon, timenow->tm_mday, timenow->tm_hour, timenow->tm_min,\
            timenow->tm_sec);
    FP_Log  = fopen(log_name, "aw");
    fprintf(FP_Log,"iterator+action+parameters+metrics\n");

    NUM_SIM = NDIM + 1;   
}


void 
downhill_simplex()
{	
	int iterator;
    double rel_met;
    double ihi_save;
    int i, ihi, ilo, inhi, j, nfunk;


    //read_config();

    //if(UPDATE == 1){
    //    update_status();
    //}

	//begin iterate
	iterator = 0;
    while(iterator < NMAX)
	{
        //read downhill configuration
        read_init();

        //open update
        if(UPDATE == 1){
            update_status();
        }

        get_paras_sum();

		// find the highest, the next highest and the lowest points
        ilo  = 0;
        ihi  = 0;
        inhi = 0;
	    for(i = 0; i < NUM_SIM; i++){
            //printf("%e\n", Metrics[i]);
            if(Metrics[i] <= Metrics[ilo]){
                ilo = i;
            }
            if(Metrics[i] > Metrics[ihi]){
                ihi = i;
            }
        }
        for(i = 0; i < NUM_SIM; i++){
            if(Metrics[i] > Metrics[inhi] && i != ihi){
                inhi = i;
            }
        }

    

        //reflect the worst simplex, -1.0 = reflect
        rel_met = update_simplex(ihi, -1.0);
        iterator++;

        //expand the reflect point
        if(rel_met <= Metrics[ilo]){
            rel_met = update_simplex(ihi, 2.0);
            iterator++;
            update_log(iterator, "expand");
        }
        //shrink the reflect point
        else if(rel_met >= Metrics[inhi]){
            ihi_save = Metrics[ihi];
            rel_met = update_simplex(ihi, 0.5);
            iterator++;
            update_log(iterator, "shrink");

            //Can’t seem to get rid of that high point. Better contract around the best point.    
            if(rel_met >= ihi_save){
                for(i = 0; i < NDIM + 1; i++){
                    if(i != ilo){
                        for(j = 0; j < NDIM; j++){
                            Paras[i][j] = 0.5 * (Paras[i][j] + Paras[ilo][j]);
                        }
                        check_paras_band(Paras[i]);
                        Metrics[i] = get_metrics(Paras[i]);
                        iterator++;
                        update_log(iterator, "all_shrink");
                    }
                }
            }
        }
        //else keep the reflect point
        else{
            update_log(iterator, "keep");
        }
    }
	
	fclose(FP_Log);
}

void 
read_init()
{
    int i, j;
    FILE *fp_config;

    if(!(fp_config = fopen("subrange", "r"))){
        printf("%s: downhill_config file does not exsit!\n", __func__);
        exit(1);
    }

    //read update signal
    fscanf(fp_config,"%d", &UPDATE);

    //read parameters range and initial valuse
    for(i = 0; i < NDIM; i++){
        for(j = 0; j < 2; j++){
            fscanf(fp_config, "%lf", &RANGE_Paras[i][j]);
            //printf("%e ", RANGE_Paras[i][j]);
        }
        //printf("\n");
    }
    //printf("\n");
    for(i = 0; i < NDIM + 1; i++){
        for(j = 0; j < NDIM; j++){
            	fscanf(fp_config, "%lf", &INIT_Paras[i][j]);
            	//printf("%e ", INIT_Paras[i][j]);
        }
        //printf("\n");
    }

    for(i = 0; i < NDIM + 1; i++){
        INIT_Metrics[i] = get_metrics(INIT_Paras[i]);
    }

    fclose(fp_config);
}

void
update_status(){
    //memcpy((void *)Paras, (void *)INIT_Paras, (NDIM + 1) * NDIM * sizeof(double));
    //memcpy((void *)Metrics, (void *)INIT_Metrics, (NDIM + 1) * sizeof(double));
    //printf("%e\n", Metrics[0]);
    int i, j;

    //reset parameters and metrics by configuration file
    for(i = 0; i < NDIM + 1; i++){
        for(j = 0; j < NDIM + 1; j++){
            if(j != NDIM){
                Paras[i][j] = INIT_Paras[i][j];
            }
            else{
                Metrics[i] = INIT_Metrics[i];
            }
        }
    }

    //reset update of configure file is 0
    system("sed -i '' '1s/1/0/g' subrange");
    //system("sed  '1s/1/0/g' downhill_config");
}

void
get_paras_sum()
{
    int i, j;

    memset(PARAS_Sum, 0, NDIM * sizeof(double));

    for(i = 0; i < NDIM; i++){
        for(j = 0; j < NDIM + 1; j++){
            PARAS_Sum[i] += Paras[j][i];
        }
    }
}

double 
update_simplex(int ihi, double fac)
{
    int i,j;
    double *paras_update;
    double fac1, fac2; 
    double metrics_update;

    paras_update = (double *)malloc(NDIM * sizeof(double));

    fac1 = (1.0 - fac)/NDIM;
    fac2 = fac1 - fac;

    for(i = 0; i < NDIM; i++){
        paras_update[i] = fabs(PARAS_Sum[i]*fac1 - Paras[ihi][i]*fac2);
    }

    check_paras_band(paras_update);
    metrics_update = get_metrics(paras_update);

    //If it’s better than the highest, then replace the highest.
    if(metrics_update < Metrics[ihi]){
        Metrics[ihi] = metrics_update;
        for(i = 0; i < NDIM; i++){
            PARAS_Sum[i] += paras_update[i] - Paras[ihi][i];
            Paras[ihi][i] = paras_update[i];
        }
    }

    free(paras_update);
    return metrics_update;
}

void 
check_paras_band(double* paras_array)
{
    int i;
    for(i = 0; i < NDIM; i++){
        if(paras_array[i] < RANGE_Paras[i][0]){
            paras_array[i] = RANGE_Paras[i][0];
        }
        else if(paras_array[i] > RANGE_Paras[i][1]){
            paras_array[i] = RANGE_Paras[i][1];
        }
    }
}

double 
get_metrics(double * paras_array)
{
    int i;
    double res;
    FILE *fp_res;
    char command[500];
    char res_file[500];

    sprintf(command,  "%s%s", benchmark_path, benchmark_case);
    sprintf(res_file, "%s%s", benchmark_path, benchmark_res);

    for(i = 0; i < NDIM; i++){
        sprintf(command, "%s %e", command, paras_array[i]);
    }

    system(command);

    fp_res = fopen(res_file, "r");
    fscanf(fp_res, "%lf", &res);
    fclose(fp_res);

    //printf("%s: %s\n", command, __func__);
    //printf("%s: %s\n", res_file, __func__);
    return res;
}

void
update_log(int iterator, const char * action)
{
    int i, j;
    fprintf(FP_Log, "%d \t %s\n", iterator, action);
    for(i = 0; i < NDIM + 1; i++){
        for(j = 0; j < NDIM + 1; j++){
            if(j != NDIM){
                fprintf(FP_Log, "%e ", Paras[i][j]);
            }
            else{
                fprintf(FP_Log, ": %e \n", Metrics[i]);
            }
        }
    }
} 
