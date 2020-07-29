from Field import Field


class Scoreboard:

    DURATION = 90
    TIMER_COLOR = "#62757f"
    SCORE_COLOR = "#004c40"

    def __init__(self, canvas, field: Field):
        self.canvas = canvas
        self.field = field
        self.score1 = 0
        self.score2 = 0
        self.timer_min = Scoreboard.DURATION
        self.timer_sec = 0
        self.score_shape = None
        self.timer_shape = None

    def add_score1(self):
        self.score1 += 1
        self.update_score()

    def add_score2(self):
        self.score2 += 1
        self.update_score()

    def add_sec(self) -> bool:
        self.timer_sec -= 1
        if self.timer_sec == -1:
            self.timer_min -= 1
            self.timer_sec = 59
        self.update_timer()
        if self.timer_min == 0 and self.timer_sec == 0:
            return True
        else:
            return False

    def update_score(self):
        if self.score_shape is not None:
            self.canvas.delete(self.score_shape)
        x = (self.field.start_x + self.field.end_x) / 2
        y = self.field.start_y / 2
        self.score_shape = self.canvas.create_text(x, y, font="Verdana 40 bold", fill=Scoreboard.SCORE_COLOR,
                                                   text=str(self.score1) + ":" + str(self.score2))

    def final_score(self, field: Field):
        if self.score_shape is not None:
            self.canvas.delete(self.score_shape)
        self.score_shape = self.canvas.create_text(field.center_x, field.center_y, font="Verdana 80 bold", fill=Scoreboard.TIMER_COLOR,
                                                   text=str(self.score1) + ":" + str(self.score2))

    def update_timer(self):
        if self.score_shape is not None:
            self.canvas.delete(self.timer_shape)
        x = self.field.end_x - 80
        y = self.field.start_y / 2
        self.timer_shape = self.canvas.create_text(x, y, font="Verdana 40 bold", fill=Scoreboard.TIMER_COLOR,
                              text='{:02d}'.format(self.timer_min) + ":" + '{:02d}'.format(self.timer_sec))
