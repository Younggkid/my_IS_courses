
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <memory.h>

#include "matrix.h"

extern int matrix_mul(Matrix* results, Matrix* source1, Matrix* source2);
extern int matrix_mul_asm(Matrix* results, Matrix* source1, Matrix* source2);

void free_matrix(Matrix* matrix)
{
	if (matrix->data)
		free(matrix->data);
	matrix->data = NULL;
}

void init_matrix(Matrix* matrix, int random)
{
	int i;
	int size = matrix->row * matrix->column;

	free_matrix(matrix);
	matrix->data = (int*)malloc(size * sizeof(int));
	if (random)
	{
		for (i = 0; i < size; i++)
			matrix->data[i] = rand() % 256;
	}
	else
	{
		memset(matrix->data, 0, size * sizeof(int));
	}
}

void print_matrix(Matrix* matrix)
{
	int i, j;

	for (i = 0; i < matrix->row; i++)
	{
		for (j = 0; j < matrix->column; j++)
			printf("%d ", *(matrix->data + i * matrix->column + j));
		printf("\n");
	}
}

int main(void)
{
	clock_t t;
	int result_size = SOURCE1_ROWS * SOURCE2_COLUMNS;
	Matrix source1 = {SOURCE1_ROWS, SOURCE1_COLUMNS, NULL};
	Matrix source2 = {SOURCE2_ROWS, SOURCE2_COLUMNS, NULL};
	Matrix results1 = {SOURCE1_ROWS, SOURCE2_COLUMNS, NULL};
	Matrix results2 = {SOURCE1_ROWS, SOURCE2_COLUMNS, NULL};

	srand((unsigned int)time(NULL));
	init_matrix(&source1, 1);
	init_matrix(&source2, 1);
	init_matrix(&results1, 0);
	init_matrix(&results2, 0);

	t = clock();
	matrix_mul(&results1, &source1, &source2);
	t = clock() - t;
	printf("C multiplication took %ld clock.\n", t);

	t = clock();
	matrix_mul_asm(&results2, &source1, &source2);
	t = clock() - t;
	printf("SIMD multiplication took %ld clock.\n", t);

	if (memcmp(results1.data, results2.data, result_size * 4) == 0)
		printf("SIMD implementation provides correct results.\n");
	else
		printf("SIMD implementation provides wrong results.\n");

	free_matrix(&source1);
	free_matrix(&source2);
	free_matrix(&results1);
	free_matrix(&results2);
}
