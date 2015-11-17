/*--------------------------------------
*	Name:		NewtonRaphsonMethod.c
*	Author:		R.Imai
*	Created:	2015 / 10 / 28
*	Last Date:	2015 / 10 / 28
*	Note:	ニュートン・ラプソン法
*
*-------------------------------------*/
#include<stdio.h>
#include<math.h>
#include<stdlib.h>
#include<string>

#define MAXNUM 100

/**
*	ACCURACY:	収束判定誤差
*	NMAX:		最大試行回数
*	DIM:		方程式の次元
*/
#define ACCURACY 0.001
#define NMAX 100
#define DIM 3

/**
*	coefficient:係数配列
*		- 配列のインデックスの数字はxの指数と同じ
*
*	checker:	ループを抜け出すトリガー
*
*	detect:		ループを抜けた理由を表す
*		- 1: 正常終了
*		  2: 回数オーバー
*		  3: 0割り
*/
const double coefficient[DIM + 1] = { -34, 1, 2, 3};
bool checker = true;
int detect = 0;

/**
*	eqation
*	- f(x)の計算
*
*/
double eqation(double x){
	double result = 0;
	for (int i = 0; i <= DIM; i++){
		result = result + pow(x, i)*coefficient[i];
	}
	return result;
}

/**
*	differential
*	- f(x)の微分の計算
*
*/
double differential(double x){
	/*double result = 0;
	for (int i = 1; i <= DIM; i++){
		result = result + i*pow(x, i - 1)*coefficient[i];
	}
	return result;*/

	return (eqation(x) - eqation(x - 0.0000001)) / 0.0000001;
}


/**
*	calc
*	- 実際に計算
*
*/
double calc(double x){
	double del;

	del = -eqation(x) / differential(x);
	x = x + del;
	if (fabs(del) < ACCURACY){
		checker = false;
		detect = 1;
	}
	return x;
}


/**
*	print
*	- detectの値によりメッセージのプリント
*
*/
void print(double ans){
	switch (detect)
	{
	case 1:
		printf("the answer is : %f", ans);
		break;
	case 2:
		printf("error : exceeded the limit number of trials.");
		break;
	case 3:
		printf("error : divided by 0.");
		break;
	default:
		break;
	}
}


int main(int argc, char *argv[]){
	int a;
	double x = atof(argv[1]);
	int n = 0;

	do{
		printf("[%d] : %f\n", n, x);
		x = calc(x);
		n++;
		if (n > NMAX){
			checker = false;
			detect = 2;
		}
	} while (checker);

	print(x);
	scanf_s("%f", &a);

	return 0;
}

