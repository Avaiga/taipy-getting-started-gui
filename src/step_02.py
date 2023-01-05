from taipy.gui import Gui

text = "Orginal text"

page = """
# Getting started with Taipy GUI

My text: <|{text}|>

Enter a word:

<|{text}|input|>
"""

Gui(page).run()
