# Step 5: Interactiveness

As shown before, parameters and variables in Taipy are dynamic. The same follows for every type of object even dataframes. Therefore, operations can be done on dataframes and results will be shown in real time on the GUI. Taipy is notified of a change when variables are being assigned through `=` like `state.xxx = yyy`.

Any expression containing `xxx` in the Markdown will be reloaded. It can be  simple charts or tables but it can also be expression like this:

```python
## Positive
<|{np.mean(dataframe['Score Pos'])}|text|>

## Neutral
<|{np.mean(dataframe['Score Neu'])}|text|>

## Negative
<|{np.mean(dataframe['Score Neg'])}|text|>
```

Using this kind of expression creates direct connection between visual elements without coding anything. I can be largely used to create an application.

## Code

The code below uses this concept to create metrics on the dataframe generated. The code for NLP is here provided; it doesn't concern Taipy but is useful for the application.

```python
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

import numpy as np
import pandas as pd 
from taipy.gui import Gui, notify

text = "Orginal text"

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

dataframe = pd.DataFrame({"Text":[''],
                          "Score Pos":[0],
                          "Score Neu":[0],
                          "Score Neg":[0],
                          "Overall":[0]})

def analize_text(text):
    # Run for Roberta Model
    encoded_text = tokenizer(text, return_tensors='pt')
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    
    return {"Text":text,
            "Score Pos":scores[2],
            "Score Neu":scores[1],
            "Score Neg":scores[0],
            "Overall":scores[2]-scores[0]}


def local_callback(state):
    print(state.text)
    notify(state, 'Info', f'The text is: {state.text}', True)
    temp = state.dataframe.copy()
    scores = analize_text(state.text)
    state.dataframe = temp.append(scores, ignore_index=True)
    state.text = ""



page = """
<|toggle|theme|>

# Getting started with Taipy GUI

My text: <|{text}|>

Enter a word:

<|{text}|input|>

<|Analyze|button|on_action=local_callback|>

## Positive
<|{np.mean(dataframe['Score Pos'])}|text|format=%.2f|>

## Neutral
<|{np.mean(dataframe['Score Neu'])}|text|format=%.2f|>

## Negative
<|{np.mean(dataframe['Score Neg'])}|text|format=%.2f|>

<|{dataframe}|table|>

<|{dataframe}|chart|type=bar|x=Text|y[1]=Score Pos|y[2]=Score Neu|y[3]=Score Neg|y[4]=Overall|color[1]=green|color[2]=grey|color[3]=red|type[4]=line|>
"""

Gui(page).run()
```