# Импортируем pygame и запускаем игровой "движок" командой pygame.init()
import pygame
# Импортируем функцию choice, это понадобится для закраски кирпичей случайным цветом
from random import choice
# Импортируем класс "Ракетка"
from paddle import Paddle
# Импортируем класс "Мяч"
from ball import Ball
# Импортируем класс "Кирпич"
from brick import Brick


pygame.init()

# В этом блоке кода мы подключаем музыку
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
# Чтобы подключить музыкальный файл, нужно правильно указать его назание в скобках
pygame.mixer.music.load('sound.mp3')
# настраиваем громкость: от 1 до 0
pygame.mixer.music.set_volume(0.1)
# эта строчка нужна, чтобы зациклить воспроизведение одного трека
pygame.mixer.music.play(-1)

# Определим несколько цветов, которые мы будем использовать в игре
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
DARKBLUE = (0, 70, 180)
LIGHTBLUE = (0, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 0)

score = 0
helth_points = 3

# ==========    Создаём окно, в котором будет находиться игра: ==========
# Указываем размеры окна
size = (800, 600)
# Cоздаём окно и указываем, что в дальнейшем будет обращаться к нему по имени screen
screen = pygame.display.set_mode(size)
# Указываем название окна
pygame.display.set_caption("Breakout")
# Вставляем картинку из файла "fon.png" как фон
background = pygame.image.load("fon.png")


# Подготовим специальный список для хранения спрайтов
all_sprites = pygame.sprite.Group()

# ==========    Создаём спрайт "Ракетка": ==========
paddle = Paddle(LIGHTBLUE, 120, 10)
# Команды rect.x и rect.y устанавливают позицию спрайта "Ракетка" в окне игры
paddle.rect.x = 350
paddle.rect.y = 570

# ==========    Создаём спрайт "Мяч":    ==========
ball = Ball(BLACK, 20, 20)
ball.rect.x = 300
ball.rect.y = 200

# ==========    Создаём ряды кирпичей разных цветов:    ==========
# Создалим отдельный список только для хранения спрайтов кирпичей
bricks_lst = pygame.sprite.Group()
# В цикле создадим разноцветные прямоугольники
for line in range(4):
    y_position = 50 + line*25
    for i in range(10):
        brick = Brick(choice([RED, ORANGE, YELLOW, WHITE]), 70, 16)
        brick.rect.x = 10 + i*79
        brick.rect.y = y_position
        # добавляем кирпич в список спрайтов
        all_sprites.add(brick)
        bricks_lst.add(brick)

# Добавляем Ракетку и Мяч в список спрайтов
all_sprites.add([paddle])
all_sprites.add([ball])

keepOn = True
clock = pygame.time.Clock()


# ======================================================================
# ====================  Основной цикл программы:    ====================
# ======================================================================
while keepOn:
    # Основной цикл, "перебирающий" события
    for event in pygame.event.get(): # Игрок что-то сделал
        if event.type == pygame.QUIT: # Если игрок закрыл окно
            keepOn = False
        # Добавим возможность закрыть игру нажатием на кнопку "Q"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                keepOn = False

    # Функция get_pressed() даёт нам возможность отследить, 
    # какие кнопки клавиатуры нажаты в текущий момент
    keys = pygame.key.get_pressed()
    # Проверка нажатия клавиш "ЛЕВО" и "ПРАВО" (кнопки со стрелками), 
    # для контроля движения ракетки
    if keys[pygame.K_LEFT]:
        paddle.moveLeft(10)
    if keys[pygame.K_RIGHT]:
        paddle.moveRight(10)

# ====================  Описание игровой логики:    ====================
    all_sprites.update()

    # Делаем проверку, врезался ли мяч в стену. Если да, то изменяем скорость на обратную
    if ball.rect.x >= 780 or ball.rect.x <= 0:
        ball.velocity[0] = -ball.velocity[0]

    # Проверим удар о верхнюю линию
    if ball.rect.y <= 38:
        ball.velocity[1] = -ball.velocity[1]
    # Если мяч коснулся дна, миновав ракетку, отнимется жизнь
    elif ball.rect.y > 600:
        ball.velocity[1] = -ball.velocity[1]
        helth_points -= 1
        if helth_points == 0:
            # Отображаем экран конца игры, так как закончились жизни
            font = pygame.font.Font(None, 100)
            text = font.render("BUSTED", 1, WHITE)
            screen.blit(text, (280,300))
            pygame.display.flip()
            pygame.time.wait(5000)

            # Останавливаем игру
            keepOn = False

    # Здесь будем отслеживать наезд мяча на ракетку
    if pygame.sprite.collide_mask(ball, paddle):
      ball.rect.x -= ball.velocity[0]
      ball.rect.y -= ball.velocity[1]
      ball.bounce()
 
    # Проверяем наезд мячика на кирпичи
    brick_collision_list = pygame.sprite.spritecollide(ball,bricks_lst,False)
    for brick in brick_collision_list:
      ball.bounce()
      score += 1
      brick.kill()
      # Если в списке, хранящем спрайты кирпичей ничего не осталось, то выводим "экран победы"
      if len(bricks_lst) == 0:
           # Показываем сообщение "LEVEL COMPLETE" в течение 10 секунд
            font = pygame.font.Font(None, 100)
            text = font.render("YOU WIN!!!", 1, WHITE)
            screen.blit(text, (240,300))
            pygame.display.flip()
            pygame.time.wait(5000)
 
            # Останавливаем игру
            keepOn = False

# ====================  Код отрисовки:  ====================
    # Во-первых, отрисуем фон
    screen.blit(background, (0, 0))
    # Нарисуем линию, отделяющую показатели игры от части экрана, где будут происходить действия
    pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 4)

    # Отображаем счёт и количество жизней сверху на экране
    font = pygame.font.Font(None, 34)
    text = font.render("Счёт: " + str(score), 1, WHITE)
    screen.blit(text, (20,10))
    text = font.render("HP: " + str(helth_points), 1, WHITE)
    screen.blit(text, (650, 10))

    # Теперь рисуем все спрайты за один шаг
    all_sprites.draw(screen)
    # Продолжаем обновлять экран, с учётом изменений
    pygame.display.flip()
    # Устанавливаем таймер на 60 кадоров в секунду
    clock.tick(60)
# ======================================================================
# ==================    Конец сновного цикла программы.    =============
# ======================================================================



# ====================  Остановка музыки и движка игры:  ====================
# Выключаем музыку функцией stop()
pygame.mixer.music.stop()
# Когда мы вышли из основного цикла программы, останавливаем движок игры
pygame.quit()