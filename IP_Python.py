class VirtualMachine(object): #główny obiekt interpretera
    def __init__(self):
        self.frames = []   # stos z ramkami
        self.frame = None  # aktualna
        self.return_value = None

    def run(self, code, global_names=None, local_names=None):
        frame = self.make_frame(code, global_names=global_names, 
                                local_names=local_names)
        self.run_frame(frame)
        
    #obsługa stosu ramek    
    def make_fr():
        pass
    
    def push_fr(self, frame):
        self.frames.append(frame)
    
    def pop_fr(self):
        self.frames.pop()
        if(len(self.frames)==0):
            self.frame = None
        else:
            self.frame = self.frames[-1]
    
    def run_fr():
        pass
    
    #operacje na stosie danych w ramce
    def top(self):
        return self.frame.stack[-1]

    def pop(self):
        return self.frame.stack.pop()

    def push(self, *x):
        self.frame.stack.extend(x)

    def popn(self, n):
        if n:
            ret = self.frame.stack[-n:]
            self.frame.stack[-n:] = []
            return ret
        else:
            return []
        
    def parse(self): #konwersja argumentów
        pass
    
    def exe_operations(self, byte_name, argument): #wykonuje daną operację z argumentami
        pass

class Frame(object): #pojedyncza ramka danych
    def __init__(self, code_obj, global_names, local_names, prev_frame):
        self.code_obj = code_obj
        self.global_names = global_names
        self.local_names = local_names
        self.prev_frame = prev_frame
        self.stack = []
        if prev_frame:
            self.builtin_names = prev_frame.builtin_names
        else:
            self.builtin_names = local_names['__builtins__']
            if hasattr(self.builtin_names, '__dict__'):
                self.builtin_names = self.builtin_names.__dict__

        self.last_instruction = 0
        self.block_stack = []
        
class Function(object): #sterowanie ramkami tworzonymi przez wywołanie funkcji
    
    def __init__():
        pass

    def __call__():
        pass
