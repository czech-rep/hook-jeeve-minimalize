import safe_parser
import json
import sys
import os
from path_finder import GetScriptDirectory
# from math import *

class ProcessingError(Exception): 
    pass
    # def __init__(self, msg):
    #     super.__init__(self)
    #     self.msg = msg

def process_input(post_dict): 
    '''
    process case data from request
    raises ProcessingError
    '''

    vars_ = post_dict["vars"]

    try:
        start_point = post_dict["x0"]  # start point is a string: 1.1,4.5,6, ..
        start_point = tuple( float(x) for x in start_point.split(',') )
    except Exception as e:
        # return {'success': False, 'msg': f'nieprawidłowy punkt startowy \n{e}'}
        raise ProcessingError(f'nieprawidłowy punkt startowy \n{e}')

    expression_string = post_dict["expr"]
    if expression_string == '':
        raise ProcessingError('nie podano wzoru funkcji')
    try:
        # print(expression_string, vars_, start_point)
        parsed_fun = safe_parser.parse_uni(expression_string, vars_) # here we get lambda: f(x, y, ..)
        test_eval = float(parsed_fun(*start_point))            # try to count in start point 
        print(test_eval)
    except NameError:
        raise ProcessingError('wykryto niedozwolone wyrażenie we wzorze funkcji')
    except Exception as e:
        raise ProcessingError('nieprawidłowa funkcja; \\n {e}')

    try:
        stop_condition = post_dict["stop"]       # 'iter', 'step'
    except KeyError:
        raise ProcessingError('wybierz warunek stopu')

    stop_value = post_dict['stopval']
    if stop_value == '':
        raise ProcessingError('uzupełnij wartość graniczną')
    try:
        if stop_condition == 'iter':
            stop_value = int(stop_value)
        else:
            stop_value = float(stop_value)
    except ValueError:
        raise ProcessingError('nieprawidłowa wartość graniczna')

    return { 'success': True
            , 'expression_string': expression_string
            , 'expression': parsed_fun
            , 'vars': vars_
            ,'start_point': start_point
            , 'stop_condition': stop_condition
            , 'stop_value': stop_value
            , 'stop_condition_name': {'iter':'liczba iteracji', 'step':'dokładność'}[stop_condition]
        }

def load_input(id_): # raises KeyError
    key = str(id_)

    script_path = GetScriptDirectory()
    parent_path = os.path.dirname(script_path)
    path = os.path.join(script_path, 'data', 'examples.json')

    with open(path, 'r') as ex_json:
        examples = json.load(ex_json)
    
    return examples[key]

def example_expresions(): # get example expressions from example cases
    script_path = GetScriptDirectory()
    parent_path = os.path.dirname(script_path)
    path = os.path.join(script_path, 'data', 'examples.json')

    with open(path, 'r') as ex_json:
        examples = json.load(ex_json)

    return [ {'no': id_, 'expr': examples[id_]['expr']} for id_ in examples.keys() ]


if __name__ == '__main__':
    None
    # load_input(1)
    print(example_expresions())
