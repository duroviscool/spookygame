import pygame
import pygame as pg
import random

pg.init()

font_name = pg.font.match_font('Arial') #поиск шрифта
size = 18 #его размер

w,h = 1200,800 #размер окна

win = pg.display.set_mode((w,h))

bg = pg.image.load("replace.png") #загрузка (добавление) картинки
bg = pg.transform.scale(bg, (w,h)) #изменение картинки на полный экран

pg.display.set_caption("потом название придумаю") # название программы (игры)

stbg = pg.image.load('darkbg.jpg') # фон игры, потом нарисую
stbg = pg.transform.scale(stbg, (w,h))

#jump_sfx = pg.mixer.Sound()
#dmg_sfx = pg.mixer.Sound()

x = w//2
y = h//2

score = 0 # очки
max_health = 5 # макс. здоровье
health = 5 # текущее здоровье
immunity = False # временная неуязвимость после получения урона
immunity_time = 0

class Player(pg.sprite.Sprite): # создание игрока
  def __init__(self, plr_x, plr_y):
    pg.sprite.Sprite.__init__(self)

    self.plr_x = plr_x
    self.plr_y = plr_y
    self.plr_turn = False # в какую сторону движется игрок, если false, то правая сторона, если true, то левая сторона
    self.jumping = False
    self.falling = False
    # скорость бега/прыжка
    self.speed_x = 2
    # счет кардов для прыжка, падения
    self.floor = 0

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
    if self.floor < 3:
      self.rect.y -= 180
      self.floor += 1
  def fall(self):
    if self.floor > 0:
      self.rect.y += 180
      self.floor -= 1
  def update(self):
    self.rect.x += self.speed_x
    # проверка поворота
    if self.plr_turn:
      self.speed_x = -2
      self.image = self.image_flip
    else:
      self.speed_x = 2
      self.image = self.image_orig
    # поворот
    if self.rect.x >= (1080-64):
      self.plr_turn = True
    elif self.rect.x <= 120:
      self.plr_turn = False

class Enemy(pg.sprite.Sprite): # создание врага
  def __init__(self):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.image.load("ghost.png")
    self.image = pg.transform.scale(self.image, (64,64))

    self.rect = self.image.get_rect()
    self.rect.x = w//2  # ИЗНАЧАЛЬНАЯ позиция
    self.rect.y = h//2

    # данные об отраженной картинки игрока
    self.image_flip = pg.image.load("ghost.png")
    self.image_flip = pg.transform.scale(self.image_flip, (64, 64))
    self.image_flip = pg.transform.flip(self.image, True, False)

    # данные об неотраженной картинки игрока
    self.image_orig = pg.image.load("ghost.png")
    self.image_orig = pg.transform.scale(self.image_orig, (64, 64))
    self.image_orig = pg.transform.flip(self.image, False, False)
    self.speed_x = 4
    self.speed_y = 4
    self.plr_turn = False

  def create(self):
    self.speed_y = random.randrange(1,4)
    win.blit(self.image, (self.rect.x, self.rect.y))

  def update(self):
    self.rect.x += self.speed_x
    self.rect.y += self.speed_y
    if self.plr_turn:
      self.speed_x = -4
      self.image = self.image_orig
    else:
      self.speed_x = 4
      self.image = self.image_flip

    if self.rect.x >= 1160:
      self.plr_turn = True
    elif self.rect.x <= 40:
      self.plr_turn = False

    if self.rect.x >= (1080-64):
      self.plr_turn = True
    elif self.rect.x <= 120:
      self.plr_turn = False

    if self.rect.y >= (720-64):
      self.speed_y = -4
    elif self.rect.y <= 80:
      self.speed_y = 4

class Walls(): # создание границ стен, пола, потолка, платформ
  def __init__(self):
    self.floor_rect = pg.draw.rect(win, (0, 0, 0), (0, 720, 1200, 800))
    self.wall_rect1 = pg.draw.rect(win, (0, 0, 0), (0, 0, 120, 800))
    self.wall_rect2 = pg.draw.rect(win, (0, 0, 0), (1080, 0, 1200, 800))
    self.ceil_rect = pg.draw.rect(win, (0, 0, 0), (0, 0, 1200, 80))

    self.plat1 = pg.draw.rect(win, (0, 0, 0), (120, 540, 960, 20))
    self.plat2 = pg.draw.rect(win, (0, 0, 0), (120, 360, 960, 20))
    self.plat2 = pg.draw.rect(win, (0, 0, 0), (120, 180, 960, 20))

player = Player(w//2,720)
all_sprites = pg.sprite.Group()
all_sprites.add(player)

enemy_list = []
enemy = Enemy()
enemy_sprites = pg.sprite.Group()
enemy_sprites.add(enemy)

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
while health >= 1: #игра работает, пока здоровье больше 0
  for event in pg.event.get():
    if event.type == pg.QUIT:
      exit()
    elif event.type == pg.KEYDOWN: # передвижение
      if event.key == pg.K_UP:
        player.jump()
      if event.key == pg.K_DOWN:
        player.fall()
  win.blit(stbg, (0,0))

  draw_text(win,name,15,15, color=(255,255,255))
  draw_text(win, f'Score:{score}', w//2,15,color=(255,255,255)) # кол-во очков

  enemy_spawntime = pygame.time.get_ticks()

  Walls()  # создание стен
  all_sprites.update() # обновление спрайта
  all_sprites.draw(win)  # создание спрайта
  enemy_list.append(enemy)
  for enemy in enemy_list:
    enemy_sprites.draw(win)
    enemy_sprites.update()
    spawn_cooldown = pygame.time.get_ticks()

  player.update()

  damage_collision = pg.sprite.spritecollide(player, enemy_sprites, False, pg.sprite.collide_mask) # проверка на прикосновение врага и игрока

  if damage_collision and not immunity:
    health -= 1 # отнимает здоровье
    print(health)
    immunity = True
    immunity_time = pg.time.get_ticks()

  if pygame.time.get_ticks() - immunity_time > 1000:
    immunity = False

  pg.display.update()
  fps.tick(60) # частота смены кадров
  #fps.tick(300) # побаловаться или для более быстрых тестов

# конечный экран
active = True
while active:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      exit()
    elif event.type == pg.KEYDOWN:
      if event.key == pg.K_ESCAPE:
        active = False

  win.fill((0,0,0))
  draw_text(win, 'ТЫ СДОХ АХПХПХАПХАПХ', (w // 2), (h // 2))
  pg.display.update()
  fps.tick(60)
pg.quit()
