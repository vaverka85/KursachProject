# KursachProject

Есть игровое поле — простой прямоугольник с твёрдыми границами. Когда шарик касается стенки или потолка, 
он отскакивает в другую сторону. Если он упадёт на пол — игра окончена. Внизу вдоль пола двигается платформа, 
управление - с помощью стрелок. Задача — подставлять платформу под шарик как можно дольше. 
За каждое удачное спасение шарика начисляется одно очко.

Для реализацуии задуманного, необходимо реализовать следующие сценарии поведения:

-игра начинается;
-шарик начинает двигаться;
-если нажаты стрелки влево или вправо — двигаем платформу;
-если шарик коснулся стенок, потолка или платформы — делаем отскок;
-если шарик коснулся платформы — увеличиваем счёт на единицу;
-если шарик упал на пол — выводим сообщение и заканчиваем игру.

Всё это происходит параллельно и независимо друг от друга. 
Нужно определить три класса — платформу, сам шарик и счёт, и определить, как они реагируют на действия друг друга. 


# подключаем графическую библиотеку
from tkinter import *
# подключаем модули, которые отвечают за время и случайные числа
import time
import random
# создаём новый объект — окно с игровым полем. 
tk = Tk()
# делаем заголовок окна — Funny Ball с помощью свойства объекта title
tk.title('Funny ball')
# запрещаем менять размеры окна, для этого используем свойство resizable
tk.resizable(0, 0)
# помещаем наше игровое окно выше остальных окон на компьютере, чтобы другие окна не могли его заслонить.
tk.wm_attributes('-topmost', 1)

# создаём новый холст — 500 на 600 пикселей
HEIGHT = 500
WIDTH = 600
canvas = Canvas(tk, width=WIDTH, height=HEIGHT, highlightthickness=0)

#задаем определеннный фон на основе ранее найденного изображения:
game_image = PhotoImage(file = 'D:\KursachProject\Ir4.gif')
canvas.create_image(0, 0, anchor = NW, image = game_image)


# говорим холсту, что у каждого видимого элемента будут свои отдельные координаты
canvas.pack()


# обновляем окно с холстом
tk.update()

# Описываем класс Ball, который будет отвечать за шарик
class Ball:
    
    # конструктор для создания нового объекта на основе этого класса
    def __int__(self, ball):
        self.ball = ball
   
   
   def __init__(self, canvas, paddle, score, color, color_1):
       
       # задаём параметры объекта, которые нам передают в скобках в момент создания
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        
        # командой create_oval мы создаём круг радиусом 30 пикселей и закрашиваем нужным цветом
        self.id = canvas.create_oval(10,10, 30, 30, fill=color, outline = color_1)
       
       # помещаем шарик в точку с координатами 245,100
        self.canvas.move(self.id, 245, 100)
        
        # задаём список возможных направлений для старта
        starts = [-2, -1, 1, 2]
       
       # перемешиваем его
        random.shuffle(starts)
       
       # выбираем первый из перемешанного — это будет вектор движения шарика
        self.x = starts[0]
       
       # уменьшаем значение по оси y,т.к. в самом начале шарик всегда падает вниз
        self.y = -2
       
       # задаем шарику высоту и ширину
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
       
       # свойство, которое отвечает за то, достиг шарик дна или нет. Пока не достиг, значение будет False
        self.hit_bottom = False

    # обрабатываем касание платформы, для этого получаем 4 координаты шарика в переменной pos (левая верхняя и правая нижняя точки)
    def hit_paddle(self, pos):
        # получаем кординаты платформы через объект paddle (платформа)
        paddle_pos = self.canvas.coords(self.paddle.id)
        
        # если координаты касания совпадают с координатами платформы
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                # увеличиваем счёт 
                self.score.hit()
                # возвращаем метку о том, что мы успешно коснулись
                return True
        # возвращаем False — касания не было
        return False


    # метод, который отвечает за движение шарика
    def draw(self):
        # передвигаем шарик на заданный вектор x и y
        self.canvas.move(self.id, self.x, self.y)
        # запоминаем новые координаты шарика
        pos = self.canvas.coords(self.id)
        # если шарик падает сверху
        if pos[1] <= 0:
            # задаём падение на следующем шаге = 2
            self.y = 2
        # если шарик правым нижним углом коснулся дна
        if pos[3] >= self.canvas_height:
            # помечаем это в отдельной переменной
            self.hit_bottom = True
            # выводим сообщение и количество очков
            canvas.create_text(300, 120, text='Вы проиграли!', font=('Courier', 30), fill='red')
        # если было касание платформы
        if self.hit_paddle(pos) == True:
            # отправляем шарик наверх
            self.y = -2
        # если коснулись левой стенки
        if pos[0] <= 0:
            # движемся вправо
            self.x = 2
        # если коснулись правой стенки
        if pos[2] >= self.canvas_width:
            # движемся влево
            self.x = -2


#  Описываем класс Paddle, который отвечает за платформы
class Paddle:
    
    # конструктор
    def __init__(self, canvas, color, color_1):
      
      # canvas означает, что платформа будет нарисована на нашем изначальном холсте
        self.canvas = canvas
       
       # создаём прямоугольную платформу 20 на 120 пикселей, закрашиваем выбранным цветом и получаем её внутреннее имя
        self.id = canvas.create_rectangle(0, 0, 120, 20, fill=color, outline = color_1)
       
       # задаём список возможных стартовых положений платформы
        start_1 = [40, 60, 90, 120, 150, 180, 200]
      
      # перемешиваем их
        random.shuffle(start_1)
        
        # выбираем первое из перемешанных
        self.starting_point_x = start_1[0]
       
       # перемещаем платформу в стартовое положение
        self.canvas.move(self.id, self.starting_point_x, 470)
        
        # пока платформа никуда не движется, поэтому изменений по оси х нет
        self.x = 0
       
       # платформа узнаёт свою ширину
        self.canvas_width = self.canvas.winfo_width()
       
       # задаём обработчик нажатий
        # если нажата стрелка вправо — выполняется метод turn_right()
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        
        # если стрелка влево — turn_left()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
       
       # пока платформа не двигается, поэтому ждём
        self.started = False
       
       # как только игрок нажмёт Enter — всё стартует
        self.canvas.bind_all('<KeyPress-Return>', self.start_game)
   
 # движемся вправо
    def turn_right(self, event):
        # будем смещаться правее на 2 пикселя по оси х
        self.x = 2
   
 # движемся влево
    def turn_left(self, event):
        # будем смещаться левее на 2 пикселя по оси х
        self.x = -2
   
 # игра начинается
    def start_game(self, event):
        # меняем значение переменной, которая отвечает за старт движения платформы
        self.started = True
   
 # метод, который отвечает за движение платформы
    def draw(self):
        # сдвигаем нашу платформу на заданное количество пикселей
        self.canvas.move(self.id, self.x, 0)
        # получаем координаты холста
        pos = self.canvas.coords(self.id)
        # если мы упёрлись в левую границу
        if pos[0] <= 0:
            # останавливаемся
            self.x = 0
        # если упёрлись в правую границу
        elif pos[2] >= self.canvas_width:
            # останавливаемся
            self.x = 0


#  Описываем класс Score, который отвечает за отображение счетов
class Score:
  
  # конструктор
    def __init__(self, canvas, color):
       
       # в самом начале счёт равен нулю
        self.score = 0
        # будем использовать наш холст
        self.canvas = canvas
       
       # создаём надпись, которая показывает текущий счёт, делаем его нужно цвета и запоминаем внутреннее имя этой надписи
        self.id = canvas.create_text(450, 10, text = 'Счёт: {}'.format(self.score), font=('Courier', 15), fill=color, tag="score")
   
   # обрабатываем касание платформы
    def hit(self):
        # увеличиваем счёт на единицу
        self.score += 1
        # пишем новое значение счёта
        self.canvas.itemconfig(self.id, text='Счёт: {}'.format(self.score))


# создаём объект — белый счёт
score = Score(canvas, 'white')
# создаём объект — синюю платформу
paddle = Paddle(canvas, 'Blue', 'white')
# создаём объект — фиолетовый шарик
ball = Ball(canvas, paddle, score, 'purple','white')

# пока шарик не коснулся дна
while not ball.hit_bottom:
    # если игра началась и платформа может двигаться
    if paddle.started == True:
        # двигаем шарик
        ball.draw()
        # двигаем платформу
        paddle.draw()
   
   # обновляем наше игровое поле, чтобы всё, что нужно, закончило рисоваться
    tk.update_idletasks()
  
  # обновляем игровое поле и смотрим за тем, чтобы всё, что должно было быть сделано — было сделано
    tk.update()
   
   # замираем на одну сотую секунды, чтобы движение элементов выглядело плавно
    time.sleep(0.01)
# если программа дошла досюда, значит, шарик коснулся дна. Ждём 3 секунды, пока игрок прочитает финальную надпись, и завершаем игру
time.sleep(3)
