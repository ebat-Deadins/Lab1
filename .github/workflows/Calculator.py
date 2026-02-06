import math
import tkinter
button_values = [
    ["R→dg", "sin", "cos", "tan", "ctg"], ##rad→deg
    ["dg→R","lg", "ln", "logx(y)", "π"],
    ["+/-","AC", "⌫", "%", "÷"], 
    ["x!","7", "8", "9", "×"], 
    ["1/x","4", "5", "6", "-"],
    ["√x","1", "2", "3", "+"],
    ["x^y","e", ".", "0", "="]
]
history = []
right_symbols = ["+/-","÷", "×", "-", "+", "=","AC", "⌫", "%"]
top_symbols = ["","deg", "sin", "cos", "tan","√x","lg", "ln", "(", ")"
            ,"x^y","x!","1/x","π", "e", "ctg","R→dg","dg→R","logx(y)"]
row_count = len(button_values) 
column_count = len(button_values[0]) 
color_light_gray = "#D4D4D2"
color_black = "#1C1C1C"
color_dark_gray = "#505050"
color_orange = "#FF9500"
color_white = "white"
#window setup
window = tkinter.Tk() #create the window
window.title("Calculator")
window.resizable(False, False) # sungahgui: prevent resizing the window
frame = tkinter.Frame(window)
label = tkinter.Label(frame, text="0", font=("Arial", 45), background=color_black,foreground=color_white, anchor="e", width=column_count)
#anchor = e -> east (right align) toogoo baruun zugruu shahah
#widht = column_count -> label-iin urtiig button-iin urttai tentsuuleh
#foreground = text color
label.grid(row=0, column=0, columnspan=column_count, sticky="we")
#sticy = we -> west-east (fill horizontal)
#columnspan = column_count -> button-uuudiin deer bugdiig ni hangah
frame.pack() #frame window deer gargah
for row in range(row_count):
    for column in range(column_count):
        value = button_values[row][column]
        button = tkinter.Button(frame, text=value, font=("Arial", 30),
                                width=column_count, height=1,
                                command=lambda value=value: button_clicked(value))
        
        if value in top_symbols:
            button.config(foreground=color_light_gray, background=color_dark_gray)
        elif value in right_symbols:
            button.config(foreground=color_white, background=color_orange)
        else:
            button.config(foreground=color_white, background=color_dark_gray)
        # ungu nemj ugsun bna
        button.grid(row=row+1, column=column)
#A+B, A-B, A*B, A/B
A = "0"
operator = None
B = None
dark_mode = True
def clear_all(): #AC button function
    global A, B, operator #global huvisagch n def func dotor bish harin gaduuraa label deer toogoo hadgalna
    A = "0"
    operator = None
    B = None
def remove_zero_decimal(num):
    try:
        num = float(num) # err orj irvel gatsna ternees sergiilne  err/ 2= 4.0 -> 4
        if num.is_integer():
            return str(int(num))
        return str(num)
    except:
        return "Error"

def on_enter(button, hover_color): #hover color
    button.config(background=hover_color)
def on_leave(event):
    event.widget.config(background=event.widget.default_bg)


def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        bg = color_black
        fg = color_white
    else:
        bg = "#F0F0F0"
        fg = "black"
    frame.config(bg=bg)
    label.config(bg=bg, fg=fg)

def show_history():
    top = tkinter.Toplevel(window)
    top.title("History")
    msg = "\n".join(history[-10:]) if history else "No history yet"
    tkinter.Label(top, text=msg, font=("Segoe UI", 14)).pack(padx=10, pady=10)

def key_event(event):
    key = event.char
    if key in "0123456789":
        button_clicked(key)
    elif key == ".":
        button_clicked(".")
    elif key == "+":
        button_clicked("+")
    elif key == "-":
        button_clicked("-")
    elif key == "*":
        button_clicked("×")
    elif key == "/":
        button_clicked("÷")
    elif event.keysym == "Return":
        button_clicked("=")
    elif event.keysym == "BackSpace":
        button_clicked("⌫")
    elif event.keysym == "Escape":
        button_clicked("AC")
    elif event.keysym == "percent":
        button_clicked("%")
    elif event.keysym == "^":
        button_clicked("x^y")
    elif event.keysym == "e":
        button_clicked("e")
    elif event.keysym == "h":
        show_history()
    else:
        return

window.bind("<Key>", key_event)
def button_clicked(value):
    import math
    global right_symbols, top_symbols, label, A, B, operator
    if value in right_symbols:
        if value == "=":
            if A is not None and operator is not None:
                B = label["text"]
                numA = float(A)
                numB = float(B)
                if operator == "+":
                    label["text"] = remove_zero_decimal(numA + numB)
                elif operator == "-":
                    label["text"] = remove_zero_decimal(numA - numB)
                elif operator == "×":
                    label["text"] = remove_zero_decimal(numA * numB)
                elif operator == "^":
                    label["text"] = remove_zero_decimal(numA ** numB)
                elif operator == "÷":
                    if numB == 0:
                        label["text"] = "Error"
                    else:
                        label["text"] = f"{float(remove_zero_decimal(numA / numB)):.10g}" #truncate long decimals
                elif operator == "logx(y)":
                    if numA <= 0 or numA == 1 or numB <= 0:
                        label["text"] = "Error"
                    else:
                        result = math.log(numB, numA)
                        label["text"] = f"{result:.10g}"
                        history.append(f"log{remove_zero_decimal(numB)}({remove_zero_decimal(numA)}) = {label['text']}")
                        return
                result = remove_zero_decimal(float(label["text"]))
                label["text"] = result
                history.append(f"{A} {operator} {B} = {result}")
                clear_all()
        elif value == "AC":
            clear_all()
            label["text"] = "0"
        elif value == "%":
            result = float(label["text"]) / 100
            label["text"] = remove_zero_decimal(result)           
        elif value == "+/-":
            result = float(label["text"]) * -1
            label["text"] = remove_zero_decimal(result)
        elif value ==  "⌫":
            current_text = label["text"]
            if len(current_text) > 1:
                label["text"] = current_text[:-1] #remove last character
            else:
                label["text"] = "0"
        elif value in "+-×÷": #500 + *
            if operator is None:
                A = label["text"]
                B = "0"
                label["text"] = B
            operator = value
    elif value in top_symbols:
        if value == "x!":
            A = label["text"]
            if float(label["text"]) < 0 or not float(label["text"]).is_integer():
                label["text"] = "Error"
                history.append(f"{A}! = Error")
                return
            result = math.factorial(int(float(label["text"])))
            label["text"] = remove_zero_decimal(result)
            history.append(f"{A}! = {result}")
        elif value == "1/x":
            try:
                x = float(label["text"])
                if x == 0:
                    label["text"] = "Error"
                    history.append(f"1/{remove_zero_decimal(x)} = Error")
                    return
                else:
                    result = 1 / x
                if abs(result) > 1e15:
                    label["text"] = "Error"
                else:
                    label["text"] = f"{result:.10g}"  # clean formatting
            except ValueError:
                label["text"] = "Error"
        elif value == "√x":
            A = label["text"]
            if float(label["text"]) < 0:
                label["text"] = "Error"
                history.append(f"√{A} = Error")
                return
            result = float(label["text"]) ** 0.5
            label["text"] = f"{result:.10g}"
            history.append(f"√{A} = {result}")
        elif value == "x^y":
            A = label["text"]
            label["text"] = "0"
            operator = "^"
        elif value == "e":
            label["text"] = f"{float(remove_zero_decimal(math.e)):.10g}"
            history.append(f"e = {remove_zero_decimal(math.e)}")
        elif value == "π":
            label["text"] = f"{float(remove_zero_decimal(math.pi)):.10g}"
            history.append(f"π = {float(remove_zero_decimal(math.pi)):.10g}")
        elif value == "lg":
            A = label["text"]
            result = math.log10(float(label["text"]))
            label["text"] = f"{float(remove_zero_decimal(result)):.10g}"
            history.append(f"lg({A}) = {label['text']}")
        elif value == "ln":
            A = label["text"]
            if float(label["text"]) <= 0:
                label["text"] = "Error"
                history.append(f"ln({A}) = Error")
                return
            result = math.log(float(label["text"]))
            label["text"] = f"{float(remove_zero_decimal(result)):.10g}"
            ##history
            result_str = remove_zero_decimal(float(label["text"]))
            label["text"] = result_str
            history.append(f"ln({A}) = {result_str}")
        elif value == "sin":
            A = label["text"]
            if A == "0":
                label["text"] = "0"
                history.append(f"sin({A}) = 0")
                return
            elif A == "180":
                label["text"] = "0"
                history.append(f"sin({A}) = 0")
                return
            result = math.sin(math.radians(float(label["text"])))
            label["text"] = f"{result:.10g}"
            history.append(f"sin({A}) = {label['text']}")
        elif value == "cos":
            A = label["text"]
            if A == "90":
                label["text"] = "0"
                history.append(f"cos({A}) = 0")
                return
            result = math.cos(math.radians(float(label["text"])))
            label["text"] = f"{result:.10g}"
            history.append(f"cos({A}) = {label['text']}")
        elif value == "tan":
            A = label["text"]
            angle = float(label["text"])
            if abs(angle % 180 - 90) < 1e-9:
                label["text"] = "Error"
                history.append(f"tan({A}) = Error")
                return
            result = math.tan(math.radians(angle))
            if len(str(result)) > 15: #if result is too long, truncate it
                label["text"] = f"{float(remove_zero_decimal(result)):.10g}"
            history.append(f"tan({A}) = {label['text']}")
        elif value == "ctg":
            A = label["text"]
            angle = float(label["text"])
            if angle % 180 == 0:
                label["text"] = "Error"
                history.append(f"ctg({A}) = Error")
                return
            result = 1 / math.tan(math.radians(angle))
            label["text"] = f"{result:.10g}"
            history.append(f"ctg({A}) = {label['text']}")
        elif value == "R→dg":
            try:
                A = float(label["text"])
                result = math.degrees(A)
                label["text"] = f"{result:.10g}"
                history.append(f"rad → deg ({A}) = {label['text']}")
            except ValueError:
                label["text"] = "Error"
        elif value == "dg→R":
            try:
                A = float(label["text"])
                result = math.radians(A)
                label["text"] = f"{result:.10g}"
                history.append(f"deg → rad ({A}) = {label['text']}")
            except ValueError:
                label["text"] = "Error"
        elif value == "logx(y)":
            if operator is None:
                A = label["text"]
                label["text"] = "0"
                B = "0"
            operator = "logx(y)"
    else: #digits or .
        if value == ".":
            if value not in label["text"]:
                label["text"] += value
        elif value in "0123456789":
            if label["text"] == "0":
                label["text"] = value #replace 0
            else:
                label["text"] += value #append digit
tkinter.Button(frame, text="🌙", font=("Segoe UI", 12),
            command=toggle_theme).grid( sticky="we", row=0, column=0)
tkinter.Button(frame, text="History", font=("Segoe UI", 10),
            command=show_history).grid(row=row_count+1, column=0, columnspan=column_count, sticky="we")
#center the window
window.update() #update window with the new size dimensions
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))
#format "(w)x(h)+(x)+(y)"

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
window.mainloop()