
#include "matrix.h"

int matrix_mul(Matrix* results, Matrix* source1, Matrix* source2)
{
	int i, j, k, sum;

	if (source1->column != source2->row)
		return 1;

	for (i = 0; i < source1->row; i++)
	{
		for (j = 0; j < source2->column; j++)
		{
			sum = 0;
			for (k = 0; k < source1->column; k++)
			{
				sum += *(source1->data + (i * source1->column + k)) *
					*(source2->data + (k * source2->column + j));
			}
			*(results->data + (i * results->column + j)) = sum;
		}
	}

	return 0;
}