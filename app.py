from bottle import get, post, view, request, run
from sympy import *
import string
from bokeh import mpl
from bokeh.embed import components
import re
import matplotlib.pyplot as plt

@get('/')
@view('index')
def get_index():
    return dict(expression='\\text{None yet!}', solved_expression='\\text{None here either!}', script='', div='')

@post('/')
@view('index')
def post_index():
    plt.close('all')
    expression_trimmed = string.replace(request.forms.get('expression'), ' ', '')
    expression_elements = string.split(expression_trimmed, '=')
    variables_trimmed = string.replace(request.forms.get('variables'), ' ', '')
    variables_array = string.split(variables_trimmed, ',')
    script = ''
    div = 'Please supply a two-variable expression to create a graph!'
    if len(expression_elements) >= 2:
        variables = dict()
        for variable in variables_array:
            variables[variable] = symbols(variable)
            expression_elements[0] = string.replace(expression_elements[0], variable, 'variables["' + variable + '"]')
            expression_elements[1] = string.replace(expression_elements[1], variable, 'variables["' + variable + '"]')

        expression = Eq(eval(expression_elements[0]), eval(expression_elements[1]))
        solved_expression = solveset(expression, variables[variables_array[0]], domain=S.Reals)

        bokeh_components = False

        if len(variables_array) == 2 and not type(solved_expression) == EmptySet and not type(solved_expression) == ConditionSet:
            for index, solution in enumerate(solved_expression):
                if(index > 9):
                    break
                if variables[variables_array[1]] in solution.free_symbols:
                    if re.match(r'(And|Or)\(.*\)', str(solution)):
                        print solution
                        solution_redacted = re.sub(r'(And|Or)\((.*)\)', r'\2', str(solution))
                        solution_trimmed = string.replace(solution_redacted, ' ', '')
                        solution_set = re.split(r'[<>]\=?[\d\-o]+,', solution_trimmed)
                        print solution_set
                        for sol in solution_set[:5]:
                            sol = re.sub(r'[<>]\=?[\d\-o]+$', '', sol)
                            print sol
                            if not bokeh_components:
                                plots = plot(eval(string.replace(sol, variables_array[1], 'variables["' + variables_array[1] + '"]')), (variables[variables_array[1]], -100, 100), ylabel=variables_array[0], xlabel=variables_array[1])
                            else:
                                plots.append(plot(eval(string.replace(sol, variables_array[1], 'variables["' + variables_array[1] + '"]')), (variables[variables_array[1]], -100, 100), ylabel=variables_array[0], xlabel=variables_array[1])[0])
                            bokeh_components = True
                    else:
                        print solution
                        if not bokeh_components:
                            plots = plot(eval(string.replace(str(solution), variables_array[1], 'variables["' + variables_array[1] + '"]')), (variables[variables_array[1]], -100, 100), ylabel=variables_array[0], xlabel=variables_array[1])
                        else:
                            plots.append(plot(eval(string.replace(str(solution), variables_array[1], 'variables["' + variables_array[1] + '"]')), (variables[variables_array[1]], -100, 100), ylabel=variables_array[0], xlabel=variables_array[1])[0])
                        bokeh_components = True
            if bokeh_components:
                plots.show()
                script, div = components(mpl.to_bokeh())
            else:
                script = ''
                div = 'No graphable solutions!'

        return dict(expression=latex(expression), solved_expression=variables_array[0] + '=' + latex(solved_expression), script=script, div=div)
    return dict(expression=latex(expression_elements[0]), solved_expression='\\text{Nothing to see here!}', script='', div='Please supply an equality function to create a graph!')

run(host='localhost', port=8080, debug=True)
