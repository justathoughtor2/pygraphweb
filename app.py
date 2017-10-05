from flask import Flask, request, render_template
from sympy import *
import numpy as np
import re
import matplotlib.pyplot as plt, mpld3
import sys

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def equate():
    if request.method == 'GET':
        return render_template('index.html', expression='\\text{None yet!}', solved_expression='\\text{None here either!}', script='', div='')
    else:
        plt.close('all')
        expression_trimmed = request.form.get('expression').replace(' ', '')
        expression_elements = expression_trimmed.split('=')
        variables_trimmed = request.form.get('variables').replace(' ', '')
        variables_array = variables_trimmed.split(',')
        print(variables_array, file=sys.stdout)
        div = 'Please supply a two-variable expression to create a graph!'
        if len(expression_elements) >= 2:
            variables = dict()
            for variable in variables_array:
                try:
                    variables[variable] = symbols(variable)
                    print(variables[variable], file=sys.stdout)
                except Exception:
                    print(variables_array, file=sys.stdout)
                    return render_template('index.html', expression=latex(expression_trimmed), solved_expression='\\text{Does not compute!}', div='Please supply an equality function with real solutions to create a graph!')
                expression_elements[0] = expression_elements[0].replace(variable, 'variables["' + variable + '"]')
                expression_elements[1] = expression_elements[1].replace(variable, 'variables["' + variable + '"]')

            try:
                expression = Eq(eval(expression_elements[0]), eval(expression_elements[1]))
                print(expression, file=sys.stdout)
            except Exception:
                print(expression_elements[0], file=sys.stdout)
                return render_template('index.html', expression=latex(expression_trimmed), solved_expression='\\text{Does not compute!}', div='Please supply an equality function with real solutions to create a graph!')
            try:
                solved_expression = solveset(expression, variables[variables_array[0]])
                print(solved_expression, file=sys.stdout)
            except Exception:
                print(expression, file=sys.stdout)
                return render_template('index.html', expression=latex(expression), solved_expression='\\text{Does not compute!}', div='Please supply an equality function with real solutions to create a graph!')

            mpld3_components = False

            if len(variables_array) == 2 and not type(solved_expression) == EmptySet and not type(solved_expression) == ConditionSet:
                for index, solution in enumerate(solved_expression):
                    if(index > 9):
                        break
                    if variables[variables_array[1]] in solution.free_symbols:
                        if re.match(r'(And|Or)\(.*\)', str(solution)):
                            print(solution, file=sys.stdout)
                            solution_redacted = re.sub(r'(And|Or)\((.*)\)', r'\2', str(solution))
                            solution_trimmed = solution_redacted.replace(' ', '')
                            solution_set = re.split(r'[<>]\=?[\d\-o]+,', solution_trimmed)
                            print(solution_set, file=sys.stdout)
                            try:
                                for sol in solution_set[:5]:
                                    sol = re.sub(r'[<>]\=?[\d\-o]+$', '', sol)
                                    print(sol, file=sys.stdout)
                                    lambda_func = lambdify(variables[variables_array[1]], eval(sol.replace(variables_array[1], 'variables["' + variables_array[1] + '"]')))
                                    var0_vals = np.arange(-15, 15, dtype=float)
                                    var1_vals = lambda_func(var0_vals)
                                    if not mpld3_components:
                                        f = plt.figure()
                                        sub = f.add_subplot(1, 1, 1)
                                        sub.plot(var0_vals, var1_vals)
                                    else:
                                        sub = f.add_subplot(1, 1, 1)
                                        sub.plot(var0_vals, var1_vals)
                                    mpld3_components = True
                            except Exception:
                                print(solved_expression, file=sys.stdout)
                                return render_template('index.html', expression=str(variables[variables_array[0]]) + sol, solved_expression=variables_array[0] + '=' + latex(solved_expression), div='Please supply an equality function with real solutions to create a graph!')
                        else:
                            print(solution, file=sys.stdout)
                            try:
                                lambda_func = lambdify(variables[variables_array[1]], eval(str(solution).replace(variables_array[1], 'variables["' + variables_array[1] + '"]')))
                                var0_vals = np.arange(-15, 15, dtype=float)
                                var1_vals = lambda_func(var0_vals)
                                if not mpld3_components:
                                    f = plt.figure()
                                    sub = f.add_subplot(1, 1, 1)
                                    sub.plot(var0_vals, var1_vals)
                                else:
                                    sub = f.add_subplot(1, 1, 1)
                                    sub.plot(var0_vals, var1_vals)
                                mpld3_components = True
                            except Exception:
                                print(solved_expression, file=sys.stdout)
                                return render_template('index.html', expression=str(variables[variables_array[0]]) + str(solution), solved_expression=variables_array[0] + '=' + latex(solved_expression), div='Please supply an equality function with real solutions to create a graph!')
                if mpld3_components:
                    # print(plots, file=sys.stdout)
                    # plots.show()
                    print(f, file=sys.stdout)
                    div = mpld3.fig_to_html(f)
                else:
                    div = 'No graphable solutions!'

            return render_template('index.html', expression=latex(expression), solved_expression=variables_array[0] + '=' + latex(solved_expression), div=div)
        return render_template('index.html', expression=latex(expression_elements[0]), solved_expression='\\text{Nothing to see here!}', div='Please supply an equality function to create a graph!')
