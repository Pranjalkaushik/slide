import pyglet, pymunk
from controller import jump
from utils import get_coordinate
from game_elements.base import *
from game_elements.ground import get_ground
from game_elements.wall import get_wall
from game_elements.slider import get_slider

window = pyglet.window.Window()
space = pymunk.Space()
space.gravity = (0, -1800)
batch = pyglet.graphics.Batch()

d = Draw(window, space, batch)
ground = get_ground(d, space, window)
wall = get_wall(d, window)
slider = get_slider(d, window)


DT = 1 / 120
_accum = 0


def update(frame_dt):
    global _accum
    global wall_direction
    _accum += min(frame_dt, 0.25)
    while _accum >= DT:
        space.step(DT)
        _accum -= DT
    slider.sync_shape()
    wall.move_left()
    if wall.body and wall.body.position.x < get_coordinate(window, 1, None)[0]:
        wall.body.position = (get_coordinate(window, 99, None)[0], GROUND_LEVEL+10)
    wall.sync_shape()


@window.event
def on_draw():
    window.clear()
    batch.draw()


@window.event
def on_key_press(symbol, modifier):
    if symbol == pyglet.window.key.SPACE:
        jump(slider.body)


pyglet.clock.schedule_interval(update, 1 / 60)
pyglet.app.run()
    
