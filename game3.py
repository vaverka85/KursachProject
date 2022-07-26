
from tkinter import *

import time
import random

tk = Tk()

tk.title('Funny ball')

tk.resizable(0, 0)

tk.wm_attributes('-topmost', 1)

HEIGHT = 500
WIDTH = 600
canvas = Canvas(tk, width=WIDTH, height=HEIGHT, highlightthickness=0)
game_image = PhotoImage(file = 'D:\KursachProject\Ir4.gif')
canvas.create_image(0, 0, anchor = NW, image = game_image)

canvas.pack()

tk.update()


class Ball:

    def __int__(self, ball):
        self.ball = ball
    def __init__(self, canvas, paddle, score, color, color_1):
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.id = canvas.create_oval(10,10, 30, 30, fill=color, outline = color_1)
        self.canvas.move(self.id, 245, 100)
        starts = [-2, -1, 1, 2]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -2
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False


    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                self.score.hit()
                return True
        return False


    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 2
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
            canvas.create_text(300, 120, text='Вы проиграли!', font=('Courier', 30), fill='red')
        if self.hit_paddle(pos) == True:
            self.y = -2
        if pos[0] <= 0:
            self.x = 2
        if pos[2] >= self.canvas_width:
            self.x = -2


class Paddle:
    def __init__(self, canvas, color, color_1):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 120, 20, fill=color, outline = color_1)
        start_1 = [40, 60, 90, 120, 150, 180, 200]
        random.shuffle(start_1)
        self.starting_point_x = start_1[0]
        self.canvas.move(self.id, self.starting_point_x, 470)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.started = False
        self.canvas.bind_all('<KeyPress-Return>', self.start_game)


    def turn_right(self, event):
        self.x = 2


    def turn_left(self, event):
        self.x = -2


    def start_game(self, event):
        self.started = True


    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0


class Score:
    def __init__(self, canvas, color):
        self.score = 0
        self.canvas = canvas
        self.id = canvas.create_text(450, 10, text = 'Счёт: {}'.format(self.score), font=('Courier', 15), fill=color, tag="score")


    def hit(self):
        self.score += 1
        self.canvas.itemconfig(self.id, text='Счёт: {}'.format(self.score))


score = Score(canvas, 'white')
paddle = Paddle(canvas, 'Blue', 'white')
ball = Ball(canvas, paddle, score, 'purple','white')
while not ball.hit_bottom:
    if paddle.started == True:
        ball.draw()
        paddle.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
time.sleep(3)

