matrix_mul: matrix_mul.o matrix_mul_asm.o main.o
	gcc -O3 -o matrix_mul matrix_mul.o matrix_mul_asm.o main.o

matrix_mul.o: matrix_mul.c matrix.h
	gcc -O3 -c matrix_mul.c

matrix_mul_asm.o: matrix_mul_asm.s
	as matrix_mul_asm.s -o matrix_mul_asm.o

main.o:	main.c matrix.h
	gcc -O3 -c main.c

clean:
	rm matrix_mul main.o matrix_mul.o matrix_mul_asm.o
