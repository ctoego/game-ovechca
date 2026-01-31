import pygame, sys
import random 
import configparser, ast



try:

    config = configparser.ConfigParser()     # создаём объекта парсера
    config.read('config.ini')
    
except :
    print(f"ошибка в 'config.ini'")





WIDTH = config.getint('game', 'WIDTH')
HEIGHT = config.getint('game', 'HEIGHT')
FPS = config.getint('game','fps')

WHITE = ast.literal_eval(config.get('color',"WHITE"))       # "(255, 255, 255)"
BLUE =  ast.literal_eval(config.get('color',"BLUE"))
GREEN = ast.literal_eval(config.get('color',"GREEN"))
pygame.font.init()



f2 = pygame.font.SysFont('serif', config.getint('text','f1_size'))
f1 = pygame.font.Font(None, config.getint('text','f2_size'))


game_run = False
running = True
score = 0
dx = 10
dy = 10
speed = 3

max_x_eat = config.getint('sprite','max_x_eat')                    #* где может появиться еда
max_y_eat = config.getint('sprite','max_y_eat')     
min_x_eat = config.getint('sprite','min_x_eat')     
min_y_eat = config.getint('sprite','min_y_eat')     

ENEMY_CENTER = ast.literal_eval(config.get('sprite','ENEMY_CENTER'))
EAT_CENTER = ast.literal_eval(config.get('sprite','EAT_CENTER'))
# класс врага 
class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        enemy1_img = pygame.image.load("wolf.png").convert_alpha()
        self.image = enemy1_img
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2 - 10)
        


class Player(pygame.sprite.Sprite): #спрайт овечки

    def __init__(self):

        super().__init__()

        player_img = pygame.image.load("sheep.png").convert_alpha()
        self.image = player_img

        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2 - 10)

        self.rect.center = (WIDTH // 2, HEIGHT // 2)

        self.x_change = speed

        self.y_change = speed
       

        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] :   self.x_change = -speed
        if keys[pygame.K_d] :   self.x_change = speed
        if keys[pygame.K_w] :   self.y_change = -speed
        if keys[pygame.K_s] :   self.y_change = speed

        self.rect.x += self.x_change

        self.rect.y += self.y_change

    
class Eat(pygame.sprite.Sprite): #спрайт еды
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface(ast.literal_eval(config.get('sprite','eat_size')))
        self.image.fill(BLUE)  # Синий цвет
        self.rect = self.image.get_rect()
        self.rect.center = EAT_CENTER
        self.radius = config.getint('sprite','eat_radius')

pygame.display.set_caption('Овечка и волк')
# Создаем экран и группы спрайтов

screen = pygame.display.set_mode((WIDTH, HEIGHT))
all_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()
enemies = pygame.sprite.Group()


player = Player()
eat = Eat()
enemy1 = Enemy1()
enemies.add(enemy1)
all_sprites.add(player,  eat)
# рендерим текст
color_text = ast.literal_eval(config.get('text','color'))
text1 = f1.render('Hello ,Привет.', True,(color_text))#цвет
text2 = f2.render("Z - играть на лёгком уровне", False, (color_text))#цвет
text3 = f2.render("X - играть на среднем уровне", False, (color_text))#цвет
text4 = f2.render("C - играть на сложном уровне", False, (color_text))#цвет
# Главный цикл игры

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()
    if game_run == True:
        
            
        enemy1.rect.x += dx
        enemy1.rect.y += dy
            # Отскок от границ
        if enemy1.rect.x < 0 or enemy1.rect.x > WIDTH - 50:
            dx = -dx
        if enemy1.rect.y < 0 or enemy1.rect.y > HEIGHT - 50:
            dy = -dy

        
        clock.tick(FPS)
        for event in pygame.event.get(): #запуск
            if event.type == pygame.QUIT:
                running = False
        if player.rect.x < 0 or player.rect.x > WIDTH - 50 or player.rect.y < 0 or player.rect.y > HEIGHT - 50: #уход за границы игрового поля
            y_player = random.randint(50, WIDTH - 50)
            x_player = random.randint(50, HEIGHT - 50)
            player.rect.center = (y_player, x_player)#помещаем в центр поля
            
     #   if pygame.sprite.collide_rect_ratio(player, enemy1, 0.7): #столкновение с врагом
        if pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_circle):
            game_run = False
        
        if pygame.sprite.collide_circle(player, eat):# столкновение с едой
            print("Столкновение! с едой")
            y_eat = random.randint(min_x_eat, max_x_eat)
            x_eat = random.randint(min_y_eat, max_y_eat)
            eat.rect.center = (y_eat, x_eat)
            score += 1
        
        # Рендерим

        all_sprites.update()
        enemies.update()
        screen.fill(GREEN)  # Заполнение фона, цвет
        
        all_sprites.draw(screen)  # Отрисовка спрайтов
        enemies.draw(screen)
        i= "твой счёт:" + str(score)

        
        text_sc = f2.render(i, False, (180, 0, 0))#цвет
        screen.blit(text_sc, (10, 100))
        pygame.display.flip()  # Обновление экрана
    else:
        if keys[pygame.K_z]:
            player.rect.center = (WIDTH // 2, HEIGHT // 2)
            enemy1.rect.center = ENEMY_CENTER
            speed = 3;game_run = True
            score = 0
            dx = 10
            dy = 10
        if keys[pygame.K_x]:
            player.rect.center = (WIDTH // 2, HEIGHT // 2)
            enemy1.rect.center = ENEMY_CENTER
            speed = 2;game_run = True
            score = 0
            dx = 10
            dy = 10
        if keys[pygame.K_c]:
            player.rect.center = (WIDTH // 2, HEIGHT // 2)
            enemy1.rect.center = ENEMY_CENTER
            speed = 1;game_run = True
            score = 0
            dx = 10
            dy = 10

        screen.blit(text1, ast.literal_eval(config.get('text','xy_text1')))
        
        screen.blit(text2, ast.literal_eval(config.get('text','xy_text2')))
        
        screen.blit(text3, ast.literal_eval(config.get('text','xy_text3')))
        
        screen.blit(text4, ast.literal_eval(config.get('text','xy_text4')))
        
        pygame.display.flip() 



pygame.quit()