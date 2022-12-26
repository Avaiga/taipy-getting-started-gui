import json


def add_line(source, line, step):

    line = line.replace('Getting Started with Taipy Core', 'Getting Started with Taipy Core on Notebooks')
    line = line.replace('(../src/', '(https://docs.taipy.io/en/latest/getting_started/src/')
    line = line.replace('(time_series.csv)', '(https://docs.taipy.io/en/latest/getting_started/step_01/time_series.csv)') #!!!!!
    line = line.replace('(time_series_2.csv)', '(https://docs.taipy.io/en/latest/getting_started/step_01/time_series_2.csv)')


    if line.startswith('!['):
        if step != 'index':
            line = line.replace('(', '(https://docs.taipy.io/en/latest/getting_started/' + step + '/')
        else:
            line = line.replace('(', '(https://docs.taipy.io/en/latest/getting_started/')

        # conversion of Markdown image to HTML
        img_src = line.split('](')[1].split(')')[0]
        width = line.split('](')[1].split(')')[1].split(' ')[1]

        source.append('<div align="center">\n')
        source.append(f' <img src={img_src} {width}>\n')
        source.append('</div>\n')



    elif step == 'step_00' and line.startswith('from taipy'):
        source.append("from taipy.gui import Gui, Markdown\n")
    elif 'Notebook' in line and 'step' in step:
        pass
    else:
        source.append(line + '\n')

    return source


def detect_new_cell(notebook, source, cell, line, execution_count, force_creation=False):
    if line.startswith('```python') or line.startswith('```') and cell == 'code' or force_creation:
        source = source[:-1]

        if cell == 'code':
            notebook['cells'].append({
                "cell_type": "code",
                "metadata": {},
                "outputs": [],
                "execution_count": execution_count,
                "source": source
            })
            cell = 'markdown'
            execution_count += 1
        else:
            notebook['cells'].append({
                "cell_type": "markdown",
                "metadata": {},
                "source": source
            })
            cell = 'code'

        source = []

    return cell, source, notebook, execution_count


def create_introduction(notebook, execution_count):
    with open('index.md', 'r') as f:
        text = f.read()

    split_text = text.split('\n')
    source = []

    for line in split_text:
        if not line.startswith('``` console'):
            add_line(source, line, 'index')
        else:
            break

    notebook['cells'].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": source
    })

    notebook['cells'].append({
        "cell_type": "code",
        "metadata": {},
        "outputs": [],
        "execution_count": execution_count,
        "source": ['# !pip install taipy\n']
    })

    notebook['cells'].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": ['## Using Notebooks\n',]
    })

    execution_count += 1
    return notebook, execution_count


def create_steps(notebook, execution_count):
    steps = ['step_0' + str(i) for i in range(1, 8)]
    source = []

    for step in steps:
        if source != []:
            cell, source, notebook, execution_count = detect_new_cell(notebook,
                                                                      source,
                                                                      cell,
                                                                      line,
                                                                      execution_count,
                                                                      force_creation=True)

        with open(step + '/ReadMe.md', 'r') as f:
            text = f.read()

        split_text = text.split('\n')
        cell = "markdown"

        for_studio = False

        for line in split_text:
            if '=== "Taipy Studio' in line:
                for_studio = True
            if '=== "Python configuration"' in line:
                for_studio = False
                
            if not for_studio:
                add_line(source, line, step)
                cell, source, notebook, execution_count = detect_new_cell(notebook, source, cell, line, execution_count)

    return notebook, execution_count


if __name__ == '__main__':
    notebook = {
        "cells": [],
        "metadata": {
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3"
            },
            "orig_nbformat": 4
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

    execution_count = 0

    notebook, execution_count = create_introduction(notebook, execution_count)
    notebook, execution_count = create_steps(notebook, execution_count)

    with open('getting_started.ipynb', 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)