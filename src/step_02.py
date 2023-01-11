from taipy.gui import Gui

text = "Orginal text"

page = """
<|toggle|theme|>

# Getting started with Taipy GUI

My text: <|{text}|>

<|{text}|input|>
"""

Gui(page).run()