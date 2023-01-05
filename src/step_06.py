
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
                          "Score Neg":[0]})


def local_callback(state):
    print(state.text)
    notify(state, 'Info', f'The text is: {state.text}', True)
    
    # Run for Roberta Model
    encoded_text = tokenizer(state.text, return_tensors='pt')
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    
    temp = state.dataframe.copy()
    state.dataframe = temp.append({"Text":state.text,
                                   "Score Pos":scores[2],
                                   "Score Neu":scores[1],
                                   "Score Neg":scores[0]}, ignore_index=True)
    state.text = ""



page = """
# Getting started with Taipy GUI

My text: <|{text}|>

Enter a word:

<|{text}|input|>

<|Run|button|on_action=local_callback|>

Positive
<|{np.mean(dataframe['Score Pos'])}|>

Neutral
<|{np.mean(dataframe['Score Neu'])}|>

Negative
<|{np.mean(dataframe['Score Neg'])}|>


<|{dataframe}|table|>

<|{dataframe}|chart|type=bar|x=Text|y=Score Pos|>
"""

Gui(page).run()