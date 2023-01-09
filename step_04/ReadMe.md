
# Charts
 
Charts are an essential part of Taipy and of any Web application. A chart is just another visual element with a lot of property to customize it.

Here is the simplest code to create a chart:

```python
<|{[100/x for x in range(1, 100)]}|chart|>
```

## Different useful properties

- x and y:

```python
<|{pd.DataFrame({"x_col":[0,1,2], "y_col1":[4,1,2],})}|chart|x=x_col|y=y_col1|>
```

```python
<|{pd.DataFrame({"x_col":[0,1,2], "y_col_1":[4,1,2], "y_col_2":[3,1,2]})}|chart|x=x_col|y[1]=y_col_1|y[2]=y_col_2|>
```

- color

```python
<|{pd.DataFrame({"x_col":[0,1,2], "y_col_1":[4,1,2], "y_col_2":[3,1,2]})}|chart|x=x_col|y[1]=y_col_1|y[2]=y_col_2|type[1]=bar|color[1]=green|>
```

## Different types of charts

- type

```python
<|{pd.DataFrame({"x_col":[0,1,2], "y_col_1":[4,1,2], "y_col_2":[3,1,2]})}|chart|x=x_col|y[1]=y_col_1|y[2]=y_col_2|type[1]=bar|>
```

## Code

```python
import pandas as pd 
from taipy.gui import Gui, notify

text = "Orginal text"

page = """
# Getting started with Taipy GUI

My text: <|{text}|>

<|{text}|input|>

<|Run|button|on_action=local_callback|>

<|{dataframe}|table|>

<|{dataframe}|chart|type=bar|x=Text|y[1]=Score Pos|y[2]=Score Neu|y[3]=Score Neg|y[4]=Overall|color[1]=green|color[2]=grey|color[3]=red|type[4]=line|>
"""


dataframe = pd.DataFrame({"Text":['Test', 'Other', 'Love'],
                          "Score Pos":[1, 1, 4],
                          "Score Neu":[2, 3, 1],
                          "Score Neg":[1, 2, 0],
                          "Overall":[0, -1, 4]})


def local_callback(state):
    print(state.text)
    notify(state, 'info', f'The text is: {state.text}')
    
    temp = state.dataframe.copy()
    state.dataframe = temp.append({"Text":state.text,
                                   "Score Pos":0,
                                   "Score Neu":0,
                                   "Score Neg":0,
                                   "Overall":0}, ignore_index=True)
    state.text = ""

Gui(page).run()
```