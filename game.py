from pyglet.window.key import G
import pyglet, pymunk

window = pyglet.window.Window()

TITLE = 'GO SLIDE !'
TITLE_FONT_SIZE = 36
SLIDER_SIZE = 10
JUMP_VELOCITY = 700
GROUND_VELOCITY = 600

#-----------------------------------------utils---------------------------------------------

def get_coordinate(horizontal_percentage:float|None, verticle_percentage:float|None) -> tuple:
    x, y = None, None
    if horizontal_percentage:
        x = horizontal_percentage * window.width / 100
    if verticle_percentage:
        y = verticle_percentage * window.height / 100
    return x,y

def jump(body):
    body.apply_impulse_at_local_point((0, JUMP_VELOCITY))

GROUND_LEVEL = get_coordinate(None, 20)[1]
GROUND_THICKNESS = 10

class GameObject:

    def __init__(
            self,
            shape:pyglet.shapes.ShapeBase|None=None,
            body:pymunk.Body|None=None,
            collider:pymunk.Shape|None=None
    ):
        self.shape = shape
        self.body = body
        self.collider = collider
    
    def update_pos(self, horizontal_percentage:float, verticle_percentage:float):
        pos = get_coordinate(horizontal_percentage, verticle_percentage)
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
            space:pymunk.Space,
            batch:pyglet.graphics.Batch
    ):
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
            window.width, GROUND_LEVEL,
            thickness = GROUND_THICKNESS,
            color=(80,200,120),
            batch=batch
        )
        return ground_shape

    def draw_slider(self)->tuple:
        slider_shape = pyglet.shapes.Rectangle(
            get_coordinate(50, None)[0],
            get_coordinate(None, 50)[1],
            width=SLIDER_SIZE,
            height=SLIDER_SIZE,
            color=(80,200,120),
            batch=batch
        )
        slider_shape.anchor_position = (SLIDER_SIZE/2, SLIDER_SIZE/2)
        slider_body = pymunk.Body(
            mass=1,
            moment=float('inf'),
        )
        slider_body.position = get_coordinate(50, 50)
        return slider_shape, slider_body


    def draw_wall(self, pos:tuple, width:float, height:float):
        wall_shape = pyglet.shapes.Rectangle(
            pos[0],
            pos[1],
            width=width,
            height=height,
            color=(80,200,120),
            batch=batch
        )
        wall_shape.anchor_position = (width/2, height/2)
        wall_body = pymunk.Body(
            mass=1,
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
            space.add(body, collider)

        elif collider_type == 'segment':
            collider = pymunk.Segment(
                body,
                pos_1,
                pos_2,
                size[0]
            )
            collider.friction = friction
            space.add(collider)
        return collider

#---------------------------- game objects ------------------------------

space = pymunk.Space()
space.gravity = (0, -1800)
batch = pyglet.graphics.Batch()

d = Draw(space, batch)

label = d.draw_text(
    TITLE,
    get_coordinate(50, 95),
    TITLE_FONT_SIZE
)

slider_shape, slider_body = d.draw_slider()
slider_collider = d.add_collider(
    slider_body,
    'poly',
    (SLIDER_SIZE, SLIDER_SIZE)
)
slider = GameObject(
    shape=slider_shape,
    body=slider_body,
    collider=slider_collider
)

ground_shape = d.draw_ground()
ground_collider = d.add_collider(
    space.static_body,
    'segment',
    (GROUND_THICKNESS/2,),
    (0, GROUND_LEVEL),
    (window.width, GROUND_LEVEL)
)
ground = GameObject(
    shape=ground_shape,
    collider=ground_collider
)


wall_shape, wall_body = d.draw_wall(
    (get_coordinate(10, None)[0], GROUND_LEVEL),
    SLIDER_SIZE,
    SLIDER_SIZE*3
)
wall_collider = d.add_collider(
    wall_body,
    'poly',
    (SLIDER_SIZE, SLIDER_SIZE*3)
)
wall = GameObject(
    shape=wall_shape,
    body=wall_body,
    collider=wall_collider
)

#------------------------ game loop func ----------------------------------

DT = 1 / 120
_accum = 0

wall_direction = 'right'

def update(frame_dt):
    global _accum
    global wall_direction
    _accum += min(frame_dt, 0.25)
    while _accum >= DT:
        space.step(DT)
        _accum -= DT
    slider.sync_shape()
    if wall_direction == 'right':
        wall.move_right()
    if wall_direction == 'left':
        wall.move_left()
    if wall.body.position and wall.body.position.x > window.width:
        wall_direction = 'left'
    elif wall.body.position and wall.body.position.x < 0:
        wall_direction = 'right'
    wall.sync_shape()


@window.event
def on_draw():
    window.clear()
    label.draw()
    batch.draw()


@window.event
def on_key_press(symbol, modifier):
    if symbol == pyglet.window.key.SPACE:
        jump(slider.body)


pyglet.clock.schedule_interval(update, 1 / 60)
pyglet.app.run()
    
