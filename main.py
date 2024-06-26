# Импортируем нужные библиотеки
import os
import textwrap


# Создаем класс для управления макросами
class Macro:
    def __init__(self, name, arguments, code):
        self.name = name
        self.arguments = arguments
        self.code = code


# Словарь макросов
macros = {
    'stop': Macro('stop', [''], "hlt"),
    "uart_write": Macro("uart_write", ["value"], "mov r:1, value addr \nlds r:0, [r:1] \nout r:0"),
    "var": Macro("var", ["value1", "value2"], "value1 dd value2"),
    "uart_read": Macro("uart_read", ["value"], "in r:0 \nmov r:1, value addr \nlds [r:1], r:0"),
    "inc": Macro("inc", ['a'], 'mov r:1, a addr \nlds r:0, [r:1] \nadd r:0, r:0, 1h \nlds [r:1], r:0'),
    "dec": Macro("dec", ['a'], 'mov r:1, a addr \nlds r:0, [r:1] \nsub r:0, r:0, 1h \nlds [r:1], r:0'),
    'add': Macro('add', ['value', 'b', 'c'],
                 'mov r:1, value addr \nmov r:2, b addr \nlds r:0, [r:1] \nlds r:3, [r:2] \nadd r:0, r:3, r:0 \nmov r:1, c addr \nlds [r:1], r:0'),
    'sub': Macro('sub', ['a', 'b', 'c'],
                 'mov r:1, a addr \nmov r:2, b addr \nlds r:0, [r:1] \nlds r:3, [r:2] \nsub r:0, r:3, r:0 \nmov r:1, c addr \nlds [r:1], r:0'),
    'whilenz': Macro('whilenz', ['value'],
                     ".startwhile: \nmov r:1, value addr \nlds r:0, [r:1] \ncmpe r:0, r:0, 0h \njz r:31, r:0, .startwhile addr"),
    'whilez': Macro('whilez', ['value'],
                     ".startwhile: \nmov r:1, value addr \nlds r:0, [r:1] \ncmpe r:0, r:0, 0h \njnz r:31, r:0, .startwhile addr"),
    'ifeq': Macro('ifeq', ['value', 'value1'], "mov r:1, value addr \nlds r:0, [r:1] \nmov r:2, value1 addr \nlds r:3, [r:2] \ncmpe r:0, r:3, r:0 \njz r:31, r:0, .endif addr \n.endif:"),
    'ifneq': Macro('ifneq', ['value', 'value1'], "mov r:1, value addr \nlds r:0, [r:1] \nmov r:2, value1 addr \nlds r:3, [r:2] \ncmpe r:0, r:3, r:0 \njnz r:31, r:0, .endif addr \n.endif:"),
    'ifgr': Macro('ifgr', ['value', 'value1'], "mov r:1, value addr \nlds r:0, [r:1] \nmov r:2, value1 addr \nlds r:3, [r:2] \ncmpa r:0, r:0, r:3 \njz r:31, r:0, .endif addr \n.endif:"),
    'ifls': Macro('ifls', ['value', 'value1'], "mov r:1, value addr \nlds r:0, [r:1] \nmov r:2, value1 addr \nlds r:3, [r:2] \ncmpa r:0, r:0, r:3 \njnz r:31, r:0, .endif addr \n.endif:"),
    'end': Macro('end', [''], '\n'),
    'endif': Macro('endif', [''], '\n'),
    'set': Macro('set', ['param', 'value'], 'mov r:1, param addr \nmov r:0, value \nlds [r:1], r:0')
}


# Функция для обработки макросов
def process_macros(code):
    # Разбиваем код на строки
    # lines = code.split("n")
    lines = code
    cycles_st = []
    # Перебираем каждую строку
    for i, line in enumerate(lines):
        # Ищем макрос в строке
        line = line.lstrip()
        if line == '':
            continue
        for macro in macros.values():
            #print(line, line.lstrip(), line.lstrip().startswith(macro.name), macro.name, line.startswith(macro.name))
            if line.lstrip().split()[0] == macro.name:

                # Получаем аргументы макроса
                arguments = line[len(macro.name):].strip().split(",")
                # print(line, arguments, macro.arguments)
                # Проверяем количество аргументов
                if len(arguments) != len(macro.arguments):
                    raise Exception(
                        f"Ошибка в строке {i + 1}: неправильное количество аргументов для макроса {macro.name}")

                if macro.name == 'whilenz' or macro.name == 'whilez':
                    d = macro.code.replace(macro.arguments[0], arguments[0])
                    cycles_st.append([i, d.split('\n')[1:]])
                    d = '\n' + d.split('\n')[0][:-2] + str(cycles_st[-1][0]) + ':'
                elif macro.name in ["ifeq", "ifneq", "ifgr", "ifls"]:
                    d = macro.code.replace(macro.arguments[0], arguments[0], 1)
                    d = d.replace(macro.arguments[1], arguments[1], 1)
                    cycles_st.append([i, d.split('\n')[-1].replace('.endif:', f'.endif{i}:')])
                    d = '\n'.join(d.replace('endif', f'endif{i}').split('\n')[:len(d.split('\n')) - 1])
                elif macro.name == 'end':
                    s = '\n'.join(cycles_st[-1][1])
                    s = s[:-5] + str(cycles_st[-1][0]) + s[-5:] + '\n'
                    cycles_st.pop(-1)
                    d = s
                elif macro.name == 'endif':
                    s = ''.join(cycles_st[-1][-1])
                    cycles_st.pop(-1)
                    d = s
                else:
                    d = macro.code
                    for j in range(len(macro.arguments)):
                        d = d.replace(macro.arguments[j], arguments[j], 1)
                lines[i] = d

                print(cycles_st)
    # Возвращаем обработанный код
    s = ''
    for i in range(len(lines)):
        s += lines[i] + "\n"
    return "".join(s)


# Функция для генерации ассемблерного кода
def generate_assembly(code):
    # Обрабатываем макросы
    processed_code = process_macros(code)

    # Заворачиваем код в секцию .text
    asm_code = textwrap.dedent(f"""format binary

include "ISA.inc"
{processed_code}

    """)

    # Возвращаем ассемблерный код
    return asm_code

i = int(input())
# Запрашиваем у пользователя код
with open("code.dml") as f:
        code = f.readlines()
if i == 0:
    # Генерируем ассемблерный код
    asm_code = generate_assembly(code)
else:
    asm_code = ''.join(code)
print('##############')
print(asm_code)
# Сохраняем ассемблерный код в файл
with open("output.asm", "w") as f:
    f.write(asm_code)

# Собираем и запускаем ассемблерный код
os.system('"/ISA/FASM.EXE" output.asm')
os.system('"/ISA/mif_converter.exe" output.bin output.mif')