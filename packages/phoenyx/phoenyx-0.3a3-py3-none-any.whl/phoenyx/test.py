# type: ignore
from phoenyx import *
import phoenyx

import math as m
import numpy as np
import random as rd

from renderer import *
from scrollbar import *
from menu import *
from slider import *
from button import *
from sandbox import *
from vector import *

renderer: Renderer = Renderer(600, 600, "smoltesting")
scrollbar = None


def setup() -> None:
    global scrollbar
    renderer.set_background(51)
    scrollbar = renderer.create_scrollbar(0, 100)


def draw() -> None:
    global scrollbar
    renderer.text(10, 10, f"value : {scrollbar.value}")

    renderer.square((300, 300), 50)


if __name__ == "__main__":
    renderer.run()
