
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Matrix source1, source2 & result(memory preserve)
// You can change this area to test different size of matrices
#define SOURCE1_ROWS			8
#define SOURCE1_COLUMNS		8
#define SOURCE2_ROWS			8
#define SOURCE2_COLUMNS		8

const static int SOURCE_MATRIX1_DATA[SOURCE1_ROWS][SOURCE1_COLUMNS] = {
	{1, 2, 3, 4, 5, 6, 7, 8},
	{2, 3, 4, 5, 6, 7, 8, 9},
	{3, 4, 5, 6, 7, 8, 9, 10},
	{4, 5, 6, 7, 8, 9, 10, 11},
	{5, 6, 7, 8, 9, 10, 11, 12},
	{6, 7, 8, 9, 10, 11, 12, 13},
	{7, 8, 9, 10, 11, 12, 13, 14},
	{8, 9, 10, 11, 12, 13, 14, 15}
};

const static int SOURCE_MATRIX2_DATA[SOURCE2_ROWS][SOURCE2_COLUMNS] = {
	{1, 1, 1, 1, 1, 1, 1, 1},
	{2, 2, 2, 2, 2, 2, 2, 2},
	{3, 3, 3, 3, 3, 3, 3, 3},
	{4, 4, 4, 4, 4, 4, 4, 4},
	{5, 5, 5, 5, 5, 5, 5, 5},
	{6, 6, 6, 6, 6, 6, 6, 6},
	{7, 7, 7, 7, 7, 7, 7, 7},
	{8, 8, 8, 8, 8, 8, 8, 8}
};
static int results_matrix_data[SOURCE1_ROWS][SOURCE2_COLUMNS];
// Matrix source1, source2 & result(memory preserve) END

typedef struct Matrix {
	int row;					//Number of rows
	int column;				//Number of columns
	const int* data;	//Address of matrix data
}Matrix;

// Matrix multiplication function declare
extern int matrix_mul(Matrix *results, const Matrix *source1, const Matrix *source2);

// Print matrix data
int print_matrix(const Matrix* matrix);
int print_matrix(const Matrix* matrix)
{
	int i, j;
	
	for (i = 0; i < matrix->row; i++)
	{
		for (j = 0; j < matrix->column; j++)
			printf("%d ", *(matrix->data + i * matrix->column + j));
		printf("\n");
	}
	return 0;
}


int main()
{
	//Source matrix 1 structure
	const Matrix source_matrix1 = {
		SOURCE1_ROWS,
		SOURCE1_COLUMNS,
		(const int*)SOURCE_MATRIX1_DATA
	};
	//Source matrix 2 structure
	const Matrix source_matrix2 = {
		SOURCE2_ROWS,
		SOURCE2_COLUMNS,
		(const int*)SOURCE_MATRIX2_DATA
	};
	//Result matrix structure
	Matrix results_matrix = {
		SOURCE1_ROWS,
		SOURCE2_COLUMNS,
		(const int*)results_matrix_data
	};
	
	//Clear result matrix data
	memset(results_matrix_data, 0, sizeof(int) * SOURCE1_ROWS * SOURCE2_COLUMNS);
	
	//Matrix multiplication
	if (matrix_mul(&results_matrix, &source_matrix1, &source_matrix2) == 0)
		// Success
		print_matrix(&results_matrix);
	else
		// Fail
		printf("Fail to multiply two matrices.\n");

	return 0;
}
