from time import sleep

from Util import Vector, Rectangle


class Field:
    X0 = 100
    Y0 = 50
    WIDTH = 1200
    HEIGHT = 750
    BOX = 200
    COLOR = "#80e27e"
    LINE_COLOR = "#ffffff"
    GOAL_COLOR = "#62757f"
    GOAL_COLOR2 = "#ba000d"

    @property
    def goal1(self):
        return Vector(self.start_x, self.center_y)

    @property
    def goal2(self):
        return Vector(self.end_x, self.center_y)

    @property
    def center(self):
        return Vector(self.center_x, self.center_y)

    @property
    def start_xy(self):
        return Vector(self.start_x, self.start_y)

    @property
    def end_xy(self):
        return Vector(self.end_x, self.end_y)

    @property
    def goal1_rectangle(self):
        return Rectangle(self.start_x - Field.BOX / 3, self.goal_start_y, self.start_x, self.goal_end_y)

    @property
    def goal2_rectangle(self):
        return Rectangle(self.end_x, self.goal_start_y, self.end_x + Field.BOX / 3, self.goal_end_y)

    @property
    def center_x(self):
        return Field.X0 + int(Field.WIDTH / 2)

    @property
    def center_y(self):
        return Field.Y0 + int(Field.HEIGHT / 2)

    @property
    def start_x(self):
        return Field.X0

    @property
    def end_x(self) -> float:
        return Field.X0 + Field.WIDTH

    @property
    def start_y(self):
        return Field.Y0

    @property
    def end_y(self):
        return Field.Y0 + Field.HEIGHT

    @property
    def goal_start_y(self):
        return Field.Y0 + Field.HEIGHT / 2 - Field.BOX / 2

    @property
    def goal_end_y(self):
        return Field.Y0 + Field.HEIGHT / 2 + Field.BOX / 2

    def __init__(self, canvas):
        self.canvas = canvas
        self.shape_goal1 = None
        self.shape_goal2 = None

    def paint_goal1(self, mode=1):
        if mode == 1:
            color = Field.GOAL_COLOR
        else:
            color = Field.GOAL_COLOR2
        self.shape_goal1 = self.canvas.create_rectangle(self.start_x - Field.BOX / 3, self.goal_start_y,
                                                        self.start_x, self.goal_end_y,
                                                        fill=color, outline=Field.LINE_COLOR, width=3)

    def paint_goal2(self, mode=1):
        if mode == 1:
            color = Field.GOAL_COLOR
        else:
            color = Field.GOAL_COLOR2
        self.shape_goal2 = self.canvas.create_rectangle(self.end_x, self.goal_start_y,
                                                        self.end_x + Field.BOX / 3, self.goal_end_y,
                                                        fill=color, outline=Field.LINE_COLOR, width=3)

    def paint(self):
        self.canvas.create_rectangle(self.start_x, self.start_y,
                                     self.end_x, self.end_y,
                                     fill=Field.COLOR, outline=Field.LINE_COLOR, width=3)
        self.canvas.create_line(self.center_x, self.start_y,
                                self.center_x, self.end_y,
                                width=3, fill=Field.LINE_COLOR)
        self.canvas.create_oval(self.center_x - Field.BOX / 2, self.center_y - Field.BOX / 2,
                                self.center_x + Field.BOX / 2, self.center_y + Field.BOX / 2,
                                outline=Field.LINE_COLOR, width=3)
        self.canvas.create_line(self.start_x, self.center_y - Field.BOX,
                                self.start_x + Field.BOX, self.center_y - Field.BOX,
                                width=3, fill=Field.LINE_COLOR)
        self.canvas.create_line(self.start_x, self.center_y + Field.BOX,
                                self.start_x + Field.BOX, self.center_y + Field.BOX,
                                width=3, fill=Field.LINE_COLOR)
        self.canvas.create_line(self.start_x + Field.BOX, self.center_y - Field.BOX,
                                self.start_x + Field.BOX, self.center_y + Field.BOX,
                                width=3, fill=Field.LINE_COLOR)
        self.canvas.create_line(self.end_x, self.center_y - Field.BOX,
                                self.end_x - Field.BOX, self.center_y - Field.BOX,
                                width=3, fill=Field.LINE_COLOR)
        self.canvas.create_line(self.end_x, self.center_y + Field.BOX,
                                self.end_x - Field.BOX, self.center_y + Field.BOX,
                                width=3, fill=Field.LINE_COLOR)
        self.canvas.create_line(self.end_x - Field.BOX, self.center_y - Field.BOX,
                                self.end_x - Field.BOX, self.center_y + Field.BOX,
                                width=3, fill=Field.LINE_COLOR)
        self.paint_goal1()
        self.paint_goal2()

    def show_goal1(self, window):
        for i in range(5):
            self.canvas.delete(self.shape_goal1)
            self.paint_goal1(0)
            window.update()
            sleep(0.2)
            self.canvas.delete(self.shape_goal1)
            self.paint_goal1()
            window.update()
            sleep(0.2)

    def show_goal2(self, window):
        for i in range(5):
            self.canvas.delete(self.shape_goal2)
            self.paint_goal2(0)
            window.update()
            sleep(0.2)
            self.canvas.delete(self.shape_goal2)
            self.paint_goal2()
            window.update()
            sleep(0.2)

