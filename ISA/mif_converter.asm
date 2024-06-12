format pe64 console

entry main

include "TOOLS\TOOLS.INC"
include_once "TOOLS\cstdio.inc"

importlib kernel32, \
	SetConsoleCP, \
	SetConsoleOutputCP

importlib msvcrt,\
	getch="_getwch"
section ".data" readable writeable
QuartusHeader:
	db "-- Quartus Prime generated Memory Initialization File(.mif)", 0Ah
	db 0Ah
	db "WIDTH = 32;", 0Ah
	db "DEPTH = 4096;", 0Ah
	db 0Ah
	db "ADDRESS_RADIX = UNS;", 0Ah
	db "DATA_RADIX = UNS;", 0Ah
	db 0Ah
	db "CONTENT BEGIN", 0Ah
	db 0

	srcfile dq ?
	dstfile dq ?
	thisdword dd ?

section ".code" readable writeable executable
	proc main
		local argc:DWORD, argv:QWORD
		@call ParseCommandLine(addr argv)
		mov [argc], eax
		@call [SetConsoleCP](1251)
		@call [SetConsoleOutputCP](1251)
		mov rbx, [argv]
		mov rax, [rbx+8]
		mov [srcfile], rax
		mov rax, [rbx+16]
		mov [dstfile], rax
		@call [fopen]([srcfile], "r")
		mov [srcfile], rax
		@call [fopen]([dstfile], "w")
		mov [dstfile], rax
		@call [fputs](QuartusHeader, [dstfile])
		mov rbx, -4095
		@@:
			@call [fscanf]([srcfile], "%4c", thisdword)
			@call [feof]([srcfile])
			test rax, rax
				jnz .offLimit
			@call [fprintf]([dstfile], <09h, "%u: %u;", 0Ah>, addr 4095+rbx, [thisdword])
			inc rbx
		jle @b
		jmp .return
		.offLimit:
			@call [fprintf]([dstfile], <09h, "[%u..4095]: 0;", 0Ah>, addr 4095+rbx)
		.return:
		@call [fputs]("END;", [dstfile])
		; @call [printf](<"%s", 0Ah>, [dstfile])
		; @call [printf](<"%s", 0Ah>, [srcfile])
		ret
	endp
