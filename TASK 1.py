from tkinter import *

# main window setup
app = Tk()
app.title("Enhanced Calculator by Rachit Misra")
app.config(background="#FF474C")
app.resizable(False, False)

# global variables
expression = ""
operation = ""
last_operation = ""

# functions
def click(num):
    entry_field.insert(END, str(num))

def add():
    calculate("add")

def subtract():
    calculate("subtract")

def multiply():
    calculate("multiply")

def divide():
    calculate("divide")

def calculate(op):
    global expression, operation
    expression = entry_field.get()
    operation = op
    entry_field.delete(0, END)
    update_history(f"{expression} {op_symbols[op]}")

def equal():
    global expression, operation
    try:
        second = entry_field.get()
        result = 0

        first_num = float(expression)
        second_num = float(second)

        if operation == "add":
            result = first_num + second_num
        elif operation == "subtract":
            result = first_num - second_num
        elif operation == "multiply":
            result = first_num * second_num
        elif operation == "divide":
            if second_num == 0:
                entry_field.delete(0, END)
                entry_field.insert(0, "Error: Div by 0")
                return
            result = first_num / second_num

        entry_field.delete(0, END)
        if result.is_integer():
            entry_field.insert(0, int(result))
        else:
            entry_field.insert(0, round(result, 5))

        update_history(f"{expression} {op_symbols[operation]} {second} = {result}")
    except:
        entry_field.delete(0, END)
        entry_field.insert(0, "Error")
        update_history("Error")

def clear():
    entry_field.delete(0, END)
    update_history("")

def backspace():
    current = entry_field.get()
    entry_field.delete(0, END)
    entry_field.insert(0, current[:-1])

def dot():
    current = entry_field.get()
    if '.' not in current:
        entry_field.insert(END, '.')

def update_history(text):
    history_label.config(text=text)

# keyboard bindings
def keypress(event):
    key = event.char
    if key.isdigit():
        click(key)
    elif key == '+':
        add()
    elif key == '-':
        subtract()
    elif key == '*':
        multiply()
    elif key == '/':
        divide()
    elif key == '.':
        dot()
    elif key == '\r':  # Enter key
        equal()
    elif key == '\x08':  # Backspace key
        backspace()

# symbols for history
op_symbols = {
    "add": "+",
    "subtract": "-",
    "multiply": "×",
    "divide": "÷"
}

# widgets
entry_field = Entry(app, width=25, justify="right", font=("Arial", 18), borderwidth=5,
                    bg="#ffffff", fg="#000000")
entry_field.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

history_label = Label(app, text="", bg="#FF474C", fg="white", anchor="e", font=("Arial", 10))
history_label.grid(row=1, column=0, columnspan=4, sticky="we")

# buttons
buttons = [
    ('7', lambda: click(7)), ('8', lambda: click(8)), ('9', lambda: click(9)), ('←', backspace),
    ('4', lambda: click(4)), ('5', lambda: click(5)), ('6', lambda: click(6)), ('+', add),
    ('1', lambda: click(1)), ('2', lambda: click(2)), ('3', lambda: click(3)), ('-', subtract),
    ('0', lambda: click(0)), ('.', dot), ('=', equal), ('×', multiply),
    ('÷', divide), ('C', clear)  # divide button first, then clear
]

# place buttons in grid
row = 2
col = 0
for text, cmd in buttons:
    if text == '÷':
        Button(app, text=text, width=7, height=2, font=("Arial", 12), command=cmd).grid(
            row=row, column=0, columnspan=4, pady=2, padx=2, sticky="we"
        )
        row += 1
        continue
    elif text == 'C':
        Button(app, text=text, width=32, height=2, font=("Arial", 12), command=cmd).grid(
            row=row, column=0, columnspan=4, pady=2, padx=2, sticky="we"
        )
        row += 1
        continue

    Button(app, text=text, width=7, height=2, font=("Arial", 12), command=cmd).grid(
        row=row, column=col, pady=2, padx=2
    )
    col += 1
    if col > 3:
        col = 0
        row += 1

# keyboard binding
app.bind("<Key>", keypress)

# run the GUI
app.mainloop()
