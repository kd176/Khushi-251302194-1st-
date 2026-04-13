import tkinter as tk
import math
import csv

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("Pro Calculator")
root.geometry("400x600")
root.resizable(False, False)

# ---------------- VARIABLES ----------------
expression = ""
history = []
memory = 0
dark_mode = True

# ---------------- FUNCTIONS ----------------
def press(val):
    global expression
    expression += str(val)
    input_text.set(expression)

def clear():
    global expression
    expression = ""
    input_text.set("")

def backspace():
    global expression
    expression = expression[:-1]
    input_text.set(expression)

def calculate():
    global expression
    try:
        result = str(eval(expression, {"__builtins__": None}, math.__dict__))
        history.append(f"{expression} = {result}")
        save_history(expression, result)
        update_history()
        expression = result
        input_text.set(result)
    except:
        input_text.set("Error")
        expression = ""

# ---------------- SCIENTIFIC ----------------
def scientific(func):
    global expression
    try:
        result = str(eval(f"{func}({expression})", {"__builtins__": None}, math.__dict__))
        history.append(f"{func}({expression}) = {result}")
        save_history(f"{func}({expression})", result)
        update_history()
        expression = result
        input_text.set(result)
    except:
        input_text.set("Error")
        expression = ""

# ---------------- MEMORY ----------------
def memory_add():
    global memory
    try:
        memory += float(expression)
    except:
        pass

def memory_sub():
    global memory
    try:
        memory -= float(expression)
    except:
        pass

def memory_recall():
    global expression
    expression = str(memory)
    input_text.set(expression)

def memory_clear():
    global memory
    memory = 0

# ---------------- HISTORY ----------------
def update_history():
    history_box.delete(0, tk.END)
    for item in reversed(history[-7:]):
        history_box.insert(0, item)

def save_history(exp, res):
    with open("history.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([exp, res])

def use_history(event):
    global expression
    if history_box.curselection():
        selected = history_box.get(history_box.curselection())
        expression = selected.split("=")[0].strip()
        input_text.set(expression)

# ---------------- THEME ----------------
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    
    if dark_mode:
        root.config(bg="#1e1e1e")
        entry.config(bg="#2d2d2d", fg="white")
    else:
        root.config(bg="white")
        entry.config(bg="lightgray", fg="black")

# ---------------- KEYBOARD ----------------
def key_event(event):
    key = event.char
    if key in "0123456789+-*/.":
        press(key)
    elif event.keysym == "Return":
        calculate()
    elif event.keysym == "BackSpace":
        backspace()

root.bind("<Key>", key_event)

# ---------------- UI ----------------
input_text = tk.StringVar()

entry = tk.Entry(root, textvariable=input_text,
                 font=('Arial', 20),
                 bd=10, relief=tk.FLAT,
                 justify='right',
                 bg="#2d2d2d", fg="white")
entry.pack(fill="both", ipadx=8, ipady=15, padx=10, pady=10)

# Buttons Frame
frame = tk.Frame(root, bg="#1e1e1e")
frame.pack()

buttons = [
    ('7',1,0), ('8',1,1), ('9',1,2), ('/',1,3),
    ('4',2,0), ('5',2,1), ('6',2,2), ('*',2,3),
    ('1',3,0), ('2',3,1), ('3',3,2), ('-',3,3),
    ('0',4,0), ('.',4,1), ('+',4,2), ('=',4,3),
]

for (text, row, col) in buttons:
    if text == "=":
        action = calculate
        color = "#00adb5"
    else:
        action = lambda x=text: press(x)
        color = "#393e46"

    tk.Button(frame, text=text, width=5, height=2,
              font=('Arial', 12), bg=color, fg="white",
              command=action).grid(row=row, column=col, padx=5, pady=5)

# Scientific Buttons
sci_frame = tk.Frame(root)
sci_frame.pack()

tk.Button(sci_frame, text="sin", command=lambda: scientific("sin")).grid(row=0,column=0)
tk.Button(sci_frame, text="cos", command=lambda: scientific("cos")).grid(row=0,column=1)
tk.Button(sci_frame, text="tan", command=lambda: scientific("tan")).grid(row=0,column=2)
tk.Button(sci_frame, text="√", command=lambda: scientific("sqrt")).grid(row=0,column=3)
tk.Button(sci_frame, text="log", command=lambda: scientific("log")).grid(row=1,column=0)

# Memory Buttons
mem_frame = tk.Frame(root)
mem_frame.pack()

tk.Button(mem_frame, text="M+", command=memory_add).grid(row=0,column=0)
tk.Button(mem_frame, text="M-", command=memory_sub).grid(row=0,column=1)
tk.Button(mem_frame, text="MR", command=memory_recall).grid(row=0,column=2)
tk.Button(mem_frame, text="MC", command=memory_clear).grid(row=0,column=3)

# Extra Buttons
tk.Button(root, text="C", bg="red", fg="white", command=clear).pack(fill="x")
tk.Button(root, text="⌫", command=backspace).pack(fill="x")
tk.Button(root, text="Toggle Theme", command=toggle_theme).pack(fill="x")

# History
history_box = tk.Listbox(root, height=7)
history_box.pack(fill="both", padx=10, pady=5)
history_box.bind("<<ListboxSelect>>", use_history)

# Run
root.mainloop() 
