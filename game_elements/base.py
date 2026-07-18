
import pyglet, pymunk
import conf


class GameObject:

    def __init__(
            self,
            window:pyglet.window.BaseWindow,
            shape:pyglet.shapes.ShapeBase|None=None,
            body:pymunk.Body|None=None,
            collider:pymunk.Shape|None=None,
            label:pyglet.text.DocumentLabel|None=None,
            space:pymunk.Space|None=None,
    ):
        self.window = window
        self.shape = shape
        self.body = body
        self.collider = collider
        self.space = space
        self.label = label
    
    def update_pos(self, horizontal_percentage:float, verticle_percentage:float):
        from utils import get_coordinate
        pos = get_coordinate(self.window, horizontal_percentage, verticle_percentage)
        if self.shape:
            self.shape.position = pos
        if self.body:
            self.body.position = pos
        if self.collider:
            self.collider.position = pos

    def move_left(self, multiplier:float=1.0):
        if self.body:
            self.body.velocity = (-conf.GROUND_VELOCITY*multiplier, self.body.velocity.y)

    def move_right(self, multiplier:float=1.0):
        if self.body:
            self.body.velocity = (conf.GROUND_VELOCITY*multiplier, self.body.velocity.y)
    
    def sync_shape(self):
        if self.shape and self.body:
            self.shape.position = self.body.position

    def rebuild_collider(self):
        if self.space and self.collider:
            self.space.remove(self.collider)
            if isinstance(self.shape, pyglet.shapes.Line):
                #add segment collider
                ...
            else:
                collider = pymunk.Poly.create_box(
                    self.body,
                    (self.shape.width, self.shape.height)
                )
                collider.friction = self.collider.friction
                self.collider = collider
                self.space.add(self.collider)



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
            anchor_y='center',
            batch=self.batch
            )
        return t

    def draw_ground(self)->pyglet.shapes.ShapeBase:
        ground_shape = pyglet.shapes.Line(
            0, conf.GROUND_LEVEL,
            self.window.width, conf.GROUND_LEVEL,
            thickness = conf.GROUND_THICKNESS,
            color=conf.GROUND_COLOR,
            batch=self.batch
        )
        return ground_shape

    def draw_slider(self)->tuple:
        from utils import get_coordinate
        slider_shape = pyglet.shapes.Rectangle(
            get_coordinate(self.window, 50, None)[0],
            get_coordinate(self.window, None, 50)[1],
            width=conf.SLIDER_SIZE,
            height=conf.SLIDER_SIZE,
            color=conf.SLIDER_COLOR,
            batch=self.batch
        )
        slider_shape.anchor_position = (conf.SLIDER_SIZE/2, conf.SLIDER_SIZE/2)
        slider_body = pymunk.Body(
            mass=1,
            moment=float('inf'),
        )
        slider_body.position = get_coordinate(self.window, 50, 50)
        self.space.add(slider_body)
        return slider_shape, slider_body


    def draw_wall(self, pos:tuple, width:float, height:float):
        wall_shape = pyglet.shapes.Rectangle(
            pos[0],
            pos[1],
            width=width,
            height=height,
            color=conf.WALL_COLOR,
            batch=self.batch
        )
        wall_shape.anchor_position = (width/2, height/2)
        wall_body = pymunk.Body(
            mass=100,
            moment=float('inf'),
        )
        wall_body.position = pos
        self.space.add(wall_body)
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


class GameWorld:

    @classmethod
    def get_obj(cls, name:str) -> GameObject|None:
        return getattr(cls, name, None)

    @classmethod
    def add_obj(cls, name:str, obj:GameObject):
        setattr(cls, name, obj)
