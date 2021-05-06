def _wander_around(x:tuple, j, step): 
    """
    guides x around 4 directions depending on j. returns x updated by e in one dimention
    new x_j is calculated on previuos x_(j-1)
    """
    step_length = (-1)**(j) * step     # 1, -1, 1, -1
    vector = list(x)
    vector[ j//2 ] += step_length    # 0, 0, 1, 1, 2, 2
    return tuple(vector)

def _step_down(expr, step, x: tuple, val): # try to step into lower region
    x_old = x
    j = 0
    eval_counter = 0
    while j < len(x_old) * 2: # for 4 dimentions, iter from 0 to 7
        x_step = _wander_around(x, j, step)
        val_step = expr(*x_step)
        eval_counter += 1
        if val_step < val:
            val = val_step      # save minimum value
            x = x_step      # if success - wander from new x

            if j%2 == 0:    # when success in try in each dimention, we skip to another dimention
                j += 2  
                continue
        
        j += 1
    return (x != x_old) , val, x, eval_counter # first argument: if x differs - means we made progess


def optimize(expr, x0:tuple, condition='step', limit=1e-3):

    stop_function = {'iter': _iter_trigger, 'step': _step_trigger}.get(condition)
    if stop_function is None:
        raise ValueError('incorrect stopping condition')

    step_initial = 1.
    step = step_initial
    beta = .51           # step shrink rato
    x = [x0]            # start point
    F = [expr( *x0 )]     # value at start
    step_iterations = [0]   # iterations where successfull steps were taken
    success = False
    message = ''

    counter, wander_counter = 1, 0
    eval_counter = 0
    while True:
        result = _step_down(expr, step, x[-1], F[-1])
        eval_counter += result[3]

        if result[0]:               # means step was successful
            F.append( result[1] )   # save results
            x.append( result[2] )
            step_iterations.append(counter)
        else:
            step *= beta

        if stop_function(counter, step, limit):
            if step == step_initial or F[0] == F[-1]:
                success, message = False, 'optimizer reached limit not finding minimum. Change starting conditions'
                break 
            else:
                success, message = True, 'desired condition met'
                break

        if counter > 5e5:
            success, message = False, 'iteration limit reached (5e5) with no success'
            break
        
        counter += 1                    # count all loop iterations
        

    return { 'success': success
        , 'message': message
        , 'counter': counter
        , 'precision': step
        , 'x_result': x[-1]
        , 'F_result': F[-1]
        , 'x': x
        , 'F': F
        , 'step_iterations': step_iterations
        , 'eval_counter': eval_counter
    }        


# stopping functions
_iter_trigger = lambda iter_, step, limit: True if iter_ >= limit else False
_step_trigger = lambda iter_, step, limit: True if step <= limit else False

def _test_wander():
    for i in range(8):
        print(_wander_around((1, 1, 1, 1), i, 1))

def print_res(res):
    # print(res['step_history'])
    print(res['success'], res['message'], res['F_result'])
    print(res['counter'], res['precision'])
    print('result: ', res['x_result'])

def _test_paraboloid_2d():
    expr = lambda x, y: (x+1)**2 + (y-2)**2
    res = optimize(expr, (3, 3), 'step', 5e-2)
    print_res(res)

def _test_paraboloid_3d():
    expr = lambda x, y, z: (x+1)**2 + (y-2)**2 + (z+.33)**2
    res = optimize(expr, (3, 3, 2), 'step', 5e-6)
    print_res(res)

def _test_paraboloid_4d():
    expr = lambda x, y, z, q: (x+1)**2 + (y-2)**2 + (z+.33)**2 + (q+9)**2
    res = optimize(expr, (3, 3, 2, 0), 'step', 5e-6)
    print_res(res)
    
def _test_plateau():
    expr = lambda x, y, z, q: 4
    res = optimize(expr, (3, 3, 2, 0), 'step', 5e-6)
    print_res(res)

def _test_f_up():
    # expr = lambda x, y: x**4 + y**4 - 4*x*y
    expr = lambda x, y: 100 * ( y - x**2)**2 + (1-x)**2
    res = optimize(expr, (3, 3), 'step', 5e-6)
    print_res(res)

if __name__ == "__main__":
    # _test_wander()
    # _test_paraboloid_2d()
    # _test_paraboloid_3d()
    _test_paraboloid_4d()
    # _test_f_up()
    # _test_plateau()
    
