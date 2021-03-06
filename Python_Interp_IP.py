import dis
import operator
import types
import inspect
import sys
import collections as c

Block = c.namedtuple("Block", "type, handler, level")

#pojedyncza ramka danych
class Frame(object):
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
        
#sterowanie ramkami tworzonymi przez wywołanie funkcji    
class Function(object): 
    
    __slots__ = [
        'func_code', 'func_name', 'func_defaults', 'func_globals',
        'func_locals', 'func_dict', 'func_closure',
        '__name__', '__dict__', '__doc__',
        '_vm', '_func',
        ]
     
    def __init__(self, name, code, globs, defaults, closure, vm):
        self._vm = vm
        self.func_code = code
        self.func_name = self.__name__ = name or code.co_name
        self.func_defaults = tuple(defaults)
        self.func_globals = globs
        self.func_locals = self._vm.frame.local_names
        self.__dict__ = {}
        self.func_closure = closure
        self.__doc__ = code.co_consts[0] if code.co_consts else None

        kw = {
            'argdefs': self.func_defaults,
        }
        if closure:
            kw['closure'] = tuple(make_cell(0) for _ in closure)
        self._func = types.FunctionType(code, globs, **kw)

    def __call__(self, *args, **kwargs):
        callargs = inspect.getcallargs(self._func, *args, **kwargs)
        frame = self._vm.make_frame(
            self.func_code, callargs, self.func_globals, {}
        )
        return self._vm.run_fr(frame)

def make_cell(value):
    fn = (lambda x: lambda: x)(value)
    return fn.__closure__[0]


#główny obiekt interpretera
class VirtualMachine(object): 
    def __init__(self):
        self.frames = []   # stos z ramkami
        self.frame = None  # aktualna
        self.return_value = None
        
    def run(self, code, global_names=None, local_names=None):
        frame = self.make_frame(code, global_names=global_names, local_names=local_names)
        self.run_fr(frame)

        
    #obsługa stosu ramek    
    def make_frame(self, code, callargs={}, global_names=None, local_names=None):
        if global_names is not None and local_names is not None:
            local_names = global_names
        elif self.frames:
            global_names = self.frame.global_names
            local_names = {}
        else:
            global_names = local_names = {
                '__builtins__': __builtins__,
                '__name__': '__main__',
                '__doc__': None,
                '__package__': None,
            }
        local_names.update(callargs)
        frame = Frame(code, global_names, local_names, self.frame)
        return frame
    
    def push_fr(self, frame):
        self.frames.append(frame)
        self.frame = frame
    
    def pop_fr(self):
        self.frames.pop()
        if(len(self.frames)==0):
            self.frame = None
        else:
            self.frame = self.frames[-1]
    
        
    def run_fr(self, frame):
        self.push_fr(frame)
        while True:
            byte_name, arguments = self.parse()

            why = self.dispatch(byte_name, arguments)
            
            while why and frame.block_stack:
                why = self.manage_block_stack(why)

            if why:
                break

        self.pop_fr()
        
        return self.return_value
    
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

    def jump(self, jump):
        self.frame.last_instruction = jump
      
    #konwersja argumentów 
    def parse(self): 
        f = self.frame
        opoffset = f.last_instruction
        byteCode = f.code_obj.co_code[opoffset]
        f.last_instruction += 1
        byte_name = dis.opname[byteCode]
        if byteCode >= dis.HAVE_ARGUMENT:
            arg = f.code_obj.co_code[f.last_instruction:f.last_instruction+2]  
            f.last_instruction += 2   
                        
            arg_val = arg[0]
            if byteCode in dis.hasconst:  
                arg = f.code_obj.co_consts[arg_val]
            elif byteCode in dis.hasname:  
                arg = f.code_obj.co_names[arg_val]
            elif byteCode in dis.haslocal: 
                arg = f.code_obj.co_varnames[arg_val]
            elif byteCode in dis.hasjrel:  
                arg = f.last_instruction + arg_val
            else:
                arg = arg_val
            argument = [arg]
        else:
            argument = []

        return byte_name, argument
    
    #operacja dla danej instrukcji
    def dispatch(self, byte_name, argument): 
        why = None
        
        try:
            bytecode_fn = getattr(self, 'byte_%s' % byte_name, None)
            if bytecode_fn is None:
                if byte_name.startswith('UNARY_'):
                    self.unaryOperator(byte_name[6:])
                else:
                    self.binaryOperator(byte_name[7:])
            else:
                why = bytecode_fn(*argument)
        except:
            self.last_exception = sys.exc_info()[:2] + (None,)
            why = 'exception'

        return why  
        
    # manipulacje block stackiem
    def block_push(self, b_type, handler=None):
        stack_height = len(self.frame.stack)
        self.frame.block_stack.append(Block(b_type, handler, stack_height))

    def block_pop(self):
        return self.frame.block_stack.pop()

    def block_unwind(self, block):
        if block.type == 'except-handler':
            # The exception itself is on the stack as type, value, and traceback.
            offset = 3  
        else:
            offset = 0

        while len(self.frame.stack) > block.level + offset:
            self.pop()

        if block.type == 'except-handler':
            traceback, value, exctype = self.popn(3)
            self.last_exception = exctype, value, traceback

    def manage_block_stack(self, why):
        frame = self.frame
        block = frame.block_stack[-1]
        if block.type == 'loop' and why == 'continue':
            self.jump(self.return_value)
            why = None
            return why

        self.block_pop()
        self.block_unwind(block)

        if block.type == 'loop' and why == 'break':
            why = None
            self.jump(block.handler)
            return why

        if (block.type in ['setup-except', 'finally'] and why == 'exception'):
            self.block_push('except-handler')
            exctype, value, tb = self.last_exception
            self.push(tb, value, exctype)
            self.push(tb, value, exctype) # yes, twice
            why = None
            self.jump(block.handler)
            return why

        elif block.type == 'finally':
            if why in ('return', 'continue'):
                self.push(self.return_value)

            self.push(why)

            why = None
            self.jump(block.handler)
            return why
        return why
   


    #instrukcje
    def byte_LOAD_CONST(self, const):
        self.push(const)

    def byte_POP_TOP(self):
        self.pop()

    def byte_LOAD_NAME(self, name):
        frame = self.frame
        if name in frame.local_names:
            val = frame.local_names[name]
        elif name in frame.global_names:
            val = frame.global_names[name]
        else:
            val = frame.builtin_names[name]
        self.push(val)

    def byte_STORE_NAME(self, name):
        self.frame.local_names[name] = self.pop()

    def byte_LOAD_FAST(self, name):
        if name in self.frame.local_names:
            val = self.frame.local_names[name]
        
        self.push(val)

    def byte_STORE_FAST(self, name):
        self.frame.local_names[name] = self.pop()

    def byte_LOAD_GLOBAL(self, name):
        f = self.frame
        if name in f.global_names:
            val = f.global_names[name]
        else:
            val = f.builtin_names[name]
        self.push(val)
        
    BINARY_OPERATORS = {
        'MULTIPLY': operator.mul,
        'FLOOR_DIVIDE': operator.floordiv,
        'TRUE_DIVIDE':  operator.truediv,
        'MODULO':   operator.mod,
        'ADD':      operator.add,
        'SUBTRACT': operator.sub,
        'AND':      operator.and_,
        'OR':       operator.or_,
        }
    
    def binaryOperator(self, op):
        x, y = self.popn(2)
        self.push(self.BINARY_OPERATORS[op](x, y))

    def byte_MAKE_FUNCTION(self, argc):
        name = self.pop()
        code = self.pop()
        defaults = self.popn(argc)
        globs = self.frame.global_names
        fn = Function(name, code, globs, defaults, None, self)
        self.push(fn)

    def byte_CALL_FUNCTION(self, arg):
        lenKw, lenPos = divmod(arg, 256) # KWargs not supported here
        posargs = self.popn(lenPos)

        func = self.pop()
        frame = self.frame
        retval = func(*posargs)
        self.push(retval)

    def byte_RETURN_VALUE(self):
        self.return_value = self.pop()
        if self.frame.generator:
            self.frame.generator.finished = True
        return "return"
    
    def PRINT_ANSWER(self):
        answer = self.stack.pop()
        print(answer)
        

    def byte_JUMP_FORWARD(self, jump):
        self.jump(jump)

    def byte_JUMP_ABSOLUTE(self, jump):
        self.jump(jump)

    def byte_POP_JUMP_IF_TRUE(self, jump):
        val = self.pop()
        if val:
            self.jump(jump)

    def byte_POP_JUMP_IF_FALSE(self, jump):
        val = self.pop()
        if not val:
            self.jump(jump)
            
            
    COMPARE_OPERATORS = [
        operator.lt,
        operator.le,
        operator.eq,
        operator.ne,
        operator.gt,
        operator.ge,
    ]

    def byte_COMPARE_OP(self, opnum):
        x, y = self.popn(2)
        self.push(self.COMPARE_OPERATORS[opnum](x, y))
        
    def byte_SETUP_LOOP(self, dest):
        self.block_push('loop', dest)

    def byte_GET_ITER(self):
        self.push(iter(self.pop()))

    def byte_FOR_ITER(self, jump):
        iterobj = self.top()
        try:
            v = next(iterobj)
            self.push(v)
        except StopIteration:
            self.pop()
            self.jump(jump)

    def byte_BREAK_LOOP(self):
        return 'break'

    def byte_POP_BLOCK(self):
        self.block_pop()


