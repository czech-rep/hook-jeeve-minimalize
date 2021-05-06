import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import plotly.offline as plt_off
from math import *

try:
    from hook_method import optimize
except ImportError:
    from .hook_method import optimize
    

def euclidean(x_result:tuple, x_path:list): # takes x_result - tuple, and x_path - list of tuples. works for any dimention
    result = []
    for x_p in x_path:
        s = [ (x1 - x2)**2 for x1, x2 in zip(x_result, x_p) ] # arr of square distances
        result.append( sum(s)**.5 )
    return result
    
def get_plot_frame(start:tuple, result:tuple, n=400): # get wider frame containing start and result points 
    xs, ys, xr, yr = start[0], start[1], result[0], result[1]
    delta = max( abs(xs-xr), abs(ys-yr) )
    xmid, ymid = (xs+xr)/2, (ys+yr)/2
    xmin, xmax = xmid-1.5*delta, xmid+1.5*delta, 
    ymin, ymax = ymid-1.5*delta, ymid+1.5*delta, 
    return (xmin, xmax), (ymin, ymax), delta/n


def plot_surf(expr, x_start, x_result, show=False):
    x_range, y_range, step = get_plot_frame(x_start, x_result)
    
    xx = np.linspace(*x_range, 100)
    yy = np.linspace(*y_range, 100)
    x,y=np.meshgrid(xx, yy)
    print(x.shape)
    z = np.array([ expr(x, y) for x, y in zip(x, y) ])

    fig = go.Figure(data=[
            go.Surface(x=tuple(x),y=tuple(y),z=tuple(z) )
            , go.Scatter(x=[x_start[0]], y=[x_start[1]], mode='markers', marker_size=19, fillcolor="red") #, z=[expr(*x_start)] )
        ])
    if show:
        fig.show()
        return None
    html_div = plt_off.plot(fig, output_type='div')
    return html_div

def plot_path(x_list, show=False): # list of tubles # plot path of walking x
    x, y = zip(*x_list)
    
    fig = go.Figure(go.Scatter(x=x, y=y, mode='lines+markers'))
    fig.update_yaxes(scaleanchor = "x", scaleratio = 1 )
    
    if show:
        fig.show()
        return None
    html_div = plt_off.plot(fig, output_type='div') # thats the method we use to generate html div
    return html_div


def plot_progress(x_result, x_path, step_iterations, show=False):
    y = euclidean(x_result, x_path)
    x = np.array(step_iterations)
    fig = go.Figure(go.Scatter(x=x, y=y
        , marker_color='rgba(240, 80, 80, .8)', mode='lines+markers') )
    if show:
        fig.show()
        return None
    html_div = plt_off.plot(fig, output_type='div') # thats the method we use to generate html div
    return html_div

def test_plot_path():
    plot_path([(0,0), (1,1), (10,5)], True)

def test_plot_surf():
    plot_surf(lambda x, y: (x-1)**2+(y+2)**2, (2, 2), (1, -2), show=True)

def test_plot_progress():
    plot_progress((0,0), [(1, 1),(.5,.8),(.1, .33)], [1, 3, 11], show=True)

if __name__ == "__main__":
    test_plot_path()
    test_plot_surf()
    test_plot_progress()