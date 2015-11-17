/*--------------------------------------
*	Name:		NewtonRaphsonMethod.c
*	Author:		R.Imai
*	Created:	2015 / 10 / 28
*	Last Date:	2015 / 10 / 28
*	Note:	�j���[�g���E���v�\���@
*
*-------------------------------------*/
#include<stdio.h>
#include<math.h>
#include<stdlib.h>
#include<string>

#define MAXNUM 100

/**
*	ACCURACY:	��������덷
*	NMAX:		�ő厎�s��
*	DIM:		�������̎���
*/
#define ACCURACY 0.001
#define NMAX 100
#define DIM 3

/**
*	coefficient:�W���z��
*		- �z��̃C���f�b�N�X�̐�����x�̎w���Ɠ���
*
*	checker:	���[�v�𔲂��o���g���K�[
*
*	detect:		���[�v�𔲂������R��\��
*		- 1: ����I��
*		  2: �񐔃I�[�o�[
*		  3: 0����
*/
const double coefficient[DIM + 1] = { -34, 1, 2, 3};
bool checker = true;
int detect = 0;

/**
*	eqation
*	- f(x)�̌v�Z
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
*	- f(x)�̔����̌v�Z
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
*	- ���ۂɌv�Z
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
*	- detect�̒l�ɂ�胁�b�Z�[�W�̃v�����g
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

