
format binary

include "ISA.inc"

mov r:1, A addr 
lds r:0, [r:1] 
out r:0
mov r:1, B addr 
lds r:0, [r:1] 
out r:0
mov r:1, C addr 
lds r:0, [r:1] 
out r:0
mov r:1, A addr 
mov r:2,  B addr 
lds r:0, [r:1] 
lds r:3, [r:2] 
add r:0, r:3, r:0 
mov r:1,  C addr 
lds [r:1], r:0
mov r:1, A addr 
lds r:0, [r:1] 
out r:0
mov r:1, B addr 
lds r:0, [r:1] 
out r:0
mov r:1, C addr 
lds r:0, [r:1] 
out r:0
hlt
A dd  1
B dd  2
C dd  0

