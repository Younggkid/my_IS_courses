
#ifndef _MATRIX_H
#define _MATRIX_H

#define SOURCE1_ROWS			512
#define SOURCE1_COLUMNS			256
#define SOURCE2_ROWS			256
#define SOURCE2_COLUMNS			512

typedef struct Matrix {
	int row;					//Number of rows
	int column;					//Number of columns
	int* data;					//Address of matrix data
}Matrix;

#endif 

