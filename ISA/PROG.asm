format binary
include "ISA.inc"
mov r:0, a addr
lds r:0,    [r:0]
mov r:1, b addr
lds r:1,    [r:1]
cmpe r:2, r:1, r:0
mov r:0, c addr
mov r:1, d addr
jnz r:0, r:2, r:1
out r:0
out r:3
lds [r:0], r:3
out r:0
out r:3
mov r:0, 170
mov r:3, 170
out r:0
out r:3
hlt
a dd 5
b dd 5
c dd 7
d dd 8