## Click menu bar

`self.actionNew.triggered.connect(lambda: self.clicked("New was clicked"))`

## Update label texts

`self.label.setText(text)`
`self.label.adjustSize()`

## Convert UI files to Py

`pyuic5 -x test3.ui -o test3.py`


# Notes:

- Stackoverflow:
   - Ensure all necessary libraries are imported
   - Ensure QTimer aren't overlapping


# Battle plan

- Sketch layout design
- Iterate each frame animation (show, hide, fade, etc.)
- Research Key.ENTER and clearing input box
- Research update label.text() with tqdm
- Research open folder