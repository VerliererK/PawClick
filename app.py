import os
from src.gui import App
from src import utils, runner

if __name__ == "__main__":
    os.makedirs('scripts', exist_ok=True)
    os.makedirs('images', exist_ok=True)
    app = App()
    app.run()
