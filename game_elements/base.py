
import pyglet, pymunk
from utils import get_coordinate
from controller import GROUND_VELOCITY

TITLE = 'GO SLIDE !'
TITLE_FONT_SIZE = 36
SLIDER_SIZE = 10
GROUND_THICKNESS = 10
GROUND_LEVEL = 20

class GameObject:

    def __init__(
            self,
            window:pyglet.window.BaseWindow,
            shape:pyglet.shapes.ShapeBase|None=None,
            body:pymunk.Body|None=None,
            collider:pymunk.Shape|None=None
    ):
        self.window = window
        self.shape = shape
        self.body = body
        self.collider = collider
    
    def update_pos(self, horizontal_percentage:float, verticle_percentage:float):
        pos = get_coordinate(self.window, horizontal_percentage, verticle_percentage)
        if self.shape:
            self.shape.position = pos
        if self.body:
            self.body.position = pos
        if self.collider:
            self.collider.position = pos

    def move_left(self):
        if self.body:
            self.body.velocity = (-GROUND_VELOCITY, self.body.velocity.y)

    def move_right(self):
        if self.body:
            self.body.velocity = (GROUND_VELOCITY, self.body.velocity.y)
    
    def sync_shape(self):
        if self.shape and self.body:
            self.shape.position = self.body.position



class Draw:
    
    def __init__(
            self,
            window:pyglet.window.BaseWindow,
            space:pymunk.Space,
            batch:pyglet.graphics.Batch
    ):
        self.window = window
        self.space = space
        self.batch = batch

    def draw_text(self, text, pos, size):
        t = pyglet.text.Label(
            text,
            font_name='Times New Roman',
            font_size=size,
            x=pos[0],
            y=pos[1],
            anchor_x='center',
            anchor_y='center'
            )
        return t

    def draw_ground(self)->pyglet.shapes.ShapeBase:
        ground_shape = pyglet.shapes.Line(
            0, GROUND_LEVEL,
            self.window.width, GROUND_LEVEL,
            thickness = GROUND_THICKNESS,
            color=(80,200,120),
            batch=self.batch
        )
        return ground_shape

    def draw_slider(self)->tuple:
        slider_shape = pyglet.shapes.Rectangle(
            get_coordinate(self.window, 50, None)[0],
            get_coordinate(self.window, None, 50)[1],
            width=SLIDER_SIZE,
            height=SLIDER_SIZE,
            color=(80,200,120),
            batch=self.batch
        )
        slider_shape.anchor_position = (SLIDER_SIZE/2, SLIDER_SIZE/2)
        slider_body = pymunk.Body(
            mass=1,
            moment=float('inf'),
        )
        slider_body.position = get_coordinate(self.window, 50, 50)
        return slider_shape, slider_body


    def draw_wall(self, pos:tuple, width:float, height:float):
        wall_shape = pyglet.shapes.Rectangle(
            pos[0],
            pos[1],
            width=width,
            height=height,
            color=(80,200,120),
            batch=self.batch
        )
        wall_shape.anchor_position = (width/2, height/2)
        wall_body = pymunk.Body(
            mass=100,
            moment=float('inf'),
        )
        wall_body.position = pos
        return wall_shape, wall_body

    def draw_box(self, pos, size):
        ...

    def add_collider(
            self,
            body:pymunk.Body,
            collider_type:str|None=None,
            size:tuple=(),
            pos_1:tuple=(),
            pos_2:tuple=(),
            friction:int=1
    )->pymunk.Shape|None:
        collider = None
        if collider_type == 'poly': 
            collider = pymunk.Poly.create_box(
                body,
                size
            )
            collider.friction = friction
            self.space.add(body, collider)

        elif collider_type == 'segment':
            collider = pymunk.Segment(
                body,
                pos_1,
                pos_2,
                size[0]
            )
            collider.friction = friction
            self.space.add(collider)
        return collider
