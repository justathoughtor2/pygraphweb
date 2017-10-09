from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from sympy import *
import numpy as np
import re
import matplotlib.pyplot as plt, mpld3
import sys
import pandas as pd
from scipy.interpolate import spline

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['csv'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
                                    var0_vals = np.linspace(-15, 15, 200)
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
                                var0_vals = np.linspace(-15, 15, 200)
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

@app.route('/data', methods=['GET', 'POST'])
def calculate():
    if request.method == 'GET':
        return render_template('data.html', expression='\\text{None yet!}', solved_expression='\\text{None here either!}', script='', div='')
    else:
        plt.close('all')
        # if 'input-data' not in request.files:
        #     return redirect(request.url)
        file = request.files['input-data']
        # if file.filename == '':
        #     return redirect(request.url)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        # expression_elements = expression_trimmed.split('=')
        data_variable = re.sub(r'[^A-Za-z\.\-]([A-Za-z\.\-])', r'\1', request.form.get('column-name'))
        time_variable = re.sub(r'[^A-Za-z\.\-]([A-Za-z\.\-])', r'\1', request.form.get('column-name-time'))
        # print(variables_array, file=sys.stdout)
        div = 'Please supply a data variable and time variable to create a graph!'

        df = pd.read_csv(file)

        # for variable in variables_array:
        #     try:
        #         if not variable in df.columns:
        #             raise Exception
        #         # variables[variable] = symbols(variable)
        #         # print(variables[variable], file=sys.stdout)
        #     except Exception:
        #         # print(variables_array, file=sys.stdout)
        #         return render_template('data.html', expression=latex(expression_trimmed), solved_expression='\\text{Does not compute!}', div='Please supply a data variable and time variable to create a graph!')
            # expression_elements[0] = expression_elements[0].replace(variable, 'variables["' + variable + '"]')
            # expression_elements[1] = expression_elements[1].replace(variable, 'variables["' + variable + '"]')
        # try:
            # if not time_variable in df.columns or not data_variable in df.columns:
            #     raise Exception
        df[time_variable] = pd.to_datetime(df[time_variable])
        count_per_month = df.groupby(time_variable)[data_variable].value_counts().unstack().resample('1M').sum()
        print(count_per_month, file=sys.stderr)
        # calcs_in = pd.DataFrame()
        # previous_count = 0
        # for index, count in enumerate(count_per_month):
        #     total_count = previous_count + count
        #     calcs_in.append(df[data_variable][previous_count:total_count].value_counts())
        #     previous_count += count
        # print(calcs_in, file=sys.stderr)
        # calcs = {}
        # for index, column in calcs_in.items():
        #     if not index in calcs:
        #         calcs[index] = []
        #     calcs[index].append(column.transpose())
        f = plt.figure(figsize=(10, 8))
        # print(calcs, file=sys.stderr)
        sub = f.add_subplot(1, 1, 1)
        subplots = []
        labels = []
        x_sample = np.linspace(0, len(count_per_month), 300)
        for column in count_per_month.sort_values(count_per_month.first_valid_index(),axis=1,ascending=False).ix[:,0:12]:
            y_sample = spline(range(0, len(count_per_month[column])), count_per_month[column], x_sample)
            subplots.append(plt.plot(x_sample[::-1], y_sample[::-1], label=column)[0])
            labels.append(column)
        plt.legend(handles=subplots, labels=labels)
        div = mpld3.fig_to_html(f)
        return render_template('data.html', expression='count(' + data_variable + ')', solved_expression=count_per_month, div=div)

        # except Exception:
        #     return redirect(request.url)
        # try:
        #     expression = Eq(eval(expression_elements[0]), eval(expression_elements[1]))
        #     print(expression, file=sys.stdout)
        # except Exception:
        #     print(expression_elements[0], file=sys.stdout)
        #     return render_template('index.html', expression=latex(expression_trimmed), solved_expression='\\text{Does not compute!}', div='Please supply an equality function with real solutions to create a graph!')
        # try:
        #     solved_expression = solveset(expression, variables[variables_array[0]])
        #     print(solved_expression, file=sys.stdout)
        # except Exception:
        #     print(expression, file=sys.stdout)
        #     return render_template('index.html', expression=latex(expression), solved_expression='\\text{Does not compute!}', div='Please supply an equality function with real solutions to create a graph!')
        #
        # mpld3_components = False
        #
        # if len(variables_array) == 2 and not type(solved_expression) == EmptySet and not type(solved_expression) == ConditionSet:
        #     for index, solution in enumerate(solved_expression):
        #         if(index > 9):
        #             break
        #         if variables[variables_array[1]] in solution.free_symbols:
        #             if re.match(r'(And|Or)\(.*\)', str(solution)):
        #                 print(solution, file=sys.stdout)
        #                 solution_redacted = re.sub(r'(And|Or)\((.*)\)', r'\2', str(solution))
        #                 solution_trimmed = solution_redacted.replace(' ', '')
        #                 solution_set = re.split(r'[<>]\=?[\d\-o]+,', solution_trimmed)
        #                 print(solution_set, file=sys.stdout)
        #                 try:
        #                     for sol in solution_set[:5]:
        #                         sol = re.sub(r'[<>]\=?[\d\-o]+$', '', sol)
        #                         print(sol, file=sys.stdout)
        #                         lambda_func = lambdify(variables[variables_array[1]], eval(sol.replace(variables_array[1], 'variables["' + variables_array[1] + '"]')))
        #                         var0_vals = np.linspace(-15, 15, 200)
        #                         var1_vals = lambda_func(var0_vals)
        #                         if not mpld3_components:
        #                             f = plt.figure()
        #                             sub = f.add_subplot(1, 1, 1)
        #                             sub.plot(var0_vals, var1_vals)
        #                         else:
        #                             sub = f.add_subplot(1, 1, 1)
        #                             sub.plot(var0_vals, var1_vals)
        #                         mpld3_components = True
        #                 except Exception:
        #                     print(solved_expression, file=sys.stdout)
        #                     return render_template('index.html', expression=str(variables[variables_array[0]]) + sol, solved_expression=variables_array[0] + '=' + latex(solved_expression), div='Please supply an equality function with real solutions to create a graph!')
        #             else:
        #                 print(solution, file=sys.stdout)
        #                 try:
        #                     lambda_func = lambdify(variables[variables_array[1]], eval(str(solution).replace(variables_array[1], 'variables["' + variables_array[1] + '"]')))
        #                     var0_vals = np.linspace(-15, 15, 200)
        #                     var1_vals = lambda_func(var0_vals)
        #                     if not mpld3_components:
        #                         f = plt.figure()
        #                         sub = f.add_subplot(1, 1, 1)
        #                         sub.plot(var0_vals, var1_vals)
        #                     else:
        #                         sub = f.add_subplot(1, 1, 1)
        #                         sub.plot(var0_vals, var1_vals)
        #                     mpld3_components = True
        #                 except Exception:
        #                     print(solved_expression, file=sys.stdout)
        #                     return render_template('index.html', expression=str(variables[variables_array[0]]) + str(solution), solved_expression=variables_array[0] + '=' + latex(solved_expression), div='Please supply an equality function with real solutions to create a graph!')
        #     if mpld3_components:
        #         # print(plots, file=sys.stdout)
        #         # plots.show()
        #         print(f, file=sys.stdout)
        #         div = mpld3.fig_to_html(f)
        #     else:
        #         div = 'No graphable solutions!'

    #     return render_template('index.html', expression=latex(expression), solved_expression=variables_array[0] + '=' + latex(solved_expression), div=div)
    # return render_template('index.html', expression=latex(expression_elements[0]), solved_expression='\\text{Nothing to see here!}', div='Please supply an equality function to create a graph!')
