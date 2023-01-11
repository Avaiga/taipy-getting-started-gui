> You can download the code of this step [here](../src/step_10.py) or all the steps [here](https://github.com/Avaiga/taipy-getting-started/tree/develop/src).

!!! warning "For Notebooks"

    The "Getting Started" Notebook is available [here](https://docs.taipy.io/en/latest/getting_started/getting_started.ipynb). In Taipy GUI, the process to execute a Jupyter Notebook is different from executing a Python Script.
    It is important to check the [Notebook](https://docs.taipy.io/en/latest/getting_started/getting_started.ipynb) content and see the [documentation](https://docs.taipy.io/en/latest/manuals/gui/notebooks/).

# Step 6: Organize the layout of your App

With just a few steps, you have created a full forecasting application which predicts across multiple days with different parameters. However, the page's layout is not yet optimal and it could be greatly improved. This will be done during this step. To get a more aesthetically pleasing page, three new useful controls will be used. These are:

- [part](https://docs.taipy.io/en/latest/manuals/gui/viselements/part/): creates a group of text/visual elements. A useful property of `part` is _render_. If set to False, it will not display the part. This allows the developer to dynamically display a group of visual elements or not.

```
<|part|render={bool_variable}|
Text
Or visual elements...
|>
```

- [layout](https://docs.taipy.io/en/latest/manuals/gui/viselements/layout/): creates invisible columns where you can put your texts and visual elements. The _columns_ property indicates the width and number of columns. Here, we create three columns of the same width.

```
<|layout|columns=1 1 1|
Button in first column <|Press|button|>

Second column

Third column
|>
```

![Layout](layout.png){ width=500 style="margin:auto;display:block;border: 4px solid rgb(210,210,210);border-radius:7px" }


One strategy to switch from one page to another is:

1. To create a specific Markdown string for each page;

2. Use the Menu or navbar control to switch pages.

This is how you can easily create multiple pages; there are many other ways to do so.
 
First, let’s start by creating the 2 pages.

The first page contains the original chart and slider defined in Step 2. Let’s use the same Markdown as the one defined in Step 2. It is named _page_ (and is also present in Step 9). 


```python
# Our first page is the original page
# (with the slider and the chart that displays a week of the historical data)
page_data_visualization = page
```

![Data Visualization](data_visualization.png){ width=700 style="margin:auto;display:block;border: 4px solid rgb(210,210,210);border-radius:7px" }


Then let’s create our second page which contains the page corresponding to the creation of scenarios seen in Step 9.

```python

page = """
<|toggle|theme|>

# Getting started with Taipy GUI

<|layout|columns=1 1|
<|
My text: <|{text}|>

Enter a word:

<|{text}|input|>

<|Analyze|button|on_action=local_callback|>
|>


<|Table|expandable|
<|{dataframe}|table|width=100%|>
|>

|>

<|layout|columns=1 1 1|
<|
## Positive
<|{np.mean(dataframe['Score Pos'])}|>
|>

<|
## Neutral
<|{np.mean(dataframe['Score Neu'])}|>
|>

<|
## Negative
<|{np.mean(dataframe['Score Neg'])}|>
|>
|>

<|{dataframe}|chart|type=bar|x=Text|y[1]=Score Pos|y[2]=Score Neu|y[3]=Score Neg|y[4]=Overall|color[1]=green|color[2]=grey|color[3]=red|type[4]=line|>
"""
```

![Multi Pages](multi_pages.png){ width=700 style="margin:auto;display:block;border: 4px solid rgb(210,210,210);border-radius:7px" }

