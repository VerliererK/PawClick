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

## GUI Application

- Build with CustomTkinter
- Script selection and management
- Configurable hotkeys for start/pause/stop

### Installation

```bash
pip install .[app]
```
### Run the App

```bash
python app/app.py
```

### Build an executable

1. Install Nuitka:
```bash
pip install nuitka
```

2. Build the application:
```bash
python -m nuitka --standalone --onefile --onefile-tempdir-spec="{CACHE_DIR}/PawClick" --lto=yes --follow-imports --windows-uac-admin --windows-icon-from-ico=app/assets/icon.ico --windows-console-mode=disable --enable-plugin=tk-inter --include-package=pawclick --include-data-files=app/assets/icon.ico=assets/icon.ico app/app.py
```
