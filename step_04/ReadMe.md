
# Step 4: Charts
 
Charts are an essential part of Taipy and of any Web application. A chart is just another visual element with a lot of property to customize it.

Here is one of the simplest code to create a chart:

```python
list_to_display = [100/x for x in range(1, 100)]
"<|{list_to_display}|chart|>"
```

Different formats can be passed to a chart element: a list, a Numpy array or a Pandas Dataframe.

## Different useful properties

Taipy charts are based on Plotly charts. Like any other visual elements, charts have a lot of parameters. Some of them can be indexed in order to change properties for specific traces of the chart. 

Here are few of the most essential properties. You can also look at the [documentation]() for more information.
 - x and y are used to define the axis of the chart. Note that even if data inside columns are dynamic, the name of columns to display in a chart are not.

```python
data = pd.DataFrame({"x_col":[0,1,2], "y_col1":[4,1,2]})
"<|{data}|chart|x=x_col|y=y_col1|>"
```

 - x and y can be indexed to add more traces to the chart:

```python
data = pd.DataFrame({"x_col":[0,1,2], "y_col_1":[4,1,2], "y_col_2":[3,1,2]})
"<|{data}|chart|x=x_col|y[1]=y_col_1|y[2]=y_col_2|>"
```

 - Taipy provides a lot of different options to customize graphs. _color_ is one of them:

```python
data = pd.DataFrame({"x_col":[0,1,2], "y_col_1":[4,1,2], "y_col_2":[3,1,2]})
"<|{data}|chart|x=x_col|y[1]=y_col_1|y[2]=y_col_2|type[1]=bar|color[1]=green|>"
```

## Different types of charts

Different types are available: maps, bar charts, pie charts, line charts, 3D charts, ... To know how to use them quickly, types are listed [here]().  If compatible, two types can also be use together like _scatter_, _line_ and _bar_ on the same chart. 

```python
data = pd.DataFrame({"x_col":[0,1,2], "y_col_1":[4,1,2], "y_col_2":[3,1,2]})
"<|{data}|chart|x=x_col|y[1]=y_col_1|y[2]=y_col_2|type[1]=bar|>"
```

## Code

A chart is added to our code to visualize the score given by our NLP algorihtm to different lines.

```python

page = """
... put previous Markdown page here

<|{dataframe}|table|>

<|{dataframe}|chart|type=bar|x=Text|y[1]=Score Pos|y[2]=Score Neu|y[3]=Score Neg|y[4]=Overall|color[1]=green|color[2]=grey|color[3]=red|type[4]=line|>
"""


dataframe = pd.DataFrame({"Text":['Test', 'Other', 'Love'],
                          "Score Pos":[1, 1, 4],
                          "Score Neu":[2, 3, 1],
                          "Score Neg":[1, 2, 0],
                          "Overall":[0, -1, 4]})

```

## Quick tip to write visual elements

In order to simplify the creation of a visual element. Each of them has a "property" parameter where a Ptyhon dictionnary of property can ba directly passed. To replicate the graph above, we could do:

```python
property_chart = {"type":bar,
                  "x":"Text",
                  "y[1]":"Score Pos",
                  "y[2]":"Score Neu",
                  "y[3]":"Score Neg",
                  "y[4]":"Overall",
                  "color[1]":"green",
                  "color[2]":"grey",
                  "color[3]":"red",
                  "type[4]":"line"
                 }

page = """
...
<|{dataframe}|chart|property={property_chart}|>
...
"""

```
