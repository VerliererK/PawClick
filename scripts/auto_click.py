from src.runner import ScriptRunner
from src.utils import click
import time


def run():
    click()
    time.sleep(0.1)


if __name__ == "__main__":
    runner = ScriptRunner('middle', 'right', run=run, loop=True)
