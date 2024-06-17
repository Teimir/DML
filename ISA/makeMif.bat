@echo off
fasm.exe PROG.asm
mif_converter.exe PROG.bin PROG.mif
pause