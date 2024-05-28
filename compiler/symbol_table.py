from .exceptions import *
from collections import ChainMap
import copy


class NextCounter():

    def __init__(self, init_value=0):
        self.value = init_value

    def next(self):
        to_return = self.value
        self.value += 1
        return to_return



class MemoryEntry():
    '''
    A class to store type information about what is stored
    at particular memory locations
    '''

    bool_types = ['bool', 'bool[']
    int_types = ['int', 'int[']
    real_types = [ 'float', 'float[']
    char_types = ['char', 'char[']

    src2interm_types = {
        'bool':'%',
        'int':'%',
        'float':'!',
        'char':'$',
        'int[':'@',
        'float[':'@',
        'char[':'@',
        'bool[':'@',
    }

    def __init__(self, loc, dtype):
        self.loc = loc
        self.dtype = dtype
        

    def is_scalar(self):
        return not self.dtype[-1] == '['

    def is_numeric(self):
        if self.dtype == 'numeric' or self.dtype == 'numeric[':
            return True
        return self.dtype in self.int_types or self.dtype in self.real_types

    def is_char(self):
        return self.dtype in self.char_types

    def is_bool(self):
        return self.dtype in self.bool_types

    def is_int(self):
        return self.dtype in self.int_types

    def is_real(self):
        return self.dtype in self.real_types

    def itype(self):
        return self.src2interm_types[self.dtype]

    def arr_dtype(self):
        if self.is_scalar():
            raise Exception('MemoryEntry: Array type requested for non-array')
        return self.dtype[:-1]

    def arr_elem_itype(self):
        if self.is_scalar():
            raise Exception('MemoryEntry: Array type requested for non-array')
        return self.src2interm_types[self.dtype[:-1]]


    def __str__(self):
        var_type = 's' if self.is_scalar() else 'a'
        prefix = self.src2interm_types[self.dtype]
        return f'{prefix}{var_type}{self.loc}'
        



class CompilerSymbolTable():

    def __init__(self):
        self.var_identifiers = ChainMap()  # Identifier to memory map
        self.memory = {}
        self.next_memloc = NextCounter(1)  # Start at 1
        self.break_label = []
        self._init_labels()



    def _init_labels(self):
        '''
        Initialize the map that keeps track of label name numbers
        '''
        prefixes = [
            'if-end', 'if-else',
            'for-start', 'for-end',
            'while-start', 'while-end'
        ]
        self.next_labels = {k:NextCounter(0) for k in prefixes}


    def mem_lookup(self, var):
        loc = int(var[2:])
        return self.memory[loc]


    def lookup(self, ident):
        """Return memory location of identifier"""
        if not self.is_declared(ident):
            raise UndeclaredError(f'{ident} is undeclared')
        else:
            return self.var_identifiers[ident]


    def is_declared(self, ident):
        """Return true if a variable identifier is declared"""
        return ident in self.var_identifiers


    def is_declared_in_scope(self, ident):
        return ident in self.var_identifiers.maps[0]


    def declare(self, ident, dtype):
        """Declare a variable identifier and return memory location"""
        if not self.is_declared_in_scope(ident):
            new_mem = self.alloc(dtype)
            self.var_identifiers[ident] = new_mem
            return new_mem
        else:
            raise RedeclarionError(f"Redeclaring identifier {ident}")


    def alloc(self, dtype):
        """Allocate a new scalar location in memory"""
        new_loc = self.next_memloc.next()
        new_memory = MemoryEntry(new_loc, dtype)
        self.memory[new_loc] = new_memory
        return new_memory


    def next_if_labels(self):
        '''
        Return the next set of labels for if-statements
        '''
        label_end = 'if-end-' + str(self.next_labels['if-end'].next())
        label_else = 'if-else-' + str(self.next_labels['if-else'].next())
        return label_end, label_else


    def next_while_labels(self):
        '''
        Return the next labels for while-statements
        '''
        label_start = 'while-start-' + str(self.next_labels['while-start'].next())
        label_end = 'while-end-' + str(self.next_labels['while-end'].next())
        return label_start, label_end


    def next_for_labels(self):
        '''
        Return the next labels for for-statements
        '''
        label_start = 'for-start' + str(self.next_labels['for-start'].next())
        label_end = 'for-end' + str(self.next_labels['for-start'].next())
        return label_start, label_end


    def push_scope(self):
        self.var_identifiers = self.var_identifiers.new_child()

    def pop_scope(self):
        self.var_identifiers.maps = self.var_identifiers.maps[1:]


    def push_scope_conditional(self):
        self.push_scope()


    def pop_scope_conditional(self):
        self.pop_scope()


    def push_scope_loop(self, end_label=None):
        '''
        Push a new scope onto the identifier chain map
        '''
        self.push_scope()
        self.break_label.append(end_label)


    def pop_scope_loop(self):
        '''
        Pop a scope off the identifier chain map
        '''
        self.pop_scope()
        self.break_label.pop()

    
    def break_to_label(self):
        return self.break_label[-1]


    def check_is_array(self, mem):
        if mem.is_scalar():
            raise CompilerTypeMismatchError()


    def check_type(self, expected, *found, where='', strict=True, as_arr_element=False):
        '''
        A function to check types

        Expected is the expected type.

        Found is an n-ary list of data types we want to see if match expected's type

        where is simply a string you can pass to give more information about where the type
        checking is happening

        strict informs this function that numeric types should be treated as strictly int or float
        '''
        
        if isinstance(expected, str):
            expected = MemoryEntry(-1, expected)
        else:
            expected = copy.copy(expected)

        for ndx, entry in enumerate(found):
            if not as_arr_element and not expected.dtype == entry.dtype:
                if not strict and expected.is_numeric() and entry.is_numeric():
                    if expected.is_real() or entry.is_real():
                        expected.dtype = 'float'
                else:
                    raise CompilerTypeMismatchError(expected.dtype, entry.dtype, where)
            elif as_arr_element and not expected.arr_dtype() == entry.dtype:
                raise CompilerTypeMismatchError(expected.dtype, entry.dtype, where)
        return expected.dtype if expected.dtype != 'numeric' else 'int'
