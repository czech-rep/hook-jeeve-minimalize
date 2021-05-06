import random

try:
    from plotting import plot_path, plot_progress, plot_surf
    from hook_method import optimize
except ImportError:
    from .plotting import plot_path, plot_progress, plot_surf
    from .hook_method import optimize


def get_results(expr, x0, condition, limit):
    result = optimize(expr, x0, condition, limit)
    if not result['success']:
        return result, {}

    # else - we succeded
    if len(x0) == 2:        # dimentions of our problem - we can plot for 3d
        plots = [plot_surf(expr, x0, result['x_result'])
                , plot_path(result['x'])
                , plot_progress(result['x_result'], result['x'], result['step_iterations'])
            ]

    else:
        plots = [plot_progress(result['x_result'], result['x'], result['step_iterations'])]

    return result, plots # return to webapp results and list of plots

def show_results(expr, x0, condition, limit): # for testing
    result = optimize(expr, x0, condition, limit)
    if not result['success']:
        return result, {}

    # else - we succeded
    if len(x0) == 2:        # dimentions of our problem - we can plot for 3d
        plot_surf(expr, x0, result['x_result'], show=True)
        plot_path(result['x'], show=True)
        plot_progress(result['x_result'], result['x'], result['step_iterations'], show=True)

    else:
        plot_progress(result['x_result'], result['x'], result['step_iterations'], show=True)

    return result # return to webapp results and list of plots


if __name__ == '__main__':
    None