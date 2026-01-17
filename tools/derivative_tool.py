import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

def compute_derivative():

    x = sp.symbols(input("Enter the variable: "))
    expr = parse_expr(input("Enter the function to differentiate: "))
    diff_expr = sp.diff(expr, x)
    
    print("The derivative of", expr, "with respect to", x, "is:")
    sp.pprint(diff_expr)

if __name__ == "__main__":
    compute_derivative()