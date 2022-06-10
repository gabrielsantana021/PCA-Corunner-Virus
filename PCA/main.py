import pygame
import os
import random
from math import pi
pygame.init()
pygame.display.set_caption("Corunner Virus")


SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

CORRIDA = [pygame.image.load(os.path.join("Assets/Personagens", "Frente1.png")),
           pygame.image.load(os.path.join("Assets/Personagens", "Parado.png"))]
PULAR = pygame.image.load(os.path.join("Assets/Personagens", "Frente1.png"))
AGACHAR = [pygame.image.load(os.path.join("Assets/Personagens", "Frente2.png")),
           pygame.image.load(os.path.join("Assets/Personagens", "Tras2.png"))]

CANO = [pygame.image.load(os.path.join("Assets/Cenário", "obstaculo1.png")),
              pygame.image.load(os.path.join("Assets/Cenário", "obstaculo2.png")),
              pygame.image.load(os.path.join("Assets/Cenário", "obstaculo3.png")),
              pygame.image.load(os.path.join("Assets/Cenário", "obstaculo4.png"))]


PASSARO = [pygame.image.load(os.path.join("Assets/Pássaro", "passaro1.png")),
           pygame.image.load(os.path.join("Assets/Pássaro", "passaro2.png"))]

NUVEM = pygame.image.load(os.path.join("Assets/Cenário", "nuvem.png"))

BG = pygame.image.load(os.path.join("Assets/Cenário", "Pista.png"))


class Medico:
    X_POS = 80
    Y_POS = 310
    Y_POS_AGACHAR = 340
    PULAR_VEL = 8.5

    def __init__(self):
        self.agachar_img = AGACHAR
        self.corrida_img = CORRIDA
        self.pular_img = PULAR

        self.medico_agachar = False
        self.medico_corrida = True
        self.medico_pular = False

        self.step_index = 0
        self.pular_vel = self.PULAR_VEL
        self.image = self.corrida_img[0]
        self.medico_rect = self.image.get_rect()
        self.medico_rect.x = self.X_POS
        self.medico_rect.y = self.Y_POS

    def update(self, userInput):
        if self.medico_agachar:
            self.agachar()
        if self.medico_corrida:
            self.corrida()
        if self.medico_pular:
            self.pular()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.medico_pular:
            self.medico_agachar = False
            self.medico_corrida = False
            self.medico_pular = True
        elif userInput[pygame.K_DOWN] and not self.medico_pular:
            self.medico_agachar = True
            self.medico_corrida = False
            self.medico_pular = False
        elif not (self.medico_pular or userInput[pygame.K_DOWN]):
            self.medico_agachar = False
            self.medico_corrida = True
            self.medico_pular = False

    def agachar(self):
        self.image = self.agachar_img[self.step_index // 5]
        self.medico_rect = self.image.get_rect()
        self.medico_rect.x = self.X_POS
        self.medico_rect.y = self.Y_POS_AGACHAR
        self.step_index += 1

    def corrida(self):
        self.image = self.corrida_img[self.step_index // 5]
        self.medico_rect = self.image.get_rect()
        self.medico_rect.x = self.X_POS
        self.medico_rect.y = self.Y_POS
        self.step_index += 1

    def pular(self):
        self.image = self.pular_img
        if self.medico_pular:
            self.medico_rect.y -= self.pular_vel * 4
            self.pular_vel -= 0.8
        if self.pular_vel < - self.PULAR_VEL:
            self.medico_pular = False
            self.pular_vel = self.PULAR_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.medico_rect.x, self.medico_rect.y))


class Nuvem:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = NUVEM
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallPipe(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 350


class Passaro(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Medico()
    nuvem = Nuvem()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Sua pontuação: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        BLUE = (135, 206, 250)
        SCREEN.fill(BLUE)
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallPipe(CANO))
            elif random.randint(0, 2) == 2:
                obstacles.append(Passaro(PASSARO))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.medico_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        nuvem.draw(SCREEN)
        nuvem.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render(
                "Pressione qualquer tecla para começar", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render(
                "Pressione qualquer tecla para recomeçar", True, (0, 0, 0))
            score = font.render("Sua pontuação: " +
                                str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(CORRIDA[0], (SCREEN_WIDTH // 2 -
                    20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)
