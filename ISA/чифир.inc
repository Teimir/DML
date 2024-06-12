include "ISA.inc"

; ASSUME:
; - r:31 is program counter
; - r:30 is stack pointer
; - r:29 is base pointer
; - r:28 is temp register
; - r:27 is second temp register
; - r:26 is flags register
; - r:25 is loop counter
; - r:0  is return value register


define ip r:31
define sp r:30
define bp r:29
define eflags r:26
define cx r:25
define ax r:0

macro push op {
    sub sp, 1
    lds [sp], op
}

macro pop op {
    add sp, 1
    mov r:28, sp
    sub r:28, 1
    lds op, [r:28]
}

macro pushf {
    push eflags
}

macro popf {
    pop eflags
}

macro call adr {
    push @f
    mov ip, adr
@@:
}

macro ret {
    pop ip
}

macro b adr {
    mov ip, adr
}

macro cmp a, b {
    sub r:28, a, b
    ; now we need to check if r:28 is negative
    ; if it is, then we need to set the "less" flag
    ; otherwise, we need to check if r:28 is zero
    ; if it isn't, we need to set the "greater" flag
    mov r:27, r:28
    and r:27, r:27, 0x80000000
    xor r:27, r:27, 0x80000000
    cmp r:27, 0
    jz r:31, r:27, .equal
    jnz r:31, r:27, .greater
.equal:
    mov r:28, eflags
    or r:28, r:28, 0x1
    mov eflags, r:28
    jmp r:31, .done
.greater:
    mov r:28, eflags
    or r:28, r:28, 0x2
    mov eflags, r:28
    jmp r:31, .done
.done:
}

macro be adr {
    ; we need to check if neither "less" nor "greater" flags are set
    ; if they are, skip the instruction
    mov r:27, eflags
    and r:27, r:27, 0x3
    cmp r:27, 0
    jz r:31, r:27, @f
    mov ip, adr
    jmp r:31, @f
@@:
}

macro bne adr {
    be @f
    b adr
@@:
}

macro bgt adr {
    ; we need to check if "greater" flag is set
    ; if it is, skip the instruction
    mov r:27, eflags
    and r:27, r:27, 0x2
    cmp r:27, 0
    jz r:31, r:27, @f
    mov ip, adr
@@:
}

macro ble adr {
    ; we need to check if "less" or "greater" flags are set
    ; if they are, skip the instruction
    mov r:27, eflags
    and r:27, r:27, 0x3
    cmp r:27, 0
    jz r:31, r:27, @f
    mov ip, adr
@@:
}

macro bge adr {
    ; we need to check if "greater" or "equal" flags are set
    ; if they are, skip the instruction
    mov r:27, eflags
    and r:27, r:27, 0x3
    cmp r:27, 0
    jz r:31, r:27, @f
    mov ip, adr
@@:
}

macro blt adr {
    ; we need to check if "less" flag is set
    ; if it is, skip the instruction
    mov r:27, eflags
    and r:27, r:27, 0x1
    cmp r:27, 0
    jz r:31, r:27, @f
    mov ip, adr
@@:
}

macro lod r, adr {
    mov r:28, adr
    lds r, [r:28]
}

macro sto adr, r {
    mov r:28, adr
    lds [r:28], r
}

macro enter n {
    push sp
    mov bp, sp
    if ~n eq
        if ~n eq 0
            sub sp, 1
        end if
    end if
}

macro leave {
    mov sp, bp
    pop bp
}

macro loop adr {
    cmp cx, 0
    be @f
    sub cx, 1
    b adr
@@:
}
