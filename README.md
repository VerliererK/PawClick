# PawClick

Give Me A Paw !

## Features

- Use mss for screen capture (faster than pyautogui)
- Image recognition and matching

## Installation

Install using pip:

```bash
pip install .
```

## Usage

Here are some basic examples:

### Screen Capture

```python
from pawclick import screenshot

# Capture full screen
img = screenshot()

# Capture specific region (x, y, width, height)
img = screenshot((100, 100, 500, 500))
```

### Image Recognition

```python
from pawclick import load_img, find_img_inwindow

# Load template image
template = load_img("template.png")

# Find image in current window
positions = find_img_inwindow(template)
# Returns a list of found coordinates
```

## Dependencies

- pygetwindow
- keyboard
- mouse
- mss
- Pillow
- numpy
