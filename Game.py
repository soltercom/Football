from time import sleep
from tkinter import Canvas, Tk

from Ball import Ball

from Field import Field
from Scoreboard import Scoreboard
from Teams import Teams


class Game:
    BEGIN, START, GAME, GOAL1, GOAL2, OUT1, OUT2, END = range(8)

    DELAY = 0.04

    def __init__(self):
        self.window = Tk()
        self.window.title('Football')
        self.canvas = Canvas(self.window, width=2*Field.X0+Field.WIDTH, height=2*Field.Y0+Field.HEIGHT)
        self.canvas.pack()
        self.field = Field(self.canvas)
        self.ball = Ball(self.canvas, self.field)
        self.scoreboard = Scoreboard(self.canvas, self.field)
        self.teams = Teams(self.canvas, self.field, self.ball)
        self.state = Game.BEGIN

    def mainloop(self):
        while True:
            if self.state == Game.BEGIN:
                self.begin()
            elif self.state == Game.START:
                self.start()
            elif self.state == Game.GAME:
                self.game()
            elif self.state == Game.GOAL1:
                self.goal1()
            elif self.state == Game.GOAL2:
                self.goal2()
            elif self.state == Game.OUT1:
                self.out1()
            elif self.state == Game.OUT2:
                self.out2()
            elif self.state == Game.END:
                self.end()

    def begin(self):
        self.field.paint()
        self.scoreboard.update_timer()
        self.state = Game.START

    def start(self):
        self.scoreboard.update_score()
        self.teams.pass_ball_to_goalkeeper()
        self.ball.set_rand_speed(self.teams.ball_possession)
        self.teams.set_start_positions()
        self.teams.pass_ball(0)
        self.state = Game.GAME

    def game(self):
        while self.state == Game.GAME:
            self.ball.move()
            self.teams.move_players()
            self.window.update()
            sleep(Game.DELAY)
            self.teams.ball_player_take()
            if self.ball.is_goal1():
                self.state = Game.GOAL1
            elif self.ball.is_goal2():
                self.state = Game.GOAL2
            elif self.ball.is_out1():
                self.state = Game.OUT1
            elif self.ball.is_out2():
                self.state = Game.OUT2
            else:
                self.ball.field_hit_test()
            self.teams.ball_hit_test()
            if self.scoreboard.add_sec():
                self.state = Game.END

    def goal1(self):
        self.teams.ball_possession = 1
        self.scoreboard.add_score2()
        self.ball.set_in_goal1()
        self.field.show_goal1(self.window)
        self.state = Game.START

    def goal2(self):
        self.teams.ball_possession = 2
        self.scoreboard.add_score1()
        self.ball.set_in_goal2()
        self.field.show_goal2(self.window)
        self.state = Game.START

    def out1(self):
        self.teams.ball_possession = 1
        self.teams.pass_ball_to_goalkeeper()
        self.window.update()
        sleep(4*Game.DELAY)
        self.teams.pass_ball(0)
        #self.ball.set_speed(self.teams.ball_possession)
        self.state = Game.GAME

    def out2(self):
        self.teams.ball_possession = 2
        self.teams.pass_ball_to_goalkeeper()
        self.window.update()
        sleep(4*Game.DELAY)
        self.teams.pass_ball(0)
        #self.ball.set_speed(self.teams.ball_possession)
        self.state = Game.GAME

    def end(self):
        self.ball.set_on_center()
        self.teams.set_start_positions()
        self.scoreboard.final_score(self.field)
        self.window.update()
