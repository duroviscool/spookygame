import pygame as pg
import random
import math

pg.init()

font_name = pg.font.match_font('Arial') #поиск шрифта
size = 18 #его размер

w = 1200
h = 800
win = pg.display.set_mode((w,h))

bg = pg.image.load("replace.png") #загрузка (добавление) картинки
bg = pg.transform.scale(bg, (w,h)) #изменение картинки на полный экран

pg.display.set_caption("потом название придумаю") # название программы (игры)

stbg = pg.image.load('darkbg.jpg') # фон игры, потом нарисую
stbg = pg.transform.scale(stbg, (w,h))

x = w//2
y = h//2

score = 0 # очки
max_health = 5 # макс. здоровье
health = 5 # текущее здоровье

class Player(pg.sprite.Sprite): # создание игрока
  def __init__(self, plr_x, plr_y):
    pg.sprite.Sprite.__init__(self)

    self.plr_x = plr_x
    self.plr_y = plr_y
    self.plr_turn = False # в какую сторону движется игрок, если false, то правая сторона, если true, то левая сторона
    self.jumping = False
    self.falling = False
    # скорость бега/прыжка
    self.speed_x = 1
    self.speed_y = 0
    # счет кардов для прыжка, падения
    self.jump_count = 0
    self.jump_max = 90
    self.jump_fall_count = 15

    # картинка игрока
    self.image = pg.image.load("player.png")
    self.image = pg.transform.scale(self.image, (64, 64))

    self.rect = self.image.get_rect()
    self.rect.centerx = self.plr_x
    self.rect.bottom = self.plr_y

    # данные об отраженной картинки игрока
    self.image_flip = pg.image.load("player.png")
    self.image_flip = pg.transform.scale(self.image_flip, (64, 64))
    self.image_flip = pg.transform.flip(self.image, True, False)

    # данные об неотраженной картинки игрока
    self.image_orig = pg.image.load("player.png")
    self.image_orig = pg.transform.scale(self.image_orig, (64, 64))
    self.image_orig = pg.transform.flip(self.image, False, False)
  def jump(self):

    # прыжок
    self.jumping = True
    for i in range(1,180):
      self.jumping = True
    self.jumping = False



  def update(self):
    self.rect.x += self.speed_x
    self.rect.y += self.speed_y

    if self.jumping == True:
      self.speed_y = 2
    else:
      self.speed_y = 0


    # проверка поворота
    if self.plr_turn:
      self.speed_x = -1
      self.image = self.image_flip
    else:
      self.speed_x = 1
      self.image = self.image_orig

    # поворот
    if self.rect.x >= (1080-64):
      self.plr_turn = True
    elif self.rect.x <= 120:
      self.plr_turn = False

class Sphere(pg.sprite.Sprite): # создание сферы
  def __init__(self, plr_pos_x, plr_pos_y):
    pg.sprite.Sprite.__init__(self)
    self.x = x
    self.y = y
    self.plr_pos_x = plr_pos_x
    self.plr_pos_y = plr_pos_y
    self.r = 5
    self.rad = 10
    self.speed = 3
    for i in range(1,3):
      self.image = pg.image.load("light_sphere.png")
      self.image = pg.transform.scale(self.image, (32,32))
      self.rect = self.image.get_rect()
      self.rect.centerx = self.x
      self.rect.bottom = self.y

  def update_pos(self):
    if self.r <= 360:  # здесь мы ставим ограничения, что-бы питон не выдал нам ошибку.
      self.angle = self.r * (3.14 / 180)  # перевод из градусов в радианы
      self.x = self.rad * math.cos(self.angle) + self.plr_pos_x
      self.y = self.rad * math.sin(self.angle) + self.plr_pos_y
      self.r += self.speed
    else:
      self.r = 0

class Enemy(pg.sprite.Sprite): # создание врага
  def __init__(self):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.image.load("ghost.png")
    self.image = pg.transform.scale(self.image, (64,64))
    self.speed_x = 1
    self.speed_y = 1
    self.plr_turn = False
    self.rect = self.image.get_rect()
    self.rect.x = random.randrange(60,1140) # ИЗНАЧАЛЬНАЯ позиция
    self.rect.y = random.randrange(60,740)
  def update(self):
    self.rect.x += self.speed_x
    self.rect.y += self.speed_y
    if self.plr_turn == True:
      self.speed_x = -1
    else:
      self.speed_x = 1
    if self.rect.x >= 1160:
      self.plr_turn = True
    elif self.rect.x <= 40:
      self.plr_turn = False
    if self.rect.y >= 740: #потом убрать
      self.speed_y = -1
    elif self.rect.y <= 40:
      self.speed_y = 1 #

class Walls(): # создание стен, пола, потолка (наверное потом будут картинки)
  def __init__(self):
    self.floor_rect = pg.draw.rect(win, (0, 0, 0), (0, 720, 1200, 800))
    self.wall_rect1 = pg.draw.rect(win, (0, 0, 0), (0, 0, 120, 800))
    self.wall_rect2 = pg.draw.rect(win, (0, 0, 0), (1080, 0, 1200, 800))
    self.ceil_rect = pg.draw.rect(win, (0, 0, 0), (0, 0, 1200, 80))

player = Player(w//2,720)
all_sprites = pg.sprite.Group()
all_sprites.add(player)

enemy = Enemy()
enemy_sprites = pg.sprite.Group()
enemy_sprites.add(enemy)

sphere = Sphere(plr_pos_x=player.plr_x, plr_pos_y=player.plr_y)
sphere_sprites = pg.sprite.Group()
sphere_sprites.add(sphere)

name = ''

def draw_text(surf, text, x, y, size=size, color=(255,255,255)):
  font = pg.font.Font(font_name, size) #определение шрифта
  text_surface = font.render(text, True, color)
  text_rect = text_surface.get_rect()
  text_rect.midtop = (x,y)
  surf.blit(text_surface, text_rect)

def user_name(surf,text,x,y,size):
  font = pg.font.Font(font_name, size) #определение шрифта
  text_surface = font.render(text, True, color=(255,255,255))
  text_rect = text_surface.get_rect()
  text_rect.midtop = (x, y)
  surf.blit(text_surface, text_rect)

fps = pg.time.Clock()
main = True
#вступительный экран
while main:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      exit()
    elif event.type == pg.KEYDOWN:
      if event.key == pg.K_BACKSPACE:
        name = name[:-1]
      elif event.key == pg.K_RETURN:
        main = False
      else:
        name += event.unicode
  win.fill((0,0,0))
  win.blit(bg, (0, 0)) #добавление фона в игру

  draw_text(win, 'Введите имя:', (w//2),(h//2))
  draw_text(win, name, w//2,((h//2) + 25))
  pg.display.update()
  fps.tick(60)

#сама игра
while health >= 1:
  for i in pg.event.get():
    if i.type == pg.QUIT:
      exit()
  fps.tick(60)
  # fps.tick(300) #побаловаться или для более быстрых тестов


  win.blit(stbg, (0,0))

  draw_text(win,name,15,15, color=(0,0,0))
  draw_text(win, f'Score:{score}', w//2,15,color=(255,255,255)) # кол-во очков

  Walls()  # создание стен
  all_sprites.update() # обновление спрайтов
  enemy_sprites.update()
  sphere_sprites.update()

  all_sprites.draw(win) # создание спрайтов
  enemy_sprites.draw(win)
  sphere_sprites.draw(win)

  sphere.update_pos()
  player.update()

  key = pg.key.get_pressed()
  if key[pg.K_UP]:
    player.jump()
    print("jump")
  # прыжок

  destroy_collision = pg.sprite.spritecollide(sphere, enemy_sprites, False, pg.sprite.collide_mask) # проверка на прикосновение врага и сферы
  if destroy_collision:
    score += 1
    enemy.new_pos() # тут враг меняет позицию при его уничтожении, но нужно, чтобы просто исчезал

  damage_collision = pg.sprite.spritecollide(player, enemy_sprites, False, pg.sprite.collide_mask) # проверка на прикосновение врага и игрока
  if damage_collision:
    health -= 1 # отнимает здоровье
    print(health)

  pg.display.update()

while True:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      exit()

  win.fill((0,0,0))
  pg.display.update()
  fps.tick(5)
