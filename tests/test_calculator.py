import unittest
from calculator import CalculatorError, CalculatorZeroDivisionError, calculate


class CalculatorTests(unittest.TestCase):
    def test_arithmetic(self):
        for expr, expected in [('2+3*4','14'), ('(2+3)*4','20'), ('10/4','2.5'), ('-5+2','-3'), ('1.2+2.3','3.5'), ('2*-3','-6'), ('0.1+0.2','0.3')]:
            with self.subTest(expr=expr):
                self.assertEqual(calculate(expr), expected)

    def test_functions(self):
        for expr, expected in [('√9','3'), ('√(9+7)','4'), ('50%','0.5'), ('200*10%','20'), ('200+10%','200.1'), ('(50+50)%','1'), ('--5','5'), ('√(16)%','0.4')]:
            with self.subTest(expr=expr):
                self.assertEqual(calculate(expr), expected)

    def test_errors(self):
        for expr in ('', '(', '1+', '2(3)', '√-1', 'hello', '1..2', '2**3', '1 2', '(' * 70 + '1' + ')' * 70):
            with self.subTest(expr=expr):
                with self.assertRaises(CalculatorError):
                    calculate(expr)
        with self.assertRaises(CalculatorZeroDivisionError):
            calculate('5/(2-2)')

    def test_limits(self):
        with self.assertRaises(CalculatorError):
            calculate('1+' * 300 + '1')
        self.assertEqual(calculate('0/5'), '0')


if __name__ == '__main__':
    unittest.main()
