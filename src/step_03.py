from taipy.gui import Gui, notify

text = "Orginal text"

# Definition of the page
page = """
# Getting started with Taipy GUI

My text: <|{text}|>

<|{text}|input|>

<|Run local|button|on_action=local_callback|>
"""

def local_callback(state):
    print(state.text)
    notify(state, 'info', f'The text is: {state.text}')

def on_change(state, var_name, var_value):
    print(var_name, var_value, state.text)
    if var_name == "text":
        ...


Gui(page).run()