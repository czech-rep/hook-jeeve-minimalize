post_dict = {'x0': '1.1 , 4.5, 6'}
start_point = post_dict["x0"]  # start point is a string: 1.1,4.5,6, ..
start_point = tuple( float(x) for x in start_point.split(',') )

print(start_point)