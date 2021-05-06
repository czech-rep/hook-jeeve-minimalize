from flask import render_template, request, redirect

from main import app

from safe_parser import parse_uni
from hook_lib.hook_service import get_results

import views_helpers


@app.route('/', methods=['GET', 'POST'])
def optimize2d():

    if request.method == 'POST':
        # ImmutableMultiDict([('vars', 'x,y'), ('expr', '(x-3)**2 + y**2'), ('x0', '2, 2'), ('stop', 'iter'), ('stopval', '30')])
        # print(request.form)
        
        try:
            case = views_helpers.process_input(request.form)
        except views_helpers.ProcessingError as e:
            return render_template('error.html', msg=e)
        # if not case['success']:
        #     return render_template('error.html', msg=case['msg'])
        
        # evaluate case
        results, plots = get_results(case['expression'], case['start_point'], case['stop_condition'], case['stop_value'])
                    # do poprawienia - lista wartości słownika

        return render_template('hook_results.html', args={'case': case, 'results': results, 'plots': plots})

    examples = views_helpers.example_expresions() # return a list of dicts
    return render_template('hook_case.html', examples=examples)


@app.route('/example/<_id>', methods=['GET'])
def example(_id):

    try:
        input_data = views_helpers.load_input(_id)
    except KeyError:
        return render_template('error.html', msg='invalid example number')

    # print(input_data)
    try:
        case = views_helpers.process_input(input_data)
    except views_helpers.ProcessingError as e:
        return render_template('error.html', msg=e)
        
    if not case['success']:
        return render_template('error.html', msg=case['msg'])
    
    # evaluate case
    results, plots = get_results(case['expression'], case['start_point'], case['stop_condition'], case['stop_value'])

    return render_template('hook_results.html', args={'case': case, 'results': results, 'plots': plots})

