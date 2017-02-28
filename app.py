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
            for solution in solved_expression:
                plot(solution)
            script, div = components(mpl.to_bokeh())
        else:
            script = ''
            div = 'Please supply a two-variable expression to create a graph!'
        return dict(expression=latex(expression), solved_expression=variables_array[0] + '=' + latex(solved_expression), script=script, div=div)
    return dict(expression=latex(expression_elements[0]), solved_expression='\\text{Nothing to see here!}', script='', div='Please supply an equality function to create a graph!')

run(host='localhost', port=8080, debug=True)
