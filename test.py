def check_cond():
    x=12
    y=12
    
    if x>y:
        print("x>y")
    elif x<y:
        print("x<y")
    else:
        print("x==y")
    
def for_loop():
    for i in range(7):
        print(i)

def while_loop():
    i = 0
    while i<5:
        print(i)
        i = i+1
    
dodawanie = compile("print(5+10)", "test.py", "exec")

odejmowanie = compile("print(27-13)", "test.py", "exec")

mnozenie = compile("print(27*10)", "test.py", "exec")

dzielenie = compile("print(26/13)", "test.py", "exec")

modulo = compile("print(26%5)", "test.py", "exec")

