import keyboard
import mouse
import numpy as np
import pygetwindow as gw
from PIL import Image
from mss import mss


def screenshot(region=None) -> np.ndarray:
    """
    Capture screen using mss library
    Args:
        region (tuple, optional): Screenshot region (x, y, width, height)
    Returns:
        numpy array: Screenshot image in RGB format
    """
    with mss() as sct:
        monitor = sct.monitors[1] if region is None else {'top': region[1], 'left': region[0], 'width': region[2], 'height': region[3]}
        im = sct.grab(monitor)
    img = np.asarray(im, dtype=np.uint8)
    return np.flip(img[:, :, :3], 2)


def load_img(img_file) -> np.ndarray:
    return np.asarray(Image.open(img_file))[:, :, :3]


def find_img(large_image: np.ndarray, small_image: np.ndarray, threshold=0, find_all=False) -> list:
    """
    Find small image in a larger image using numpy
    Args:
        large_image (numpy array): Large image to search in
        small_image (numpy array): Template image to find
        find_all (bool, optional): Whether to return all matches or just the first one
    Returns:
        list: List of coordinates where template is found
    """

    def array_equal(arr1, arr2):
        if threshold == 0:
            return np.array_equal(arr1, arr2)
        diff = np.abs(arr1.astype(np.int16) - arr2.astype(np.int16))
        return np.mean(diff) < threshold

    small_height, small_width = small_image.shape[:2]
    large_height, large_width = large_image.shape[:2]

    matches = np.all(large_image[:large_height - small_height + 1, :large_width - small_width + 1] == small_image[0, 0, :], axis=-1)
    coordinates = np.column_stack(np.where(matches))

    locations = []
    for coord in coordinates:
        y, x = coord
        if small_height > 1 and not array_equal(large_image[y + 1, x], small_image[1, 0]):
            continue
        if array_equal(large_image[y:y + small_height, x:x + small_width], small_image):
            pos = [int(x), int(y)]
            locations.append(pos)

            if not find_all:
                break
    return locations


def find_img_inwindow(image: np.ndarray, threshold=0, find_all: bool = False) -> list:
    region = None
    active_window = gw.getActiveWindow()
    if active_window:
        region = (active_window.left, active_window.top, active_window.width, active_window.height)
    pos = find_img(screenshot(region), image, threshold=threshold, find_all=find_all)
    for p in pos:
        p[0] += region[0] if region else 0
        p[1] += region[1] if region else 0
    return pos


def keypress(key: str):
    keyboard.press_and_release(key)


def click(button: str = 'left'):
    mouse.click(button)


def move(x: int, y: int, absolute=True):
    mouse.move(x, y, absolute=absolute)


def position():
    return mouse.get_position()
