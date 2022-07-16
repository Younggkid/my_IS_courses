
	AREA	program, CODE, READONLY
matrix_mul
	EXPORT	matrix_mul

    ; Please write your code below that will implement:
	; R0-R10 and stack is used in this program,the basic idea is to do nested loop
	; by lcy520030910301
			LDR R3,[R1,#4] ;COL1
			LDR R4,[R2]    ;ROW2
			CMP R3,R4
			BEQ mulTI     ;check if col1=row2,if true ,jm to mutiple part
			MOV R0,#1     ;return value 1
			BX LR         ;col!=row2,come to return
mulTI		
			PUSH {FP,LR}  ;12 bytes on stack to store the starting address of martixs
			MOV FP,SP
			SUB SP,SP,#12
			LDR R4,[R0,#8]
			STR R4,[SP],#4
			LDR R4,[R1,#8]
			STR R4,[SP],#4
			LDR R4,[R2,#8]
			STR R4,[SP],#4
			SUB SP,SP,#12 ;SP should point to the top of stack
            LDR R4,[R1]   ;get Row1 to R4 
			LDR R5,[R2,#4];get Col2 to R5
			MOV R6,#0
			MOV R7,R6     ;R6,R7 start from 0,the counter of row and col
			MOV R8,#0     ;R8 start from 0,the counter of inner cycle
loop1		
			CMP R6,R4     ;check if row loop is completed
			BGE finish1
loop2		
			CMP R7,R5     ;check if col loop is completed
			BGE finish2
			MOV R0,#0
loop3		
			CMP R8,R3     ;check if one number of result has been computed
			BGE finish3
			ADD R1,SP,#4  ;R1 store address of matrix1 start
			MUL R2,R3,R6
			ADD R2,R2,R8
			LSL R2,R2,#2  ;use R2 to get the offset address of the matrix
			LDR R9,[R1]
			LDR R9,[R9,R2]
			
			ADD R1,R1,#4
			MUL R2,R5,R8
			ADD R2,R2,R7
			LSL R2,R2,#2  ;use R2 to get the offset address of the matrix
			LDR R10,[R1]
			LDR R10,[R10,R2]
			MLA R0,R9,R10,R0
			ADD R8,R8,#1
			B loop3
finish3
			LDR R1,[SP],#0
			MUL R9,R6,R5
			ADD R9,R9,R7
			LSL R9,R9,#2
			STR R0,[R1,R9]
			ADD R7,R7,#1
			MOV R8,#0    ;Reset R8
			B loop2
finish2
			ADD R6,R6,#1
			MOV R7,#0    ;Reset R7
			B loop1
finish1
			MOV SP, FP
			POP {FP, LR}
			MOV R0,#0    ;Return value 0
	
			BX		LR
			END