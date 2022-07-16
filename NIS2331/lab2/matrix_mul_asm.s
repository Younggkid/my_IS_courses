
	.text
	.global matrix_mul_asm

matrix_mul_asm:
    // Please write your code below that will implement:
    //       int matrix_mul_asm(Matrix* results, Matrix* source1, Matrix* source2);
	//programmed by lcy520030910301
	//The basic idea is to break big matrix into small 4x4 matrixs,and fo nested loop
	//Code for neon show a easy way to compute the multiply of 4X4 matrix
    LDR W3,[X1,#4] //COL1
	LDR W4,[X2]    //ROW2
	CMP W3,W4
	BEQ mulTI   //check if col1=row2,if true ,jm to mutiple part
	MOV W0,#1     //return value 1
	RET        //col!=row2,come to return
mulTI:
			LSR W3,W3,#2
			LDR W4,[X1]   //get Row1 to R4
			LSR W4,W4,#2
			LDR W5,[X2,#4]//get Col2 to R5
			LSR W5,W5,#2
			MOV W6,#0
			MOV W7,W6     //R6,R7 start from 0,the counter of row and col
			MOV W8,#0     //R8 start from 0,the counter of inner cycle
			LDR X1,[X1,#8]//start of source1
			LDR X2,[X2,#8]//start of source2
			LDR X0,[X0,#8]//start of result
			MOV X13,#0
loop1:		
			CMP W6,W4     //check if row loop is completed
			BGE finish1
loop2:		
			CMP W7,W5     //check if col loop is completed
			BGE finish2
		    MOV V8.D[0], X13
			MOV V8.D[1], X13
			MOV V9.D[0], X13
			MOV V9.D[1], X13
			MOV V10.D[0], X13
			MOV V10.D[1], X13
			MOV V11.D[0], X13
			MOV V11.D[1], X13
			//zero the result registers,there is no easy way to zero ,so i choose the stupid way,but it works
loop3:		
			CMP W8,W3     //check if one number of result has been computed
			BGE finish3  
			//The following W9 is the offset of any small matrix start address
			//X10 store the address after offset
			//W11 is the inner offset of small matrix             
			MUL W9,W3,W6   
			LSL W9,W9,#6   // W9*64 because this is block,each block has 64 offset
			ADD W9,W9,W8,LSL #4
		    ADD X10,X1,W9,SXTW
			LSL W11,W3,#4
			LD1 { V0.4S },[X10],X11
			LD1 { V1.4S },[X10],X11
			LD1 { V2.4S },[X10],X11
			LD1 { V3.4S },[X10] //get the 16 elements of matrix1

			MUL W9,W8,W5
			LSL W9,W9,#6
			ADD W9,W9,W7,LSL #4
			ADD X10,X2,W9,SXTW
			LSL W11,W5,#4
			LD1 { V4.4S },[X10],X11
			LD1 { V5.4S },[X10],X11
			LD1 { V6.4S },[X10],X11
			LD1 { V7.4S },[X10]//get the 16 elements of matrix2

            //next do the 4x4 multiply,and add them togeter
            MLA V8.4S, V4.4S, V0.S[0] 
			MLA V9.4S, V4.4S, V1.S[0] 
			MLA V10.4S, V4.4S, V2.S[0] 
			MLA V11.4S, V4.4S, V3.S[0] 
			MLA V8.4S, V5.4S, V0.S[1] 
			MLA V9.4S, V5.4S, V1.S[1] 
			MLA V10.4S, V5.4S, V2.S[1] 
			MLA V11.4S, V5.4S, V3.S[1] 
			MLA V8.4S, V6.4S, V0.S[2] 
			MLA V9.4S, V6.4S, V1.S[2] 
			MLA V10.4S, V6.4S, V2.S[2] 
			MLA V11.4S, V6.4S, V3.S[2] 
			MLA V8.4S, V7.4S, V0.S[3] 
			MLA V9.4S, V7.4S, V1.S[3] 
			MLA V10.4S, V7.4S, V2.S[3] 
			MLA V11.4S, V7.4S, V3.S[3] 
			ADD W8,W8,#1
			B loop3
finish3:
		    MUL W9,W5,W6
			LSL W9,W9,#6
			ADD W9,W9,W7,LSL #4
			ADD X10,X0,W9,SXTW
			LSL W11,W5,#4
			ST1 { V8.4S },[X10],X11
			ST1 { V9.4S },[X10],X11
			ST1 { V10.4S },[X10],X11
			ST1 { V11.4S },[X10]

			ADD W7,W7,#1
			MOV W8,#0    //Reset R8
			B loop2
finish2:
			ADD W6,W6,#1
			MOV W7,#0    //Reset R7
			B loop1
finish1:
            MOV X0,#0

	RET
