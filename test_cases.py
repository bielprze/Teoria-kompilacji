vm = VirtualMachine()
    
code_obj = compile("x=4\nif (x%2)==0:\n    print(1)\n", "filename", "exec")

code_obj2 = compile("for i in range(3):\n    print(i)", "filename", "exec")


code_obj3 = compile("if 1==0:\n     print(1)\nelse:\n       print(0)", "filename", "exec")


print("Test with exec: ")
exec(code_obj)

print("Test with vm: ")
vm.run(code_obj)