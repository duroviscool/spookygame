import pygame as pg
import random

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

class Enemy(pg.sprite.Sprite): # создание врага
  def __init__(self):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.image.load("ghost.png")
    self.image = pg.transform.scale(self.image, (64,64))
    self.rect = self.image.get_rect()
    self.rect.x = random.randrange(60,1140) # ИЗНАЧАЛЬНАЯ позиция
    self.rect.y = random.randrange(60,740)
  def new_pos(self): # смена позиции
    self.rect.x = random.randrange(60, 1140)
    self.rect.y = random.randrange(60, 740)
class Player(pg.sprite.Sprite): # создание игрока
  def __init__(self, plr_x, plr_y):
    pg.sprite.Sprite.__init__(self)
    self.plr_x = plr_x
    self.plr_y = plr_y
    self.speed_x = 1
    self.speed_y = -1
    self.plr_turn = False
    self.image = pg.image.load("player.png")
    self.image = pg.transform.scale(self.image, (64,64))
    self.rect = self.image.get_rect()
    self.rect.centerx = self.plr_x
    self.rect.bottom = self.plr_y
  def update(self):
    self.rect.x += self.speed_x
    self.rect.y += self.speed_y
    key = pg.key.get_pressed()
    if key[pg.K_UP]:
      self.speed_y = -1
    if key[pg.K_DOWN]:
      self.speed_y = 1
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
class Sphere(pg.sprite.Sprite): # создание сферы
  def __init__(self):
    pg.sprite.Sprite.__init__(self)
    self.x = x
    self.y = y
    self.spin_speed = 3
    self.image = pg.image.load("light_sphere.png")
    self.image = pg.transform.scale(self.image, (32,32))
    self.rect = self.image.get_rect()
    self.rect.centerx = self.x
    self.rect.bottom = self.y
  def update(self):
    pass # потом напишу, это не выглядит простым

all_sprites = pg.sprite.Group()
player = Player(w//2,h//2)
all_sprites.add(player)

enemy = Enemy()
enemy_sprites = pg.sprite.Group()
enemy_sprites.add(enemy)

sphere = Sphere()
sphere_sprites = pg.sprite.Group()
sphere_sprites.add(sphere)

#вступительный экран
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
  draw_text(win, name, 300,325)
  pg.display.update()
  fps.tick(60)

#сама игра
alive = True
while alive:
  for i in pg.event.get():
    if i.type == pg.QUIT:
      exit()

  win.blit(stbg, (0,0))

  draw_text(win,name,15,15, color=(0,0,0))
  draw_text(win, f'Score:{score}', w//2,15,color=(0,0,0)) # кол-во очков

  all_sprites.update() # обновление спрайтов
  enemy_sprites.update()
  sphere_sprites.update()

  all_sprites.draw(win) # создание спрайтов
  enemy_sprites.draw(win)
  sphere_sprites.draw(win)

  destroy_collision = pg.sprite.spritecollide(sphere, enemy_sprites, False, pg.sprite.collide_mask) # проверка на прикосновение врага и сферы
  if destroy_collision:
    score += 1
    enemy.new_pos() # тут враг меняет позицию при его уничтожении, но нужно, чтобы просто исчезал

  damage_collision = pg.sprite.spritecollide(player, enemy_sprites, False, pg.sprite.collide_mask) # проверка на прикосновение врага и игрока
  if damage_collision:
    health -= 1 # отнимает здоровье

  if health <= 0: # проверка на количество здоровья (если 0 или меньше, игра заканчивается)
    alive = False
  pg.display.update()
  fps.tick(60)
