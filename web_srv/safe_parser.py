from math import *

safe_list = ['acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 
                 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 
                 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 
                 'modf', 'pi', 'pow', 'radians'
				 , 'sin'
				 , 'sinh', 'sqrt', 
                 'tan', 'tanh'] 

safe_dict = {}
for k in safe_list:
    safe_dict[k] = locals().get(k)

def parse(expr):            # raises NameError
    fun = eval( 'lambda x: ' + expr , safe_dict ) 
    return fun

def parse2d(expr):
    fun = eval( 'lambda x,y: ' + expr, safe_dict)
    return fun

def parse_uni(expr, vars_):
    fun = eval( f'lambda {vars_}: {expr}', safe_dict)
    return fun

def test_pn(input):
    x=5
    _dict = safe_dict
    _dict['x'] = x
    expr = eval(f'input', _dict)
    return expr

if __name__ == '__main__':
    # f = parse('sin(x) + p')
    # f = parse('sin(x)')
    # print(f)
    # print(type(f))
    # print(f(0))
    # print(f(3.1415))
    fu = parse2d('x+sin(y)')
    # print(f(5, 5))
    # fu = parse_uni('(x-3)**2 + y**2', 'x,y')
    print(fu(1, 1))

    # print(test_pn('x**2'))
# ImmutableMultiDict([('vars', 'x,y'), ('expr', ), ('x0', '2, 2'), ('stop', 'iter'), ('stopval', '30')])
'''
problem is, that NameError is raised in line 29 as the function is called
it should be in line 25 when evaluating lambda and finding not allowed expression
'''