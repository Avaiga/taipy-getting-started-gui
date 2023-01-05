import pandas as pd 
from taipy.gui import Gui, notify

text = "Orginal text"

page = """
# Getting started with Taipy GUI

My text: <|{text}|>

Enter a word:

<|{text}|input|>

<|Run|button|on_action=local_callback|>

<|{dataframe}|table|>

<|{dataframe}|chart|type=bar|x=Text|y=Score Pos|>
"""


dataframe = pd.DataFrame({"Text":[''],
                          "Score Pos":[0],
                          "Score Neu":[0],
                          "Score Neg":[0]})


def local_callback(state):
    print(state.text)
    notify(state, 'info', f'The text is: {state.text}')
    
    temp = state.dataframe.copy()
    state.dataframe = temp.append({"Text":state.text,
                                   "Score Pos":0,
                                   "Score Neu":0,
                                   "Score Neg":0}, ignore_index=True)
    state.text = ""

Gui(page).run()