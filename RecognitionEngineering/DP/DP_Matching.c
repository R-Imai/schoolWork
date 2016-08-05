/*------------------------------------------------*/
//  Name:		DP_Matching.c
//	Author:		R.Imai
//	Created:	2016 / 06 / 09
//	Last Date:	2016 / 06 / 09
//	Note:
/*------------------------------------------------*/
#include <stdio.h>
#include <math.h>
#include <dirent.h>
#include <string.h>

#define slantCoe 2

struct melCepst{
    char label[20];
    int length;
    float data[150][15];
};
struct people{
    struct melCepst mel[100];
};

struct melCepst import(char *path, int num){
    FILE *fp;
    int j;
    char ff[20];
    char fname[30];
    struct melCepst peo;
    sprintf(fname,"data/%s/%s_%03d.txt",path,path,num);
    fp = fopen(fname, "r");
    fscanf(fp,"%s",ff);
    fscanf(fp, "%s", peo.label);
    fscanf(fp, "%d", &peo.length);
    j = 0;
    while (fscanf(fp, "%f %f %f %f %f %f %f %f %f %f %f %f %f %f %f", &peo.data[j][0],&peo.data[j][1],&peo.data[j][2],&peo.data[j][3],&peo.data[j][4],&peo.data[j][5],&peo.data[j][6],&peo.data[j][7],&peo.data[j][8],&peo.data[j][9],&peo.data[j][10],&peo.data[j][11],&peo.data[j][12],&peo.data[j][13],&peo.data[j][14]) != EOF){
        j += 1;
    }
    fclose(fp);


    return peo;
}

float dist(float a[15], float b[15]){
    float sum = 0;
    int i;
    for(i = 0; i < 15; i++){
        sum += (a[i] - b[i])*(a[i] - b[i]);
    }
    sum = sqrtf(sum);
    return sum;
}

float DP_length(struct melCepst data1, struct melCepst data2){
    float mat[150][150];
    float cost[150][150];
    float distance;
    int i, j;
    float calcSpace[3];
    for(i = 0; i < data1.length; i++){
        for(j = 0; j < data2.length; j++){
            mat[i][j] = dist(data1.data[i], data2.data[j]);
        }
    }
    cost[0][0] = mat[0][0];
    for(i = 1; i < data1.length; i++){
        cost[i][0] = cost[i - 1][0] + mat[i][0];
    }
    for(j = 1; j < data2.length; j++){
        cost[0][j] = cost[0][j - 1] + mat[0][j];
    }
    for(i = 1; i < data1.length; i++){
        for(j = 1; j < data2.length; j++){
            calcSpace[0] = cost[i - 1][j] + mat[i][j];
            calcSpace[1] = cost[i - 1][j - 1] + slantCoe*mat[i][j];
            calcSpace[2] = cost[i][j - 1] + mat[i][j];
            cost[i][j] = fminf(calcSpace[0], fminf(calcSpace[1], calcSpace[2]));
        }
    }
    distance = cost[data1.length - 1][data2.length - 1]/(float)(data1.length + data2.length);
    return distance;
}


int main(int argc, char *argv[]){
    struct melCepst data[2];
    float minDist, dist;
    char dirName[4][8];
    char labelA[20], labelB[20];
    int i, j, k, l, match;
    int matchMat[4][4];
    float trueLen = 0.0, falseLen = 0.0;
    int trueCnt = 0, falseCnt = 0;
    strcpy(dirName[0], "city011");
    strcpy(dirName[1], "city012");
    strcpy(dirName[2], "city021");
    strcpy(dirName[3], "city022");

    for(k = 0; k < 4; k++){
        for(l = 0; l < 4; l++){
            //printf("%s vs %s\n",dirName[k],dirName[l]);
            //printf("%sで%sを認識\\\\\n",dirName[k],dirName[l]);
            //printf("\\begin{itemize}\n\\setlength{\\parskip}{0cm}\n\\setlength{\\itemsep}{0cm}\n");
            match = 0;
            for(i = 1;i < 101; i++){
                minDist = 99999999.9;
                for(j = 1;j < 101; j++){
                    //printf("%d\n",j);
                    data[0] = import(dirName[k], j);
                    data[1] = import(dirName[l], i);
                    dist = DP_length(data[1], data[0]);
                    if(dist < minDist){
                        minDist = dist;
                        strcpy(labelA, data[0].label);
                        strcpy(labelB, data[1].label);
                    }
                }
                if(strcmp(labelA, labelB) == 0){
                    match += 1;
                    trueLen += dist;
                    trueCnt += 1;
                }else{
                    falseLen += dist;
                    falseCnt += 1;
                    //printf("%s :: %s\n",labelA,labelB);
                }
            }
            matchMat[l][k] = match;
            //printf("\\end{itemize}\n");
            //printf("\t\tmatting rate is %d\n", match);
        }
    }
    printf("\t|%3d|%3d|%3d|%3d|\n", matchMat[0][0],matchMat[0][1],matchMat[0][2],matchMat[0][3]);
    printf("\t|%3d|%3d|%3d|%3d|\n", matchMat[1][0],matchMat[1][1],matchMat[1][2],matchMat[1][3]);
    printf("\t|%3d|%3d|%3d|%3d|\n", matchMat[2][0],matchMat[2][1],matchMat[2][2],matchMat[2][3]);
    printf("\t|%3d|%3d|%3d|%3d|\n", matchMat[3][0],matchMat[3][1],matchMat[3][2],matchMat[3][3]);
    printf("true dist mean: %f",trueLen/trueCnt);
    printf("false dist mean: %f",falseLen/falseCnt);


}
