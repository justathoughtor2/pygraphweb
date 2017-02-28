from bottle import get, post, view, request, run
from sympy import *
import matplotlib.pyplot as plt
import string
from bokeh import mpl
from bokeh.embed import components
import re
import math

@get('/')
@view('index')
def get_index():
    return dict(expression='\\text{None yet!}', solved_expression='\\text{None here either!}', script='', div='')

@post('/')
@view('index')
def post_index():
    expression_trimmed = string.replace(request.forms.get('expression'), ' ', '')
    expression_elements = string.split(expression_trimmed, '=')
    variables_trimmed = string.replace(request.forms.get('variables'), ' ', '')
    variables_array = string.split(variables_trimmed, ',')
    if len(expression_elements) >= 2:
        variables = dict()
        for variable in variables_array:
            variables[variable] = symbols(variable)
            expression_elements[0] = string.replace(expression_elements[0], variable, 'variables["' + variable + '"]')
            expression_elements[1] = string.replace(expression_elements[1], variable, 'variables["' + variable + '"]')

        expression = Eq(eval(expression_elements[0]), eval(expression_elements[1]))
        solved_expression = solve(expression, variables[variables_array[0]])
        if len(variables_array) == 2 and len(solved_expression) > 0:
            # x_values_initial = linspace(-10, 10, 100)
            # x_values = False
            # y_values = False
            # y_len = 0
            for solution in solved_expression:
                plot(solution)
                    # if str(solution)[0] != '-':
                        # y_values = []
                        # x_values = []
                        # for x in x_values_initial:
                        #     y = solve(Eq(solution, x))
                        #     if len(y) > 0:
                        #         y_len = len(y)
                        #         run_y = True
                        #         for y_instance in y:
                        #             if not re.search('^\-?\d*\.?\d*$', str(y_instance)):
                        #                 run_y = False
                        #                 break
                        #         if run_y:
                        #             y_values.append(y_instance)
                        #             x_values.append(x)
                        # break
            #     y_values = []
            #     x_values = []
            #     for x in x_values_initial:
            #         print x
            #         y = solve(Eq(solved_expression[0], x))
            #         print y
            #         if len(y) > 0:
            #             y_len = len(y)
            #             prev_y = False
            #             for y_instance in y:
            #                 if not re.search('^\-?\d*\.?\d*$', str(y_instance)):
            #                     if not prev_y == False:
            #                         y_values.append(prev_y)
            #                         x_values.append(x)
            #                 else:
            #                     y_values.append(y_instance)
            #                     x_values.append(x)
            #
            # print x_values
            # print y_values
            # if x_values != False and y_values != False:
            #     i = 0
            #     new_y_values = []
            #     new_x_values = []
            #     # k = 3
            #     # primes = [2]
            #     # invert = False
            #     # while k <= y_len:
            #     #     if k % 2 == 0:
            #     #         k += 1
            #     #     else:
            #     #         for l in range(3, int(math.sqrt(y_len)) + 1, 2):
            #     #             if not y_len % l == 0:
            #     #                 primes.append(l)
            #     #         k += 1
            #     while i < y_len:
            #         # for prime in primes:
            #         #     if i % prime == 0:
            #         #         invert = True
            #         #         break
            #         if not i % 2 == 0:
            #             new_x_values = append(new_x_values, x_values[i::y_len])
            #             new_y_values = append(new_y_values, y_values[i::y_len])
            #             # invert = False
            #         # elif i == y_len - 1:
            #         #     new_x_values = append(new_x_values, x_values[i::y_len][::-1])
            #         #     new_y_values = append(new_y_values, y_values[i::y_len][::-1])
            #         else:
            #             new_x_values = append(new_x_values, x_values[i::y_len][::-1])
            #             new_y_values = append(new_y_values, y_values[i::y_len][::-1])
            #         i = i + 1
            #     j = 0
            #     while j < len(new_y_values):
            #         print new_y_values[j]
            #         print new_x_values[j]
            #         j = j + 1
            script, div = components(mpl.to_bokeh())
        else:
            script = ''
            div = 'Please supply a two-variable expression to create a graph!'
        return dict(expression=latex(expression), solved_expression=variables_array[0] + '=' + latex(solved_expression), script=script, div=div)
    return dict(expression=latex(expression_elements[0]), solved_expression='\\text{Nothing to see here!}', script='', div='Please supply an equality function to create a graph!')



run(host='localhost', port=8080, debug=True)
