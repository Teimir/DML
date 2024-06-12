format binary

include "ISA.inc"


.startwhile0: 

mov r:1, B addr 
lds r:0, [r:1] 
out r:0
mov r:1, B addr 
lds r:0, [r:1] 
sub r:0, r:0, 1h 
lds [r:1], r:0
mov r:1, A addr 
mov r:0,  5 
lds [r:1], r:0

.startwhile4: 

mov r:1, A addr 
lds r:0, [r:1] 
out r:0
mov r:1, A addr 
lds r:0, [r:1] 
sub r:0, r:0, 1h 
lds [r:1], r:0
mov r:1, A addr 
lds r:0, [r:1] 
cmpe r:0, r:0, 0h 
jz r:31, r:0, .startwhile4 addr
mov r:1, B addr 
lds r:0, [r:1] 
cmpe r:0, r:0, 0h 
jz r:31, r:0, .startwhile0 addr
hlt
B dd  5
A dd  0