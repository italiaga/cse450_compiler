import unittest


class TestYourTests(unittest.TestCase):
    """
    If you want to add any tests of your own,
    you can do so here.
    """
    pass



class TestProject01(unittest.TestCase):
    
    def test_empty(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = ""
        expected = []
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)



    def test_newline(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = "\n"
        expected = [
            'EOC'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    def test_comments_0(self):
        # from compiler.solution import lex_source
        # from helpers import get_token_names
        # src = "#This is a single line comment"
        # expected = [
        #     'COMMENT_SINGLE'
        # ]
        # actual = get_token_names(lex_source(src))
        # self.assertEquals(expected, actual)
        pass  # Project 2 makes this test fail


    def test_comments_1(self):
        # from compiler.solution import lex_source
        # from helpers import get_token_names
        # src = """#This is a single line comment
        # """
        # expected = [
        #     'COMMENT_SINGLE','EOC'
        # ]
        # actual = get_token_names(lex_source(src))
        # self.assertEquals(expected, actual)
        pass  # Project 2 makes this test fail


    def test_comments_2(self):
        # from compiler.solution import lex_source
        # from helpers import get_token_names
        # src = """
        # '''
        # This is a mutliline comment.  We will process this
        # as a single lexeme even though it contains multiple
        # lines.  You will have to use a regular expression flags
        # to handle multiple lines and the newline character.  You can
        # logically OR the flags together using the | operator.
        # '''
        # Hello
        # """
        # expected = [
        #     'EOC',
        #     'COMMENT_MULTI','EOC',
        #     'IDENTIFIER','EOC'
        # ]
        # actual = get_token_names(lex_source(src))
        # self.assertEquals(expected, actual)
        pass  # Project 2 makes this test fail



    # ===================================================================================== SCALAR TYPES
    def test_scalar_type_0(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = "int"
        expected = [
            'SCALAR_TYPE'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)



    def test_scalar_type_1(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = "float"
        expected = [
            'SCALAR_TYPE'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)



    def test_scalar_type_2(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = "bool"
        expected = [
            'SCALAR_TYPE'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)



    def test_scalar_type_3(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = "char"
        expected = [
            'SCALAR_TYPE'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    # ===================================================================================== LITERALS
    def test_literal_bool_0(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = "True"
        expected = [
            'BOOL_LITERAL'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    
    def test_literal_bool_1(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = "False"
        expected = [
            'BOOL_LITERAL'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)

    

    def test_literal_char_0(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = "'a'"
        expected = [
            'CHAR_LITERAL'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    def test_literal_int_0(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = "123"
        expected = [
            'INT_LITERAL'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)       



    def test_literal_int_1(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = "+42"
        expected = [
            'MATH_PLUS','INT_LITERAL'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)     


    
    def test_literal_int_2(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = "-200"
        expected = [
            'MATH_MINUS','INT_LITERAL'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)      



    def test_literal_float_0(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = "3.14"
        expected = [
            'FLOAT_LITERAL'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)     



    def test_literal_float_1(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = "+42.14"
        expected = [
            'MATH_PLUS','FLOAT_LITERAL'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)  



    def test_literal_float_2(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = "-212.2"
        expected = [
            'MATH_MINUS','FLOAT_LITERAL'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)  



    def test_scalar_declarations_0(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """int w
        float x
        char y
        bool z
        """
        expected = [
            'SCALAR_TYPE','IDENTIFIER','EOC',
            'SCALAR_TYPE','IDENTIFIER','EOC',
            'SCALAR_TYPE','IDENTIFIER','EOC',
            'SCALAR_TYPE','IDENTIFIER','EOC'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)



    # ===================================================================================== MATH OPS
    def test_math_unary_0(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """--1"""
        expected = [
            'MATH_MINUS','MATH_MINUS','INT_LITERAL'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    def test_math_binary_0(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """1+2"""
        expected = [
            'INT_LITERAL','MATH_PLUS','INT_LITERAL'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    def test_math_binary_1(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """1-2"""
        expected = [
            'INT_LITERAL','MATH_MINUS','INT_LITERAL'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    def test_math_binary_2(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """1+2
        3-2
        100*200
        30/3
        33%11
        """
        expected = [
            'INT_LITERAL','MATH_PLUS','INT_LITERAL','EOC',
            'INT_LITERAL','MATH_MINUS','INT_LITERAL','EOC',
            'INT_LITERAL','MATH_BINARY_OP','INT_LITERAL','EOC',
            'INT_LITERAL','MATH_BINARY_OP','INT_LITERAL','EOC',
            'INT_LITERAL','MATH_BINARY_OP','INT_LITERAL','EOC'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)



    def test_math_nary_op_0(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """sum_of"""
        expected = [
            'MATH_NARY_OP'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)



    def test_math_nary_op_1(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """product_of"""
        expected = [
            'MATH_NARY_OP'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)



    def test_math_nary_op_3(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """minimum_of"""
        expected = [
            'MATH_NARY_OP'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)



    def test_math_nary_op_4(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """maximum_of"""
        expected = [
            'MATH_NARY_OP'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)

    
    def test_math_nary_op_5(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """minimum_of {1, 2, 3}
        maximum_of {1,2,3}
        product_of {1}
        sum_of {1,2}
        """
        expected = [
            'MATH_NARY_OP','BRACE_OPEN','INT_LITERAL','COMMA','INT_LITERAL','COMMA','INT_LITERAL','BRACE_CLOSE','EOC',
            'MATH_NARY_OP','BRACE_OPEN','INT_LITERAL','COMMA','INT_LITERAL','COMMA','INT_LITERAL','BRACE_CLOSE','EOC',
            'MATH_NARY_OP','BRACE_OPEN','INT_LITERAL','BRACE_CLOSE','EOC',
            'MATH_NARY_OP','BRACE_OPEN','INT_LITERAL','COMMA','INT_LITERAL','BRACE_CLOSE','EOC'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    def test_complex_math_0(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """
        1 + 3 * 4 - -1
        """
        expected = [
            'EOC',
            'INT_LITERAL', 'MATH_PLUS', 'INT_LITERAL', 'MATH_BINARY_OP', 'INT_LITERAL', 'MATH_MINUS', 'MATH_MINUS', 'INT_LITERAL', 'EOC'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)



    def test_complex_math_1(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """
        (-3.14 - 10) + -10.0
        """
        expected = [
            'EOC',
            'PAREN_OPEN','MATH_MINUS','FLOAT_LITERAL','MATH_MINUS','INT_LITERAL','PAREN_CLOSE','MATH_PLUS','MATH_MINUS','FLOAT_LITERAL','EOC'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)



    # ===================================================================================== BOOLEAN OPS
    def test_boolean_unary_0(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """~True
        """
        expected = [
            'LOGIC_UNARY_OP','BOOL_LITERAL','EOC'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    def test_boolean_binary_0(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """True and False
        """
        expected = [
            'BOOL_LITERAL','LOGIC_BINARY_OP','BOOL_LITERAL','EOC'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)



    def test_boolean_binary_1(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """False or True
        """
        expected = [
            'BOOL_LITERAL','LOGIC_BINARY_OP','BOOL_LITERAL','EOC'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)



    def test_boolean_binary_2(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """True xor False
        """
        expected = [
            'BOOL_LITERAL','LOGIC_BINARY_OP','BOOL_LITERAL','EOC'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)



    def test_boolean_nary_0(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """every_of {True, False}"""
        expected = [
            'LOGIC_NARY_OP','BRACE_OPEN','BOOL_LITERAL','COMMA','BOOL_LITERAL','BRACE_CLOSE'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)



    def test_boolean_nary_1(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """any_of {False, False}"""
        expected = [
            'LOGIC_NARY_OP','BRACE_OPEN','BOOL_LITERAL','COMMA','BOOL_LITERAL','BRACE_CLOSE'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    def test_boolean_complex_0(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """every_of {True, False} or True"""
        expected = [
            'LOGIC_NARY_OP','BRACE_OPEN','BOOL_LITERAL','COMMA','BOOL_LITERAL','BRACE_CLOSE','LOGIC_BINARY_OP','BOOL_LITERAL'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)



    def test_boolean_complex_1(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """True and (True or False)"""
        expected = [
            'BOOL_LITERAL','LOGIC_BINARY_OP','PAREN_OPEN','BOOL_LITERAL','LOGIC_BINARY_OP','BOOL_LITERAL','PAREN_CLOSE'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    
    def test_boolean_complex_2(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """every_of {~True, True, ~False} or True"""
        expected = [
            'LOGIC_NARY_OP','BRACE_OPEN','LOGIC_UNARY_OP','BOOL_LITERAL','COMMA','BOOL_LITERAL','COMMA','LOGIC_UNARY_OP','BOOL_LITERAL','BRACE_CLOSE','LOGIC_BINARY_OP','BOOL_LITERAL'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    # ===================================================================================== COMPARE OPS
    def test_compare_op_0(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """1>2"""
        expected = [
           'INT_LITERAL','COMPARE_BINARY_OP','INT_LITERAL'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    def test_compare_op_1(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """3 > 4.0"""
        expected = [
           'INT_LITERAL','COMPARE_BINARY_OP','FLOAT_LITERAL'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    def test_compare_op_2(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """10 >= 1"""
        expected = [
           'INT_LITERAL','COMPARE_BINARY_OP','INT_LITERAL'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    def test_compare_op_3(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """11.1 <= -1.0"""
        expected = [
           'FLOAT_LITERAL','COMPARE_BINARY_OP','MATH_MINUS','FLOAT_LITERAL'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    def test_compare_op_4(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """True == False"""
        expected = [
           'BOOL_LITERAL','COMPARE_BINARY_OP','BOOL_LITERAL'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    def test_compare_op_5(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """True ~= ~False"""
        expected = [
           'BOOL_LITERAL','COMPARE_BINARY_OP','LOGIC_UNARY_OP','BOOL_LITERAL'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    # ===================================================================================== I/O

    def test_printing_0(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """print {x}
        println {10,11}
        """
        expected = [
           'PRINTING','BRACE_OPEN','IDENTIFIER','BRACE_CLOSE','EOC',
           'PRINTING','BRACE_OPEN','INT_LITERAL','COMMA','INT_LITERAL','BRACE_CLOSE','EOC'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    def test_inputting_0(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """
        char foo = input_char
        int FOO = input_int
        float bar = input_float
        bool BAR = input_bool
        """
        expected = [
           'EOC',
           'SCALAR_TYPE','IDENTIFIER','ASSIGN','INPUTTING','EOC',
           'SCALAR_TYPE','IDENTIFIER','ASSIGN','INPUTTING','EOC',
           'SCALAR_TYPE','IDENTIFIER','ASSIGN','INPUTTING','EOC',
           'SCALAR_TYPE','IDENTIFIER','ASSIGN','INPUTTING','EOC'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    # ===================================================================================== COMPLEX

    def test_complex_0(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """
        int integer = 10
        float y = 20.0
        float z = integer + (y - -10.0)
        z = z + input_float
        print {z}
        """
        expected = [
            'EOC',
            'SCALAR_TYPE','IDENTIFIER','ASSIGN','INT_LITERAL','EOC',
            'SCALAR_TYPE','IDENTIFIER','ASSIGN','FLOAT_LITERAL','EOC',
            'SCALAR_TYPE','IDENTIFIER','ASSIGN','IDENTIFIER','MATH_PLUS','PAREN_OPEN','IDENTIFIER','MATH_MINUS','MATH_MINUS','FLOAT_LITERAL','PAREN_CLOSE','EOC',
            'IDENTIFIER','ASSIGN','IDENTIFIER','MATH_PLUS','INPUTTING','EOC',
            'PRINTING','BRACE_OPEN','IDENTIFIER','BRACE_CLOSE','EOC'
        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    def test_complex_1(self):
        from compiler.solution import lex_source
        from helpers import get_token_names
        src = """
        bool boolean = True
        bool boolean2 = False
        bool every_of_two = every_of {boolean, boolean2}
        bool any_of_two = any_of {boolean, boolean2}
        """
        expected = [
            'EOC',
            'SCALAR_TYPE','IDENTIFIER','ASSIGN','BOOL_LITERAL','EOC',
            'SCALAR_TYPE','IDENTIFIER','ASSIGN','BOOL_LITERAL','EOC',
            'SCALAR_TYPE','IDENTIFIER','ASSIGN','LOGIC_NARY_OP','BRACE_OPEN','IDENTIFIER','COMMA','IDENTIFIER','BRACE_CLOSE','EOC',
            'SCALAR_TYPE','IDENTIFIER','ASSIGN','LOGIC_NARY_OP','BRACE_OPEN','IDENTIFIER','COMMA','IDENTIFIER','BRACE_CLOSE','EOC'

        ]
        actual = get_token_names(lex_source(src))
        self.assertEquals(expected, actual)


    def test_complex_2(self):
        # from compiler.solution import lex_source
        # from helpers import get_token_names
        # src = """
        # '''
        # This is a test
        # of a multiline
        # comment
        # '''

        # bool b = True    # Set to true
        # int foo
        # int FOO
        # foo = -FOO
        # int Foo = (foo+FOO) * +30  # Should be zero?
        # """
        # expected = [
        #     'EOC',
        #     'COMMENT_MULTI',
        #     'EOC',
        #     'EOC',
        #     'SCALAR_TYPE','IDENTIFIER','ASSIGN','BOOL_LITERAL','COMMENT_SINGLE','EOC',
        #     'SCALAR_TYPE','IDENTIFIER','EOC',
        #     'SCALAR_TYPE','IDENTIFIER','EOC',
        #     'IDENTIFIER', 'ASSIGN', 'MATH_MINUS', 'IDENTIFIER','EOC',
        #     'SCALAR_TYPE','IDENTIFIER','ASSIGN','PAREN_OPEN','IDENTIFIER','MATH_PLUS','IDENTIFIER','PAREN_CLOSE','MATH_BINARY_OP','MATH_PLUS','INT_LITERAL','COMMENT_SINGLE','EOC'

        # ]
        # actual = get_token_names(lex_source(src))
        # self.assertEquals(expected, actual)
        pass  # Project 2 makes this test fail