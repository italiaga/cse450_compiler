from compiler.interpreter.ast_nodes import CommandListNode


class ASTNode:
    
    def __init__(self, children):
        self.children = children

    def compile(self, st, output):
        raise NotImplementedError(self.__class__, 'is not implemented')
    
    def interpret(self, st):
        raise NotImplementedError(self.__class__, 'is not implemented')


class ExprNode(ASTNode):
    pass

class StmtNode(ASTNode):
    pass


class StartNode(ASTNode):
    """
    children[0] : CmdListNode
    """
    def compile(self, st, output):
        output += ['VAL_COPY @10000 @s0']
        self.children[0].compile(st, output)


class CmdListNode(ASTNode):
    """
    self.children : list of statements
    """
    def compile(self, st, output):
        for child in self.children:
            child.compile(st, output)



class StmtDeclare(StmtNode):
    """
    children[0]: dtype
    children[0]: identifier
    """
    def compile(self, st, output):
        dtype, id = self.children[0], self.children[1]
        st.declare(id, dtype)


class StmtDeclareAssign(StmtNode):
    """
    children[0]: dtype
    children[1]: assign node
    """
    def compile(self, st, output):
        id = self.children[1].children[0]
        dtype = self.children[0]
        st.declare(id, dtype)
        self.children[1].compile(st, output)



class ExprAssignNode(StmtNode):  #Project differs!
    """
    children[0]: ID lexeme
    children[1]: expression to assign
    """
    def compile(self, st, output):
        mem_expr = self.children[1].compile(st, output)
        mem_id = st.lookup(self.children[0])
        if mem_expr:
            # If the value is not None, then we know it's a scalar expression
            st.check_type(mem_id, mem_expr)
            output += [f'VAL_COPY {mem_expr} {mem_id}']
        else:
            #It's a expr_list (expr list returns None on compile)
            # We have to handle assignment ourselves by bulding the array
            expr_list = self.children[1].children
            num_expr = len(expr_list)
            output += [f'VAL_COPY @s0 {mem_id}']
            output += [f'ADD @s0 %1 @s0']
            output += [f'ADD @s0 %{num_expr} @s0']
            output += [f'AR_SET_SZ {mem_id} %{num_expr}']
            for ndx, expr in enumerate(expr_list):
                mem_expr = expr.compile(st, output)
                st.check_type(mem_id, mem_expr, as_arr_element=True)
                output += [f'AR_SET_NDX {mem_id} %{ndx} {mem_expr}']
        return mem_id



class StmtPrint(StmtNode):
    """
    children[0]: ExprListNode
    """
    def compile(self, st, output):
        for expr in self.children[0].children:
            mem_result = expr.compile(st, output)
            if mem_result.is_scalar():
                self.print_element(st, output, mem_result)
            else:
                self.print_array(st, output, mem_result)


    def print_element(self, st, output, mem_result):
        if mem_result.is_int() or mem_result.is_bool():
            output += [f'OUT_INT {mem_result}']
        elif mem_result.is_real():
            output += [f'OUT_FLOAT {mem_result}']
        elif mem_result.is_char():
            output += [f'OUT_CHAR {mem_result}']
        else:
            raise NotImplementedError('Unable to print out {mem_result}')


    def print_array(self, st, output, mem_ptr):
        mem_ndx = st.alloc('int')
        mem_sz = st.alloc('int')
        mem_test = st.alloc('bool')
        mem_elem = st.alloc(mem_ptr.arr_dtype())
        label_start, label_end = st.next_while_labels()
        output += [f'VAL_COPY %0 {mem_ndx}']
        output += [f'AR_GET_SZ {mem_ptr} {mem_sz}']
        output += [f'{label_start}:']
        output += [f'TEST_LESS {mem_ndx} {mem_sz} {mem_test}']
        output += [f'JUMP_IF_0 {mem_test} {label_end}']
        output += [f'AR_GET_NDX {mem_ptr} {mem_ndx} {mem_elem}']
        self.print_element(st, output, mem_elem)
        output += [f'ADD {mem_ndx} %1 {mem_ndx}']
        output += [f'JUMP {label_start}']
        output += [f'{label_end}:']



class StmtPrintln(StmtPrint):
    """
    children[0]: ExprListNode
    """    
    def compile(self, st, output):
        super().compile(st, output)
        output += [f'OUT_CHAR $\'%n\'']
        


class ExprID(ExprNode):
    """
    children[0]: ID lexeme
    """
    def compile(self, st, output):
        mem_id = st.lookup(self.children[0])
        return mem_id



class ExprIntLiteralNode(ExprNode):
    """
    children[0]: integer lexeme
    """
    def compile(self, st, output):
        mem_number = st.alloc('int')
        output += [f'VAL_COPY %{self.children[0]} {mem_number}']
        return mem_number


class ExprBoolLiteralNode(ExprNode):
    """
    children[0]: bool lexeme
    """
    def compile(self, st, output):
        mem_bool = st.alloc('bool')
        lexeme = self.children[0]
        bool_val = 0 if lexeme == 'False' else 1
        output += [f'VAL_COPY %{bool_val} {mem_bool}']
        return mem_bool



class ExprFloatLiteralNode(ExprNode):
    """
    children[0]: float lexeme
    """
    def compile(self, st, output):
        mem_number = st.alloc('float')
        output += [f'VAL_COPY !{self.children[0]} {mem_number}']      
        return mem_number



class ExprCharLiteralNode(ExprNode):
    """
    children[0]: char lexeme
    """
    def compile(self, st, output):
        mem_char = st.alloc('char')
        output += [f'VAL_COPY ${self.children[0]} {mem_char}']
        return mem_char



class ExprListNode(ExprNode):
    """
    children: variable length list of expr nodes
    """
    def compile(self, st, output):
        pass


class ExprMathNegate(ExprNode):
    """
    children[0]: expr to interpret
    """
    def compile(self, st, output):
        mem_expr = self.children[0].compile(st, output)
        out_type = st.check_type('numeric', mem_expr, strict=False)
        mem_result = st.alloc(out_type)
        output += [f'MUL %-1 {mem_expr} {mem_result}']
        return mem_result



class ExprMathBinary(ExprNode):
    """
    children[0]: lhs operand
    children[1]: operation
    children[2]: rhs operand
    """
    def compile(self, st, output):
        op = self.children[1]
        mem_lhs = self.children[0].compile(st, output)
        mem_rhs = self.children[2].compile(st, output)
        out_type = st.check_type('numeric', mem_lhs, mem_rhs, strict=False)
        mem_result = st.alloc(out_type)
        if op == '+':
            output += [f'ADD {mem_lhs} {mem_rhs} {mem_result}']
        elif op == '-':
            output += [f'SUB {mem_lhs} {mem_rhs} {mem_result}']
        elif op == '*':
            output += [f'MUL {mem_lhs} {mem_rhs} {mem_result}']
        elif op == '/':
            if out_type == 'int':
                output += [f'IDIV {mem_lhs} {mem_rhs} {mem_result}']
            else:
                output += [f'DIV {mem_lhs} {mem_rhs} {mem_result}']
        elif op == '%':
            if out_type == 'int':
                output += [f'MOD {mem_lhs} {mem_rhs} {mem_result}']
            else:
                raise Exception('Modulo must be performed on integers only.')
        else:
            raise NotImplementedError('MathBinOp ', op, 'not defined.')
        return mem_result
        



class ExprMathNary(ExprNode):
    """
    children[0]: op
    children[1]: ExprListNode
    """
    def compile(self, st, output):
        mem_result = st.alloc('int')
        op, expr_list = self.children

        mem_elements = []
        for expr in expr_list.children:
            mem_elements.append(expr.compile(st, output))

        out_type = st.check_type('numeric', *mem_elements, strict=False)
        mem_result = st.alloc(out_type)

        if op == 'sum_of':
            output += [f'VAL_COPY {mem_result.itype()}0 {mem_result}']
            for elem in mem_elements:
                output += [f'ADD {elem} {mem_result} {mem_result}']
        elif op == 'product_of':
            output += [f'VAL_COPY {mem_result.itype()}1 {mem_result}']
            for elem in mem_elements:
                output += [f'MUL {elem} {mem_result} {mem_result}']
        elif op == 'minimum_of':
            output +=  [f'VAL_COPY {mem_elements[0]} {mem_result}']
            if len(mem_elements) > 1:
                mem_test = st.alloc('bool')
                for elem in mem_elements[1:]:
                    label_end, label_else = st.next_if_labels()
                    output += [f'TEST_LESS {elem} {mem_result} {mem_test}']
                    output += [f'JUMP_IF_0 {mem_test} {label_end}']
                    output += [f'VAL_COPY {elem} {mem_result}']
                    output += [f'{label_end}:']
        elif op == 'maximum_of':
            output +=  [f'VAL_COPY {mem_elements[0]} {mem_result}']
            if len(mem_elements) > 1:
                mem_test = st.alloc('bool')
                for elem in mem_elements[1:]:
                    label_end, label_else = st.next_if_labels()
                    output += [f'TEST_GTR {elem} {mem_result} {mem_test}']
                    output += [f'JUMP_IF_0 {mem_test} {label_end}']
                    output += [f'VAL_COPY {elem} {mem_result}']
                    output += [f'{label_end}:']
        else:
            raise NotImplemented(f'Math N-ary op: {op}')
        return mem_result


class ExprMathNaryArray(ExprNode):
    """
    children[0] : op
    children[1] : ident
    """
    def compile(self, st, output):
        op, ident = self.children
        mem_arr = st.lookup(ident)
        st.check_type('numeric[', mem_arr, strict=False)

        mem_ndx = st.alloc('int')
        output += [f'VAL_COPY %0 {mem_ndx}']
        mem_arr_sz = st.alloc('int')
        output += [f'AR_GET_SZ {mem_arr} {mem_arr_sz}']
        mem_test = st.alloc('bool') 
        return_dtype = mem_arr.arr_dtype()
        mem_result = st.alloc(return_dtype)
        mem_curr_elem = st.alloc(return_dtype) 

        if op in ['minimum_of', 'maximum_of']:
            output += [f'AR_GET_NDX {mem_arr} %0 {mem_result}']
        elif op == 'product_of':
            output += [f'VAL_COPY {mem_arr.arr_elem_itype()}1 {mem_result}']
        elif op == 'sum_of':
            output += [f'VAL_COPY {mem_arr.arr_elem_itype()}0 {mem_result}']
        else:
            raise NotImplemented(f'Math Nary-op: {op}')

        label_start, label_end = st.next_while_labels()
        output += [f'{label_start}:']
        output += [f'TEST_LESS {mem_ndx} {mem_arr_sz} {mem_test}']
        output += [f'JUMP_IF_0 {mem_test} {label_end}']
        output += [f'AR_GET_NDX {mem_arr} {mem_ndx} {mem_curr_elem}']
        
        if op == 'minimum_of':
            cond_end, cond_else = st.next_if_labels()
            mem_min_test = st.alloc('bool')
            output += [f'TEST_LESS {mem_curr_elem} {mem_result} {mem_min_test}']
            output += [f'JUMP_IF_0 {mem_min_test} {cond_end}']
            output += [f'VAL_COPY {mem_curr_elem} {mem_result}']
            output += [f'{cond_end}:']
        elif op == 'maximum_of':
            cond_end, cond_else = st.next_if_labels()
            mem_max_test = st.alloc('bool')
            output += [f'TEST_GTR {mem_curr_elem} {mem_result} {mem_max_test}']
            output += [f'JUMP_IF_0 {mem_max_test} {cond_end}']
            output += [f'VAL_COPY {mem_curr_elem} {mem_result}']
            output += [f'{cond_end}:']
        elif op == 'product_of':
            output += [f'MUL {mem_curr_elem} {mem_result} {mem_result}']
        elif op == 'sum_of':
            output += [f'ADD {mem_curr_elem} {mem_result} {mem_result}']
        
        output += [f'ADD {mem_ndx} %1 {mem_ndx}']
        output += [f'JUMP {label_start}']
        output += [f'{label_end}:']

        return mem_result





class ExprLogicNegate(ExprNode):
    """
    children[0]: expr to interpret
    """
    def compile(self, st, output):
        mem_expr = self.children[0].compile(st, output)
        out_type = st.check_type('bool', mem_expr)
        mem_result = st.alloc(out_type)
        output += [f'NOT {mem_expr} {mem_result}']
        return mem_result



class ExprLogicBinary(ExprNode):
    def compile(self, st, output):
        op = self.children[1]
        mem_lhs = self.children[0].compile(st, output)
        mem_rhs = self.children[2].compile(st, output)
        out_type = st.check_type('bool', mem_lhs, mem_rhs)
        mem_result = st.alloc(out_type)
        if op == 'and':
            output += [f'MUL {mem_lhs} {mem_rhs} {mem_result}']
        elif op == 'or':
            output += [f'ADD {mem_lhs} {mem_rhs} {mem_result}']
        elif op == 'xor':
            mem_anded = st.alloc('bool')
            mem_ored = st.alloc('bool')
            mem_nanded = st.alloc('bool')
            output += [f'MUL {mem_lhs} {mem_rhs} {mem_anded}']  # Not XOR if true
            output += [f'ADD {mem_lhs} {mem_rhs} {mem_ored}']   # Not XOR if false
            output += [f'NOT {mem_anded} {mem_nanded}']
            output += [f'MUL {mem_nanded} {mem_ored} {mem_result}']
        else:
            raise NotImplementedError('LogicBinaryOp ', op, 'not defined.')
        return mem_result



class ExprLogicNary(ExprNode):
    """
    children[0]: op
    children[1]: ExprListNode
    """
    def compile(self, st, output):
        op, expr_list = self.children

        mem_elements = []
        for expr in expr_list.children:
            mem_elements.append(expr.compile(st, output))

        out_type = st.check_type('bool', *mem_elements, strict=False)
        mem_result = st.alloc(out_type)
        
        if op == 'any_of':
            output += [f'VAL_COPY %0 {mem_result}']
            for elem in mem_elements:
                output += [f'ADD {elem} {mem_result} {mem_result}']
        elif op == 'every_of':
            output += [f'VAL_COPY %1 {mem_result}']
            for elem in mem_elements:
                output += [f'MUL {elem} {mem_result} {mem_result}']
        else:
            raise NotImplemented(f'Logic N-ary op: {op}')
        return mem_result


class ExprLogicNaryArray(ExprNode):
    """
    children[0] : op
    children[1] : ident
    """
    def compile(self, st, output):
        op, ident = self.children
        mem_arr = st.lookup(ident)
        st.check_type('bool[', mem_arr)

        mem_ndx = st.alloc('int')
        output += [f'VAL_COPY %0 {mem_ndx}']
        mem_arr_sz = st.alloc('int')
        output += [f'AR_GET_SZ {mem_arr} {mem_arr_sz}']
        mem_test = st.alloc('bool') 
        return_dtype = mem_arr.arr_dtype()
        mem_result = st.alloc(return_dtype)
        mem_curr_elem = st.alloc(return_dtype) 

        if op == 'any_of':
            output += [f'VAL_COPY %0 {mem_result}']
        elif op == 'every_of':
            output += [f'VAL_COPY %1 {mem_result}']
        else:
            raise NotImplemented(f'Math Nary-op: {op}')

        label_start, label_end = st.next_while_labels()
        output += [f'{label_start}:']
        output += [f'TEST_LESS {mem_ndx} {mem_arr_sz} {mem_test}']
        output += [f'JUMP_IF_0 {mem_test} {label_end}']
        output += [f'AR_GET_NDX {mem_arr} {mem_ndx} {mem_curr_elem}']
        
        if op == 'any_of':
            output += [f'ADD {mem_result} {mem_curr_elem} {mem_result}']
        elif op == 'every_of':
            output += [f'MUL {mem_result} {mem_curr_elem} {mem_result}']

        output += [f'ADD {mem_ndx} %1 {mem_ndx}']
        output += [f'JUMP {label_start}']
        output += [f'{label_end}:']

        return mem_result





class ExprCompareBinary(ExprNode):
    def compile(self, st, output):
        op = self.children[1]
        mem_lhs = self.children[0].compile(st, output)
        mem_rhs = self.children[2].compile(st, output)
        mem_result = st.alloc('bool')
        st.check_type(mem_lhs, mem_rhs, strict=False)
        if op == '~=':
            output += [f'TEST_NEQU {mem_lhs} {mem_rhs} {mem_result}']
        elif op == '==':
            output += [f'TEST_EQU {mem_lhs} {mem_rhs} {mem_result}']
        elif op == '<':
            output += [f'TEST_LESS {mem_lhs} {mem_rhs} {mem_result}']
        elif op == '>':
            output += [f'TEST_GTR {mem_lhs} {mem_rhs} {mem_result}']
        elif op == '<=':
            mem_equ = st.alloc('int')
            mem_less = st.alloc('int')
            output += [f'TEST_EQU {mem_lhs} {mem_rhs} {mem_equ}']
            output += [f'TEST_LESS {mem_lhs} {mem_rhs} {mem_less}']
            output += [f'ADD {mem_equ} {mem_less} {mem_result}']
        elif op == '>=':
            mem_equ = st.alloc('int')
            mem_gtr = st.alloc('int')
            output += [f'TEST_EQU {mem_lhs} {mem_rhs} {mem_equ}']
            output += [f'TEST_GTR {mem_lhs} {mem_rhs} {mem_gtr}']
            output += [f'ADD {mem_equ} {mem_gtr} {mem_result}']
        else:
            raise NotImplementedError('MathBinOp ', op, 'not defined.')
        return mem_result



class StmtIf(StmtNode):
    '''
    children[0] : expr test condition
    children[1] : stmt list if true
    '''
    def compile(self, st, output):
        mem_test = self.children[0].compile(st, output)
        st.check_type('bool', mem_test)
        label_end, label_else = st.next_if_labels()
        output += [f'JUMP_IF_0 {mem_test} {label_end}']
        st.push_scope_conditional()
        self.children[1].compile(st, output)
        st.pop_scope_conditional()
        output += [f'{label_end}:']



class StmtIfElse(StmtNode):
    '''
    children[0] : expr test condition
    children[1] : stmt list if true
    children[2] : stmt list else
    '''
    def compile(self, st, output):
        mem_test = self.children[0].compile(st, output)
        st.check_type('bool', mem_test)
        label_end, label_else = st.next_if_labels()
        output += [f'JUMP_IF_0 {mem_test} {label_else}']
        st.push_scope_conditional()
        self.children[1].compile(st, output)
        st.pop_scope_conditional()
        output += [f'JUMP {label_end}']
        output += [f'{label_else}:']
        st.push_scope_conditional()
        self.children[2].compile(st, output)
        st.pop_scope()
        output += [f'{label_end}:']



class StmtWhileLoop(StmtNode):
    '''
    children[0] : expr test condition
    children[1] : stmt list block
    '''
    def compile(self, st, output):
        label_start, label_end = st.next_while_labels()

        output += [f'{label_start}:']

        mem_test = self.children[0].compile(st, output)
        st.check_type('bool', mem_test)
        
        output += [f'JUMP_IF_0 {mem_test} {label_end}']
        
        st.push_scope_loop(label_end)
        self.children[1].compile(st, output)
        st.pop_scope_loop()
        
        output += [f'JUMP {label_start}']
        output += [f'{label_end}:']



class StmtBreak(StmtNode):
    '''
    children : None
    '''
    def compile(self, st, output):
        end_label = st.break_to_label()
        output += [f'JUMP {end_label}']





class ExprStringLiteral(ExprNode):
    '''
    children[0] : string literal
    Note: escaped characters still escaped here
    '''

    def compile(self, st, output):
        import re
        # Copy array into memory; return pointer
        str_literal = self.str_unescape(self.children[0][1:-1])
        total_len = len(str_literal)
        mem_ptr = st.alloc('char[')
        output += [f'VAL_COPY @s0 {mem_ptr}']
        output += [f'ADD @s0 %1 @s0']
        output += [f'ADD @s0 %{total_len} @s0']
        output += [f'AR_SET_SZ {mem_ptr} %{total_len}']
        for ndx, char in enumerate(str_literal):
            escaped = self.char_escape(char)
            output += [f'AR_SET_NDX {mem_ptr} %{ndx} $\'{escaped}\'']
        return mem_ptr

    @classmethod
    def str_unescape(cls, s):
        s = s.replace('%n', '\n')
        s = s.replace('%t', '\t')
        s = s.replace('%%', '%')
        s = s.replace('%"', '"')
        return s

    @classmethod
    def char_escape(cls, s):
        s = s.replace('%', '%%')
        s = s.replace('\n', '%n')
        s = s.replace('\t', '%t')
        s = s.replace("'", "%'")
        return s
        




class StmtDeclareArrayNoSizeNoAssign(StmtNode):
    '''
    children[0] : arr dtype
    children[1] : identifier
    '''
    def compile(self, st, output):
        dtype, ident = self.children
        st.declare(dtype, ident) 


class StmtDeclareArraySizedNoAssign(StmtNode):
    '''
    children[0] : arr dtype
    children[1] : identifier
    children[2] : expr [int] size
    '''
    def compile(self, st, output):
        dtype, ident, size = self.children
        arr_ptr = st.declare(ident, dtype)
        mem_expr = size.compile(st, output)
        st.check_type('int', mem_expr)
        output += [f'VAL_COPY @s0 {arr_ptr}']
        output += [f'ADD @s0 %1 @s0']
        output += [f'ADD @s0 {mem_expr} @s0']
        output += [f'AR_SET_SZ {arr_ptr} {mem_expr}']


class StmtDeclareArrayNoSizeAssign(StmtNode):
    '''
    children[0]: array dtype
    children[1]: assign node
    '''
    def compile(self, st, output):
        dtype, assign = self.children
        ident = assign.children[0]
        st.declare(ident, dtype)
        assign.compile(st, output)


class StmtDeclareArraySizedAssign(StmtNode):
    '''
    children[0] : arr dtype
    children[1] : expr size
    children[2] : assign node
    '''
    def compile(self, st, output):
        dtype, expr_size, assign = self.children
        ident = assign.children[0]
        mem_size = expr_size.compile(st, output)
        st.check_type('int', mem_size)
        mem_arr = st.declare(ident, dtype)
        assign.compile(st, output)
        output += [f'AR_SET_SZ {mem_arr} {mem_size}']


class ExprArraySize(ExprNode):
    '''
    children[0] : identifier
    '''
    def compile(self, st, output):
        ident = self.children[0]
        mem_ptr = st.lookup(ident)
        st.check_is_array(mem_ptr)
        mem_result = st.alloc('int')
        output += [f'AR_GET_SZ {mem_ptr} {mem_result}']
        return mem_result


class ExprArrayCopy(ExprNode):
    '''
    children[0] : identifier
    '''
    def compile(self, st, output):
        ident = self.children[0]
        mem_src = st.lookup(ident)
        st.check_is_array(mem_src)
        mem_src_sz = st.alloc('int')
        mem_copy = st.alloc(mem_src.dtype)
        output += [f'AR_GET_SZ {mem_src} {mem_src_sz}']
        output += [f'VAL_COPY @s0 {mem_copy}']
        output += [f'ADD @s0 %1 @s0']
        output += [f'ADD @s0 {mem_src_sz} @s0']
        output += [f'AR_COPY {mem_src} {mem_copy}']
        return mem_copy



class ExprAssignArrayNdx(ExprNode):
    '''
    children[0] : identifier
    children[1] : ndx expr
    children[2] : to_assign expr
    '''
    def compile(self, st, output):
        ident, expr_ndx, expr_toassign = self.children
        mem_ndx = expr_ndx.compile(st, output)
        st.check_type('int', mem_ndx)
        mem_arr = st.lookup(ident)
        st.check_is_array(mem_arr)
        mem_expr = expr_toassign.compile(st, output)
        st.check_type(mem_arr.arr_dtype(), mem_expr)
        output += [f'AR_SET_NDX {mem_arr} {mem_ndx} {mem_expr}']
        return mem_expr



class ExprArrayGetNdx(ExprNode):
    '''
    children[0] : array var
    children[1] : int ndx
    '''
    def compile(self, st, output):
        ident, expr_ndx = self.children
        mem_arr = st.lookup(ident)
        mem_expr = expr_ndx.compile(st, output)
        st.check_type('int', mem_expr)
        mem_result = st.alloc(mem_arr.arr_dtype())
        output += [f'AR_GET_NDX {mem_arr} {mem_expr} {mem_result}']
        return mem_result


class ExprArrRange(ExprNode):
    '''
    children[0] : expr start
    children[1] : expr step
    children[2] : expr stop
    '''
    def compile(self, st, output):
        expr_start, expr_step, expr_stop = self.children
        mem_start = expr_start.compile(st, output)
        mem_step = expr_step.compile(st, output)
        mem_stop = expr_stop.compile(st, output)
        st.check_type('int', mem_start, mem_step, mem_stop)

        # We're going to delay setting the array size until
        # we are done setting the elements.  That also means
        # we have to delay updating the next heap address
        mem_count = st.alloc('int')
        mem_curr = st.alloc('int')
        mem_test = st.alloc('bool')
        label_start, label_end = st.next_while_labels()
        mem_result = st.alloc('int[')

        output += [f'VAL_COPY @s0 {mem_result}']
        output += [f'VAL_COPY %0 {mem_count}']
        output += [f'VAL_COPY {mem_start} {mem_curr}']
        output += [f'{label_start}:']
        output += [f'TEST_LESS {mem_curr} {mem_stop} {mem_test}']
        output += [f'JUMP_IF_0 {mem_test} {label_end}']
        output += [f'AR_SET_NDX {mem_result} {mem_count} {mem_curr}']
        output += [f'ADD %1 {mem_count} {mem_count}']
        output += [f'ADD {mem_step} {mem_curr} {mem_curr}']
        output += [f'JUMP {label_start}']
        output += [f'{label_end}:']

        # Handle delay size stuff
        output += [f'AR_SET_SZ {mem_result} {mem_count}']
        output += [f'ADD @s0 %1 @s0']
        output += [f'ADD @s0 {mem_count} @s0']

        return mem_result



class StmtForArrayID(StmtNode):
    '''
    children[0] : local identifier
    children[1] : array identifier
    children[2] : cmd_list
    '''
    def compile(self, st, output):
        ident_elem, ident_arr, cmd_list = self.children
        mem_arr = st.lookup(ident_arr)
        st.check_is_array(mem_arr)

        st.push_scope_loop()
        label_start, label_end = st.next_for_labels()
        
        arr_dtype = mem_arr.arr_dtype()
        mem_curr_elem = st.declare(ident_elem, arr_dtype)
        mem_curr_ndx = st.alloc('int')
        output += [f'VAL_COPY %0 {mem_curr_ndx}']
        mem_arr_sz = st.alloc('int')
        output += [f'AR_GET_SZ {mem_arr} {mem_arr_sz}']

        output += [f'{label_start}:']

        mem_test = st.alloc('bool')
        output += [f'TEST_LESS {mem_curr_ndx} {mem_arr_sz} {mem_test}']
        output += [f'JUMP_IF_0 {mem_test} {label_end}']
        output += [f'AR_GET_NDX {mem_arr} {mem_curr_ndx} {mem_curr_elem}']

        cmd_list.compile(st, output)

        output += [f'ADD {mem_curr_ndx} %1 {mem_curr_ndx}']
        output += [f'JUMP {label_start}']
        output += [f'{label_end}:']



class StmtForRange(StmtNode):
    '''
    children[0] : local identifier
    children[1] : range
    children[2] : cmd_list
    '''
    def __init__(self, children):
        self.children = children

    def compile(self, st, output):
        ident_elem, the_range, cmd_list = self.children
        mem_arr = the_range.compile(st, output)
        st.check_is_array(mem_arr)

        st.push_scope_loop()
        label_start, label_end = st.next_for_labels()
        
        arr_dtype = mem_arr.arr_dtype()
        mem_curr_ndx = st.alloc('int')
        output += [f'VAL_COPY %0 {mem_curr_ndx}']
        mem_arr_sz = st.alloc('int')
        output += [f'AR_GET_SZ {mem_arr} {mem_arr_sz}']

        output += [f'{label_start}:']

        mem_test = st.alloc('bool')
        output += [f'TEST_LESS {mem_curr_ndx} {mem_arr_sz} {mem_test}']
        output += [f'JUMP_IF_0 {mem_test} {label_end}']

        st.push_scope_loop(label_end)
        mem_curr_elem = st.declare(ident_elem, arr_dtype)
        output += [f'AR_GET_NDX {mem_arr} {mem_curr_ndx} {mem_curr_elem}']
        cmd_list.compile(st, output)
        st.pop_scope()

        output += [f'ADD {mem_curr_ndx} %1 {mem_curr_ndx}']
        output += [f'JUMP {label_start}']
        output += [f'{label_end}:']

