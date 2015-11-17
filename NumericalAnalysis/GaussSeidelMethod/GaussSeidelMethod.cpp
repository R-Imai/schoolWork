/*--------------------------------------
*	Name:		GaussSeidelMethod.c
*	Author:		R.Imai
*	Created:	2015 / 09 / 30
*	Last Date:	2015 / 10 / 08
*	Note:	ガウス・ザイデル法
*
*-------------------------------------*/

#include<stdio.h>
#include<math.h>

/**
*	DIMENSION:	連立方程式の次数
*	ACCURACY:	収束判定の誤差
*
*	mat:		連立方程式の拡大行列
*	eqation:	移項後の係数群
*	coe:		解
*	wasCoe:		一つ前の解
*	colIndex:	行を入れ替えた際の元の行のインデックス
*/

#define DIMENSION 6
#define ACCURACY 0.000001

double mat[DIMENSION][DIMENSION + 1] = { { 10, 1, 0, 0, 0, 1, 9 }, { 1, 10, 1, 0, 0, 0, 24 }, { 0, 1, 10, 1, 0, 0, 31 }, { 0, 0, 1, 10, 1, 0, -9 }, { 0, 0, 0, 1, 10, 1, -24 }, { 1, 0, 0, 0, 1, 10, -31 } };
double eqaision[DIMENSION][DIMENSION];
double coe[DIMENSION] = { 1, 1, 1, 1, 1, 1 };
double wasCoe[DIMENSION] = { 0, 0, 0,0,0,0 };
int colIndex[DIMENSION];


/**
*	transPos
*	行を入れ替えて収束する可能性があるかの判断
*
*/
bool transPos(int *index){
	bool check = true;

	for (int i = 0; i < DIMENSION; i++){
		if (index[i] == -1){
			check = false;
		}
	}
	return check;
}


/**
*	matrixSet
*	収束する可能性が高いように行入れ替え
*/
void matrixSet(){
	int maxCol = 0;
	int maxColList[DIMENSION];
	double newMat[DIMENSION][DIMENSION + 1];

	for (int i = 0; i < DIMENSION; i++){
		colIndex[i] = -1;
	}
	for (int i = 0; i < DIMENSION; i++){
		maxCol = 0;
		for (int j = 1; j < DIMENSION; j++){
			if (mat[i][maxCol] < mat[i][j]){
				maxCol = j;
			}
		}
		maxColList[i] = maxCol;
		colIndex[maxCol] = i;
	}

	if (transPos(colIndex)){
		for (int i = 0; i < DIMENSION; i++){
			for (int j = 0; j <= DIMENSION; j++){
				newMat[i][j] = mat[colIndex[i]][j];
			}
		}

		for (int i = 0; i < DIMENSION; i++){
			for (int j = 0; j <= DIMENSION; j++){
				mat[i][j] = newMat[i][j];
			}
		}
	}


}


/**
*	possibility
*	収束可能性判断
*/
bool possibility(){
	bool check = true;
	double cnt;

	for (int i = 0; i < DIMENSION; i++){
		cnt = 0;
		for (int j = 0; j < DIMENSION; j++){
			if (i != j){
				cnt += mat[i][j];
			}
		}
		if (mat[i][i] < cnt){
			check = false;
		}
	}
	return check;
}


/**
*	deformation
*	移項
*/
void deformation(){
	int k;
	for (int i = 0; i < DIMENSION; i++){
		k = 0;
		for (int j = 0; j < DIMENSION + 1; j++){
			if (i != j){
				eqaision[i][k] = mat[i][j] / mat[i][i];
				k++;
			}
		}
	}
}


/**
*	calc
*	実際に計算
*/
void calc(){
	int k = 0;

	for (int i = 0; i < DIMENSION; i++){
		wasCoe[i] = coe[i];
	}
	for (int i = 0; i < DIMENSION; i++){
		k = 0;
		coe[i] = eqaision[i][DIMENSION-1];
		for (int j = 0; j < DIMENSION; j++){
			if (i != j){
				coe[i] = coe[i] - eqaision[i][k] * coe[j];
				k++;
			}
		}
	}
	for (int i = 0; i < DIMENSION; i++){
		printf("%3.3f　", coe[colIndex[i]]);
	}
	printf("\n");
}


/**
*	check
*	収束判定
*/
bool check(){
	bool cnt = false;
	for (int i = 0; i < DIMENSION; i++){
		if (fabs(coe[i] - wasCoe[i])>ACCURACY){
			cnt = true;
		}
	}
	return cnt;
}


/**
*	output
*	結果出力
*/
void output(){
	printf("The answers are ");
	for (int i = 0; i < DIMENSION; i++){
		printf("X%d = %f	", i + 1, coe[colIndex[i]]);
	}
}


void main(){
	matrixSet();
	if (possibility()){
		deformation();
		while (check()){
			calc();
		}
		output();
	}
	else{
		printf("this case can not calc.\n");
	}
}