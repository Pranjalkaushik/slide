import pyglet, pymunk
import conf
import random
from pymunk.pyglet_util import DrawOptions
from controller import jump
from utils import are_in_contact, get_coordinate, on_ground
from game_elements.base import Draw, GameObject, GameWorld 
from game_elements.ground import get_ground
from game_elements.wall import get_wall, next_height
from game_elements.slider import get_slider
from game_elements.label import get_label

window = pyglet.window.Window(fullscreen=True)
space = pymunk.Space()
space.gravity = conf.GRAVITY
draw_options = DrawOptions()
batch = pyglet.graphics.Batch()

d = Draw(window, space, batch)
label = get_label('0', d, space, window)
ground = get_ground(d, space, window)
wall = get_wall(d, window)
slider = get_slider(d, window)

walls = [wall,]


DT = 1 / 120
_accum = 0
points = 0

wall_pos = {f'wall{id(wall)}': wall.body.position}

def update(frame_dt):
    global _accum
    global wall_direction
    global points
    
    if (slider.body.position[0] <  get_coordinate(window, -1, None)[0]) or are_in_contact(slider, walls):
        label.label.text = "Game Over !"
        return

    _accum += min(frame_dt, 0.25)
    while _accum >= DT:
        space.step(DT)
        _accum -= DT
    slider.sync_shape()
    if on_ground(slider):
        conf.JUMP_COUNT = 2
   
    to_delete = []
    to_add = []
    
    for wall in walls:
        slider_pos = slider.body.position
        # before the move
        wall_pos_x_bm = wall_pos[f'wall{id(wall)}'][0]
        wall.move_left()
        # after the move
        wall_pos_x_am = wall.body.position[0]
        if wall_pos_x_bm > slider_pos[0] and wall_pos_x_am < slider_pos[0]:
            slider.move_right(1.5)
            points += 1
            label.label.text = str(points)
       
        if wall.body.position[0] < get_coordinate(window, -5, None)[0]:
            to_delete += [wall]
            to_add.append(get_wall(d, window))
            conf.GROUND_VELOCITY = min(conf.MAX_GROUND_VELOCITY, random.randrange(conf.GROUND_VELOCITY, conf.GROUND_VELOCITY+100)) 
        wall.sync_shape()
        wall_pos[f'wall{id(wall)}'] = wall.body.position
    
    for wall in to_delete:
        space.remove(wall.body)
        space.remove(wall.collider)
        delattr(GameWorld, f"wall{id(wall)}")
        walls.remove(wall)

    for wall in to_add:
        walls.append(wall)
        wall_pos[f'wall{id(wall)}'] = wall.body.position

    


@window.event
def on_draw():
    window.clear()
    batch.draw()
    #space.debug_draw(draw_options)


@window.event
def on_key_press(symbol, modifier):
    if symbol == pyglet.window.key.SPACE:
        jump(slider)


pyglet.clock.schedule_interval(update, 1 / 60)
pyglet.app.run()
    
