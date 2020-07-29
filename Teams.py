from random import randint

from Ball import Ball
from Field import Field
from Goalkeeper import Goalkeeper
from Player import Player
from Util import Vector


class Teams:
    LINEUP = [Vector(2 * Field.WIDTH / 5, 1 * Field.HEIGHT/5),
              Vector(2 * Field.WIDTH / 5, 2 * Field.HEIGHT/5),
              Vector(2 * Field.WIDTH / 5, 3 * Field.HEIGHT/5),
              Vector(2 * Field.WIDTH / 5, 4 * Field.HEIGHT/5),
              Vector(3 * Field.WIDTH / 5, 1 * Field.HEIGHT / 5),
              Vector(3 * Field.WIDTH / 5, 2 * Field.HEIGHT / 5),
              Vector(3 * Field.WIDTH / 5, 3 * Field.HEIGHT / 5),
              Vector(3 * Field.WIDTH / 5, 4 * Field.HEIGHT / 5),
              Vector(4 * Field.WIDTH / 5, 2 * Field.HEIGHT / 5),
              Vector(4 * Field.WIDTH / 5, 3 * Field.HEIGHT / 5)]

    AREA = Vector(Field.WIDTH / 4, Field.HEIGHT / 4)

    PLAYERS_NUMBER = 10

    def __init__(self, canvas, field: Field, ball: Ball):
        self.canvas = canvas
        self.field = field
        self.ball = ball
        self.goalkeeper1 = Goalkeeper(self.canvas, 1)
        self.goalkeeper2 = Goalkeeper(self.canvas, 2)
        self.players1 = []
        self.players2 = []
        self.ball_possession = 1
        self.ball_player = -1
        self.pass_to_player = -1
        self.init_players()

    def init_players(self):
        for i in range(Teams.PLAYERS_NUMBER):
            self.players1.append(Player(self.canvas, 1))
            self.players2.append(Player(self.canvas, 2))

    def set_start_positions(self):
        self.goalkeeper1.set_on_center(self.field)
        self.goalkeeper2.set_on_center(self.field)
        for i in range(Teams.PLAYERS_NUMBER):
            pos = Teams.LINEUP[i].mul(Vector(0.5, 1))
            self.players1[i].set(self.field.start_xy.add(pos))
            self.players2[i].set(self.field.end_xy.sub(pos))

    def pass_ball_to_goalkeeper(self):
        self.goalkeeper1.miss_ball = False
        self.goalkeeper2.miss_ball = False
        if self.ball_possession == 1:
            self.goalkeeper1.get_ball(self.ball, self.ball_possession)
        elif self.ball_possession == 2:
            self.goalkeeper2.get_ball(self.ball, self.ball_possession)

    def ball_hit_test(self):
        if self.goalkeeper1.ball_hit_test(self.ball):
            self.ball_possession = 1
        if self.goalkeeper2.ball_hit_test(self.ball):
            self.ball_possession = 2

    def ball_player_take(self):
        for i in range(Teams.PLAYERS_NUMBER):
            if self.players1[i].ball_hit_test(self.ball):
                self.ball.stop()
                self.ball_possession = 1
                self.ball_player = i
                self.pass_to_player = -1
                self.make_decision()
                return
        for i in range(Teams.PLAYERS_NUMBER):
            if self.players2[i].ball_hit_test(self.ball):
                self.ball.stop()
                self.ball_possession = 2
                self.ball_player = i
                self.pass_to_player = -1
                self.make_decision()
                return

    def move_players(self):
        self.goalkeeper1.move_to_ball_y(self.ball, self.field)
        self.goalkeeper2.move_to_ball_y(self.ball, self.field)
        ball_v = self.ball.pos.sub(self.field.center).norm()
        for i in range(Teams.PLAYERS_NUMBER):
            if self.ball_possession == 1 and self.pass_to_player == i: continue
            ideal = self.field.start_xy.add(Teams.LINEUP[i]).add(Teams.AREA.mul(ball_v))
            self.players1[i].move_to_point(ideal)
        ball_v = self.field.center.sub(self.ball.pos).norm()
        for i in range(Teams.PLAYERS_NUMBER):
            if self.ball_possession == 2 and self.pass_to_player == i: continue
            lineup = Teams.LINEUP[i]
            area = Teams.AREA.invert(True, False)
            ideal = self.field.end_xy.sub(lineup).add(area.mul(ball_v))
            self.players2[i].move_to_point(ideal)

    def pass_ball(self, to_player: int):
        if self.ball_possession == 1:
            self.ball.direct_to_point(self.players1[to_player].pos)
            self.ball_player = -1
            self.pass_to_player = to_player
        else:
            self.ball.direct_to_point(self.players2[to_player].pos)
            self.ball_player = -1
            self.pass_to_player = to_player

    def shoot_ball(self):
        self.ball_player = -1
        self.pass_to_player = -1
        self.ball.shoot(3-self.ball_possession)

    def make_decision(self):
        if self.ball.dist2_to_goal(3-self.ball_possession) <= (Field.BOX * 2) * (Field.BOX * 2):
            self.shoot_ball()
        else:
            to_player = (self.ball_player + 1) % Teams.PLAYERS_NUMBER
            self.pass_ball(to_player)