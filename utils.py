import pyglet

def get_coordinate(
        window:pyglet.window.BaseWindow,
        horizontal_percentage:float|None,
        verticle_percentage:float|None
) -> tuple:
    x, y = None, None
    if horizontal_percentage:
        x = horizontal_percentage * window.width / 100
    if verticle_percentage:
        y = verticle_percentage * window.height / 100
    return x,y
