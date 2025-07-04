from tkinter import *

# Window setup
app = Tk()
app.title("Enhanced Calculator by Rachit Mishra")
app.config(background="#2E8BC0")  # nice soft blue
app.resizable(False, False)

expression = ""
operation = ""
op_symbols = {"add": "+", "subtract": "-", "multiply": "×", "divide": "÷"}

def click(num):
    entry_field.insert(END, str(num))

def calculate(op):
    global expression, operation
    expression = entry_field.get()
    operation = op
    entry_field.delete(0, END)
    update_history(f"{expression} {op_symbols[op]}")

def equal():
    try:
        first = float(expression)
        second = float(entry_field.get())
        if operation == "add":
            result = first + second
        elif operation == "subtract":
            result = first - second
        elif operation == "multiply":
            result = first * second
        elif operation == "divide":
            if second == 0:
                raise ZeroDivisionError
            result = first / second
        entry_field.delete(0, END)
        entry_field.insert(0, int(result) if result.is_integer() else round(result, 5))
        update_history(f"{expression} {op_symbols[operation]} {second} = {result}")
    except ZeroDivisionError:
        entry_field.delete(0, END)
        entry_field.insert(0, "Error: Div by 0")
        update_history("Division by zero error")
    except:
        entry_field.delete(0, END)
        entry_field.insert(0, "Error")
        update_history("Invalid operation")

def clear():
    entry_field.delete(0, END)
    update_history("")

def backspace():
    entry_field.delete(0, END)
    entry_field.insert(0, entry_field.get()[:-1])

def dot():
    if '.' not in entry_field.get():
        entry_field.insert(END, '.')

def update_history(text):
    history_label.config(text=text)

def keypress(event):
    key = event.char
    if key.isdigit(): click(key)
    elif key == '+': calculate("add")
    elif key == '-': calculate("subtract")
    elif key == '*': calculate("multiply")
    elif key == '/': calculate("divide")
    elif key == '\r': equal()
    elif key == '\x08': backspace()
    elif key == '.': dot()

# Entry and history
entry_field = Entry(app, width=25, justify="right", font=("Arial", 18), borderwidth=5, bg="white", fg="black")
entry_field.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

history_label = Label(app, text="", bg="#2E8BC0", fg="#F8F8F8", anchor="e", font=("Arial", 10))
history_label.grid(row=1, column=0, columnspan=4, sticky="we")

# Button style
btn_bg = "#145DA0"
btn_fg = "white"

# Buttons layout (excluding ÷ and C for now)
buttons = [
    ('7', lambda: click(7)), ('8', lambda: click(8)), ('9', lambda: click(9)), ('←', backspace),
    ('4', lambda: click(4)), ('5', lambda: click(5)), ('6', lambda: click(6)), ('+', lambda: calculate("add")),
    ('1', lambda: click(1)), ('2', lambda: click(2)), ('3', lambda: click(3)), ('-', lambda: calculate("subtract")),
    ('0', lambda: click(0)), ('.', dot), ('=', equal), ('×', lambda: calculate("multiply")),
]

# Place buttons
row, col = 2, 0
for text, cmd in buttons:
    Button(app, text=text, width=7, height=2, font=("Arial", 12), command=cmd,
           bg=btn_bg, fg=btn_fg, activebackground="#0C2D48", activeforeground="white").grid(
        row=row, column=col, padx=2, pady=2
    )
    col += 1
    if col > 3:
        col = 0
        row += 1

# ÷ and C side by side
Button(app, text='÷', width=14, height=2, font=("Arial", 12), command=lambda: calculate("divide"),
       bg=btn_bg, fg=btn_fg, activebackground="#0C2D48", activeforeground="white").grid(
    row=row, column=0, columnspan=2, padx=2, pady=2, sticky="we"
)

Button(app, text='C', width=14, height=2, font=("Arial", 12), command=clear,
       bg="#D7263D", fg="white", activebackground="#A4161A", activeforeground="white").grid(
    row=row, column=2, columnspan=2, padx=2, pady=2, sticky="we"
)

# Keyboard support
app.bind("<Key>", keypress)

# Start the app
app.mainloop()
