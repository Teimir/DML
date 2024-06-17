import tkinter as tk
from tkinter import ttk
import gener


def complete_text(event):
    """Функция автодополнения при нажатии Tab"""
    current_text = text_area.get("insert linestart", "insert")
    for suggestion in suggestions:
        print(suggestion)
        if suggestion.startswith(current_text):
            text_area.delete("insert linestart", "insert")
            text_area.insert("insert", suggestions[suggestion])
            text_area.mark_set("insert", text_area.index("insert") + str(len(suggestions[suggestion])))
            return "break"  # Прерываем обработку события
    return "break"  # Прерываем обработку события, если ничего не найдено


def submit_text():
    """Обработчик события нажатия кнопки"""
    text = text_area.get("1.0", tk.END)
    print(f"Введенный текст:\n{text}")
    # Здесь можно добавить код для обработки введенного текста

# Создание окна
root = tk.Tk()
root.title("Многострочное поле ввода")

# Создание текстового поля
text_area = tk.Text(root, wrap=tk.WORD)
text_area.insert(tk.END, 'format binary \ninclude "ISA.inc" \n')
text_area.pack(fill=tk.BOTH, expand=True)
text_area.bind("<Tab>", complete_text)

# Создание кнопки
submit_button = ttk.Button(root, text="Отправить", command=submit_text)
submit_button.pack(pady=10)



def start():
# Запуск цикла обработки событий
    root.mainloop()
