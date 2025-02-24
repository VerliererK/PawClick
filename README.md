# PawClick

Give Me A Paw !

## Features

- Customizable hotkeys for start/pause/stop scripts
- Use mss for screen capture (faster than pyautogui)

## Installation

1. Clone the repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python app.py
```

2. Select a script from the dropdown menu
3. Configure hotkeys (default: F1=Start, F2=Pause, ESC=Stop)
4. Click "Load" to initialize the script
5. Use the configured hotkeys or GUI buttons to control the script

## Build

1. Install Nuitka:
```bash
pip install nuitka
```

2. Build the application:
```bash
python -m nuitka --standalone --onefile --onefile-tempdir-spec=app --lto=yes --follow-imports --windows-uac-admin --windows-icon-from-ico=assets/icon.ico --windows-console-mode=disable --enable-plugin=tk-inter --include-data-dir=scripts=scripts --include-data-files=assets/icon.ico=assets/icon.ico app.py
```
