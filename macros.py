def ifeq():
    global flag
    if flag != 1:
        if eval(file[1][:-1]) != eval(file[2]):
            flag = 1
        else:
            flag = 0
    print('Робит 1')

def ifneq():
    global flag
    if flag != 1:
        if eval(file[1][:-1]) == eval(file[2]):
            flag = 1
        else:
            flag = 0
    print('Робит 2')

def uart_write():
    print(eval(file[1]))

def endif():
    global flag
    flag = 0
    print('Закончить бы')

def stop():
    exit()

def set():
    global file
    eval("{} = {}".format(file[1][:-1], file[2]))

flag = 0
A = 10
B = 12
with open('test_macros/code.txt') as f:
    while True:
        file = f.readline().split()
        t = eval(file[0]+"()")

