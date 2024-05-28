import unittest

class TestParsing(unittest.TestCase):

    def test_empty(self):
        from helpers import test_rules
        src=''
        test_rules(src)

    
    def test_comments(self):
        from helpers import test_rules
        src="""
        '''This is a test'''
        # To see if comments are removed
        """
        test_rules(src)


    def test_error(self):
        from helpers import test_rules
        src="""This should throw an exception!
        """
        with self.assertRaises(Exception):
            test_rules(src)

    
    def test_expr_scalar_int(self):
        from helpers import test_rules
        src = '3\n'
        test_rules(src)


    def test_expr_scalar_bool_0(self):
        from helpers import test_rules
        src = 'True\n'
        test_rules(src)


    def test_expr_scalar_bool_1(self):
        from helpers import test_rules
        src = 'False\n'
        test_rules(src)


    def test_stmt_declare_0(self):
        from helpers import test_rules
        src = 'int x\n'
        test_rules(src)

    
    def test_stmt_declare_1(self):
        from helpers import test_rules
        src = 'bool y\n'
        test_rules(src)


    def test_stmt_decalre_w_init_int(self):
        from helpers import test_rules
        src = 'int x = 42\n'
        test_rules(src)


    def test_stmt_decalre_w_init_bool(self):
        from helpers import test_rules
        src = 'bool x = True\n'
        test_rules(src)


    def test_stmt_declare_w_init_chained(self):
        from helpers import test_rules
        src = 'int x = y = 100\n'
        test_rules(src)


    def test_expr_math_negate(self):
        from helpers import test_rules
        src = '-44\n'
        test_rules(src)


    def test_math_bin_ops_0(self):
        from helpers import test_rules
        src = '1+2\n'
        test_rules(src)


    def test_math_bin_ops_1(self):
        from helpers import test_rules
        src = '3-4\n'
        test_rules(src)


    def test_math_bin_ops_2(self):
        from helpers import test_rules
        src = '4/2\n'
        test_rules(src)


    def test_math_bin_ops_3(self):
        from helpers import test_rules
        src = '2*7\n'
        test_rules(src)


    def test_math_bin_ops_4(self):
        from helpers import test_rules
        src = '1+2*3\n'
        test_rules(src)


    def test_math_bin_ops_5(self):
        from helpers import test_rules
        src = 'x+1\n'
        test_rules(src)


    def test_math_bin_ops_6(self):
        from helpers import test_rules
        src = 'y+foo\n'
        test_rules(src)



    def test_math_paren_0(self):
        from helpers import test_rules
        src = '(47)\n'
        test_rules(src)


    def test_math_paren_1(self):
        from helpers import test_rules
        src = '(47+92-8)+1\n'
        test_rules(src)

    def test_math_paren_2(self):
        from helpers import test_rules
        src = '(True)\n'
        test_rules(src)


    def test_math_logic_negate(self):
        from helpers import test_rules
        src = '~False\n'
        test_rules(src)

    
    def test_logic_binary_ops_0(self):
        from helpers import test_rules
        src = 'True and False\n'
        test_rules(src)


    def test_logic_binary_ops_1(self):
        from helpers import test_rules
        src = 'False or False\n'
        test_rules(src)


    def test_logic_binary_ops_2(self):
        from helpers import test_rules
        src = 'True xor True\n'
        test_rules(src)


    def test_compare_ops_equal(self):
        from helpers import test_rules
        src = '1 == 2\n'
        test_rules(src)


    def test_compare_ops_notequal(self):
        from helpers import test_rules
        src = '100 ~= 200\n'
        test_rules(src)


    def test_compare_ops_less(self):
        from helpers import test_rules
        src = '99 < 200\n'
        test_rules(src)


    def test_compare_ops_greater(self):
        from helpers import test_rules
        src = '444 > 333\n'
        test_rules(src)


    def test_compare_ops_geq(self):
        from helpers import test_rules
        src = '444 >= 333\n'
        test_rules(src)


    def test_compare_ops_leq(self):
        from helpers import test_rules
        src = '444 <= 333\n'
        test_rules(src)


    def test_input_bool(self):
        from helpers import test_rules
        src = 'input_bool\n'
        test_rules(src)


    def test_input_int(self):
        from helpers import test_rules
        src = 'input_int\n'
        test_rules(src)


    def test_printing_single_0(self):
        from helpers import test_rules
        src = 'print {3}\n'
        test_rules(src)


    def test_printing_single_1(self):
        from helpers import test_rules
        src = 'print {True}\n'
        test_rules(src)


    def test_printing_single_2(self):
        from helpers import test_rules
        src = 'print {1<3}\n'
        test_rules(src)

    
    def test_printing_multiple_0(self):
        from helpers import test_rules
        src = 'print {1,2}\n'
        test_rules(src)


    def test_printing_multiple_1(self):
        from helpers import test_rules
        src = 'print {1,2,3,4,5}\n'
        test_rules(src)


    def test_println_single_0(self):
        from helpers import test_rules
        src = 'println {3}\n'
        test_rules(src)


    def test_println_single_1(self):
        from helpers import test_rules
        src = 'println {True}\n'
        test_rules(src)


    def test_println_single_2(self):
        from helpers import test_rules
        src = 'println {1<3}\n'
        test_rules(src)

    
    def test_println_multiple_0(self):
        from helpers import test_rules
        src = 'println {1,2}\n'
        test_rules(src)


    def test_println_multiple_1(self):
        from helpers import test_rules
        src = 'println {1,2,3,4,5}\n'
        test_rules(src)


    def test_math_nary_0(self):
        from helpers import test_rules
        src = 'sum_of {1}\n'
        test_rules(src)


    def test_math_nary_1(self):
        from helpers import test_rules
        src = 'product_of {1,2,3,4}\n'
        test_rules(src)
        

    def test_math_nary_2(self):
        from helpers import test_rules
        src = 'minimum_of {42,343,1231}\n'
        test_rules(src)


    def test_math_nary_3(self):
        from helpers import test_rules
        src = 'maximum_of {-42,-343,foo}\n'
        test_rules(src)


    def test_math_nary_empty(self):
        from helpers import test_rules
        src = 'maximum_of {}\n'
        with self.assertRaises(Exception):
            test_rules(src)


    def test_logic_nary_0(self):
        from helpers import test_rules
        src = 'any_of {True}\n'
        test_rules(src)


    def test_logic_nary_1(self):
        from helpers import test_rules
        src = 'every_of {True, True, True}\n'
        test_rules(src)


    def test_complex_0(self):
        from helpers import test_rules
        src = """
        # this is a comment
        int foo = 10
        int bar = foo + foo
        println {foo, bar}
        """
        test_rules(src)
    

    def test_complex_1(self):
        from helpers import test_rules
        src = """
        bool baz = every_of {True, True, False} or True
        """
        test_rules(src)

    
    def test_complex_2(self):
        from helpers import test_rules
        src = """
        int foo = 10
        bool bar
        bool baz = bar = True
        print {foo, bar, baz}
        """
        test_rules(src)


    def test_complex_3(self):
        from helpers import test_rules
        src = """
        bool is_less = 10 < 30
        int x = 20
        is_less = x < 30
        """
        test_rules(src)


    def test_complex_4(self):
        from helpers import test_rules
        src = """
        int x = sum_of {4,5,-6,3+4, product_of{1,2,3}}
        """
        test_rules(src)


    def test_complex_5(self):
        from helpers import test_rules
        src = """
        bool result = True and False or every_of {True, True, True} xor False
        bool other = False
        println {reuslt == other}
        """
        test_rules(src)


    def test_complex_6(self):
        from helpers import test_rules
        src = """
        bool result_A = 10 < 20
        bool result_B = 20 > 30
        bool result_C = 100 ~= 100
        println {any_of{result_A,result_B,result_C}}
        """
        test_rules(src)


    def test_complex_7(self):
        from helpers import test_rules
        src = """
        '''This is a multiline
        comment'''
        int foo = ---6+1
        int bar = product_of {foo, 10}
        int baz = input_int
        println {bar+baz}
        """
        test_rules(src)


    def test_complex_8(self):
        from helpers import test_rules
        src = """
        print {3+4, 10<200, --200, True, any_of{True}}
        """
        test_rules(src)