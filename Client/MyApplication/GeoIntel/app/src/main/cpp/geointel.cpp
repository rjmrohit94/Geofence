//
// Created by jarvis on 8/10/19.
//
#include<unistd.h>
#include <jni.h>
#include<stdio.h>
#include<time.h>
#include<math.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#define NUM_LAYERS 8
#define BATCH_SIZE 1
#define INPUT_SIZE 2
#define TEST_SIZE 20000


/* Error Codes*/
#define FILE_NOT_FOUND 101
#define INVALID_INPUT 102

#define IN 1
#define OUT 0

double y[BATCH_SIZE];


float max_x= 8.58173;
float max_y=76.89261;
float min_x=8.58142;
float min_y=76.89227;
int num_neurons[NUM_LAYERS]={INPUT_SIZE,5,10,10,20,10,4,1};
int point_inside(double lat, double longi)
{
    if (lat > min_x and lat < max_x and longi > min_y and longi < max_y)
        return 1;

    return -1;
}
void convert_lat_long(double *Lat, double *Long)
{
    *Lat=(*Lat- min_x)/(max_x-min_x);
    *Long=(*Long- min_y)/(max_y-min_y);
}
const char* getfield(char* line, int num)
{
    const char* tok;
    for (tok = strtok(line, " ");
         tok && *tok;
         tok = strtok(NULL, " \n"))
    {
        if (!--num)
            return tok;
    }
    return NULL;
}
void readcsvfile(FILE* stream ,int linenumber,int size, double *input[])
{

    char line[1024];
    int i=0,j;
    char* tmp;
    i=linenumber;
    while (i<(linenumber+size))
    {
        fgets(line, 1024, stream);
        for(j=0;j<INPUT_SIZE;j++)
        {
            tmp = strdup(line);
            //printf("  %s", getfield(tmp, j+1));
            sscanf(getfield(tmp,j+1), "%lf", &input[i-linenumber][j]);
            // NOTE strtok clobbers tmp
            free(tmp);
        }
        tmp = strdup(line);
        sscanf(getfield(tmp,INPUT_SIZE+1), "%lf", &y[i-linenumber]);
        //printf(" %lf\n",y[i-linenumber]);
        // NOTE strtok clobbers tmp
        free(tmp);
        i++;
    }

}
int restoreWeights(char *fileName, double **weights[])
{
    FILE* stream = fopen(fileName, "r");
    if (stream == NULL)
    {
        printf("Could not open file %s\n", fileName);
        return FILE_NOT_FOUND;
    }
    int looper,j,k;
    for(looper =0;looper <NUM_LAYERS-1;looper++){
        for(j = 0; j<num_neurons[looper];j++)
        {
            for(k = 0; k<num_neurons[looper+1];k++)
            {
                fscanf(stream,"%lf",&weights[looper][j][k]);
            }
        }
    }
    fclose(stream);
    return  0;
}
void matmul(int rowA,int colA,int rowB,int colB, double *ans[], double *first[], double *second[])
{
    int i,j,k=0;
    if(colA!=rowB)
    {
        printf("Error => colA must be equal to rowB\n");
    }
    for(i=0;i<rowA;i++)
    {
        for(j=0;j<colB;j++)
        {
            *(*(ans+i)+j)=0;
            for(k=0;k<rowB;k++)
            {
                *(*(ans+i)+j) = *(*(ans+i)+j) + (*(*(first+i) + k )) * (*(*(second+k) + j));
            }
        }//j
    }//i
}
int restoreBias(char *fileName, double **bias[])
{
    FILE* stream = fopen(fileName, "r");
    if (stream == NULL)
    {
        printf("Could not open file %s\n", fileName);
        return FILE_NOT_FOUND;
    }
    int looper,j,k,size=0;
    for(looper =0;looper <NUM_LAYERS-1;looper++){
        for(j = 0; j<BATCH_SIZE;j++)
        {
            for(k = 0; k<num_neurons[looper+1];k++)
            {
                fscanf(stream,"%lf \n",&bias[looper][j][k]);
            }
        }
    }
    fclose(stream);
    return  0;
}
void matsum(int row,int col, double *ans[], double *first[], double *second[])
{
    int i,j;
    for(i=0;i<row;i++)
    {
        for(j=0;j<col;j++)
        {
            ans[i][j]=first[i][j]+second[i][j];
        }
    }
}
double sigmoid(double x)
{
    double exp_value;
    double return_value;

    /*** Exponential calculation ***/
    exp_value = exp((double) -x);

    /*** Final sigmoid value ***/
    return_value = 1 / (1 + exp_value);

    return return_value;
}
double Relu(double x)
{
    if (x >= 0)
        return x;
    else
        return 0;
}
double LeakyRelu(double x)
{
    if (x >= 0)
        return x;
    else
        return x / 5;
}
void doublemalloc(double ***var,int row,int col)
{
    int i;
    *var = (double **)malloc(row * sizeof(double *));
    for (i=0; i<row; i++)
    {
        (*var)[i] = (double *)malloc(col * sizeof(double));
    }
}
void doublematsigmoid(int row, int col,double *ans[], double *matrix[])
{
    int i,j;
    for(i=0; i<row; i++)
    {
        for(j=0; j<col; j++)
        {
            ans[i][j]=sigmoid(matrix[i][j]);
        }
    }
}
void doublematrelu(int row, int col,double *ans[], double *matrix[])
{
    int i,j;
    for(i=0; i<row; i++)
    {
        for(j=0; j<col; j++)
        {
            ans[i][j]=Relu(matrix[i][j]);
        }
    }
}
void doublematleakyrelu(int row, int col,double *ans[], double *matrix[])
{
    int i,j;
    for(i=0; i<row; i++)
    {
        for(j=0; j<col; j++)
        {
            ans[i][j]=LeakyRelu(matrix[i][j]);
        }
    }
}

extern "C"
JNIEXPORT jint
JNICALL Java_com_ahio_geointel_GIEngine_calculateFence(JNIEnv *env, jobject, jdouble lat, jdouble longi)
{
    double **weights[NUM_LAYERS-1];
    double **bias[NUM_LAYERS-1];
    double **layer[NUM_LAYERS-1];
    double **output;
    int i,ret;
    for(i=0;i<(NUM_LAYERS-1);i++)
    {
        doublemalloc(&weights[i],num_neurons[i],num_neurons[i+1]);
        doublemalloc(&bias[i],BATCH_SIZE,num_neurons[i+1]);
        doublemalloc(&layer[i],BATCH_SIZE,num_neurons[i]);
    }
    doublemalloc(&output,BATCH_SIZE,1);
    if(restoreWeights("/storage/emulated/0/Download/weights.txt", weights) == FILE_NOT_FOUND){
        return FILE_NOT_FOUND;
    }
    if(restoreBias("/storage/emulated/0/Download/bias.txt", bias) == FILE_NOT_FOUND){
        return  FILE_NOT_FOUND;
    }
    if( lat !=NULL && longi != NULL){
        ret=point_inside(lat,longi);
    }
    else{
        return INVALID_INPUT;
    }
    if(ret<0)
    {
        return OUT;
    }
    else
    {
        convert_lat_long(&lat,&longi);
        layer[0][0][0]= lat;
        layer[0][0][1]= longi;
        for(i=0;i<(NUM_LAYERS-2);i++)
        {
            matmul(BATCH_SIZE,num_neurons[i],num_neurons[i],num_neurons[i+1],layer[i+1],layer[i],weights[i]);
            matsum(BATCH_SIZE,num_neurons[i+1],layer[i+1],layer[i+1],bias[i]);
            doublematrelu(BATCH_SIZE,num_neurons[i+1],layer[i+1],layer[i+1]);
        }
        matmul(BATCH_SIZE,num_neurons[i],num_neurons[i],num_neurons[i+1],output,layer[NUM_LAYERS-2],weights[NUM_LAYERS-2]);
        matsum(BATCH_SIZE,num_neurons[i+1],output,output,bias[NUM_LAYERS-2]);
        doublematsigmoid(BATCH_SIZE,num_neurons[i+1],output,output);
        if(output[0][0]>0.5){
            output[0][0]=1;
            return IN;
        }
        else {
            return OUT;
        }
    }
}