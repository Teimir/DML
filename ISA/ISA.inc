macro _instr instrnum*, op1*, op2=r:0, op3=r:0{
	local opcode
	opcode = (instrnum and 1111b) shl 3
	match =r:reg1, op1\{
		local matched1
		opcode = opcode or ((reg1 and 11111b) shl 7)
		match =r:reg2, op2\\{
			local matched2
			define matched1
			opcode = opcode or ((reg2 and 11111b) shl 12)
			match =r:reg3, op3\\\{
				define matched2
				opcode = opcode or ((reg3 and 11111b) shl 17)
				opcode = opcode or 11b
			\\\}
			match =matched2, matched2\\\{
				opcode = opcode or ((op3 and 111111111111111b) shl 17)
				opcode = opcode or 10b
			\\\}
		\\}
		match =matched1, matched1\\{
			opcode = opcode or ((op2 and 11111111111111111111b) shl 12)
			opcode = opcode or 01b
		\\}
		dd opcode
	\}
}

; _instr 0, r:0, 5

nop equ dd 0

hlt equ dd 5

macro mov args*&{
	_instr 0, args
}
macro add args*&{
	_instr 1, args
}
macro sub args*&{
	_instr 2, args
}
macro not args*&{
	_instr 3, args
}
macro and args*&{
	_instr 4, args
}
macro or args*&{
	_instr 5, args
}
macro xor args*&{
	_instr 6, args
}
macro shr args*&{
	_instr 7, args
}
macro shl args*&{
	_instr 8, args
}

macro cmpa args*&{
	_instr 9, args
}

macro cmpe args*&{
	_instr 10, args
}

macro cmpb args*&{
	_instr 11, args
}

macro jnz args*&{
	_instr 12, args
}

macro jz args*&{
	_instr 13, args
}

addr fix shr 2

macro lds op1, op2{
	local opcode
	opcode = 4
	match r:reg1 [r:reg2], op1 op2\{
		opcode = opcode or (0 shl 3)
		opcode = opcode or ((reg1 and 11111b) shl 7)
		opcode = opcode or ((reg2 and 11111b) shl 12)
	\}
	match r:reg1 [r:reg2], op2 op1\{
		opcode = opcode or (1 shl 3)
		opcode = opcode or ((reg1 and 11111b) shl 7)
		opcode = opcode or ((reg2 and 11111b) shl 12)
	\}
	dd opcode
}

macro _uart_ins _insvar, op1*{
	local opcode
	opcode = 4
	match r:reg1, op1\{
		opcode = opcode or (_insvar shl 3)
		opcode = opcode or 1 shl 5
		opcode = opcode or ((reg1 and 11111b) shl 7)
	\}
	dd opcode
}

macro ins op1{
	_uart_ins 0, op1
}

macro sets op1{
	_uart_ins 1, op1
}

macro in op1{
	_uart_ins 10b, op1
}

macro out op1*{
	_uart_ins 11b, op1
}