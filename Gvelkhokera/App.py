import random
import time
import pygame
pygame.init()


class Food:
    def __init__(self):
        self.fr = 30
        self.fx = random.randint(self.fr, App.width - 30)
        self.fy = random.randint(self.fr, App.length - 30)
        self.xrl, self.xrr = (self.fx - self.fr, self.fx + self.fr)
        self.yru, self.yrd = (self.fy - self.fr, self.fy + self.fr)
        self.img = pygame.image.load('ვაშლი.png')
        self.img1 = pygame.image.load('ბაყაყი.png')
        self.times = random.randint(0, 100)

    def render(self, screen):
        if self.times == 7:
            screen.blit(self.img1, (self.fx, self.fy))
        else:
            self.times += 1
            screen.blit(self.img, (self.fx, self.fy))


class Body:
    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.sX = 1
        self.sY = 0
        self.img = pygame.image.load('ტანი.png')
        self.img1 = pygame.image.load('თავი.png')

    def update(self):
        self.X += self.sX
        self.Y += self.sY

    def render(self, screen):
        screen.blit(self.img, (self.X, self.Y))

    def render1(self, screen):
        screen.blit(self.img1.convert_alpha(screen), (self.X, self.Y))


class App:
    width, length = 1200, 600
    pygame.mixer.init()

    def __init__(self):
        self.running = False
        self.clock = None
        self.x, self.y = App.width / 2, App.length / 2
        self.body = [Body(self.x + 60, self.y), Body(self.x + 45, self.y), Body(self.x + 30, self.y),
                     Body(self.x + 15, self.y), Body(self.x, self.y)]
        self.food = Food()
        self.score = 0
        self.background = pygame.image.load('ფონი.jpg')
        self.end = pygame.image.load('დასასრული.jpeg')
        self.rules = pygame.image.load('წესები.jpeg')
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.screen = None

    def run(self):
        self.init()
        while self.running:
            self.update()
            self.render()
        self.clean_up()

    def init(self):
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('მარებელი.mp3'), -1)
        self.screen = pygame.display.set_mode((App.width, App.length))
        self.background.convert_alpha(self.screen)
        pygame.display.set_caption('გველხოკერა')
        self.clock = pygame.time.Clock()
        self.screen.blit(self.rules, (0, 0))
        self.render()
        time.sleep(10)
        pygame.font.init()
        self.running = True

    def collision(self):
        if (self.body[0].X >= (App.width - 45) or self.body[0].X < -15) or \
                (self.body[0].Y >= (App.length - 45) or self.body[0].Y < -10):
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('დატაკება.mp3'), 0)
            for ball in self.body:
                ball.sX, ball.sY = 0, 0
        for ball in self.body[1:]:
            if self.body[0].X == ball.X and self.body[0].Y == ball.Y:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('დატაკება.mp3'), 0)
                self.body[0].sX, self.body[0].sY = 0, 0

    def update(self):
        if self.play_again():
            self.screen.blit(self.end, (0, 0))
            pygame.display.flip()
            time.sleep(3)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_SPACE:
                        self.__init__()
                        self.init()
        for circle in self.body:
            if self.body.index(circle) % 2 == 1:
                circle.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.events()
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        self.body[0].update()
        self.body[0].render1(self.screen)
        for ball in self.body[1:len(self.body)]:
            if ball.X == self.body[self.body.index(ball) - 1].X or ball.Y == self.body[self.body.index(ball) - 1].Y:
                ball.sX = self.body[self.body.index(ball) - 1].sX
                ball.sY = self.body[self.body.index(ball) - 1].sY
            ball.update()
            ball.render(self.screen)
            self.food.render(self.screen)
            self.eat()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_UP:
                    if self.body[0].sX != 0 and self.body[0].sY != 1:
                        self.body[0].sX = 0
                        self.body[0].sY = -1
                if event.key == pygame.K_DOWN:
                    if self.body[0].sX != 0 and self.body[0].sY != -1:
                        self.body[0].sX = 0
                        self.body[0].sY = 1
                if event.key == pygame.K_RIGHT:
                    if self.body[0].sX != -1 and self.body[0].sY != 0:
                        self.body[0].sX = 1
                        self.body[0].sY = 0
                if event.key == pygame.K_LEFT:
                    if self.body[0].sX != 1 and self.body[0].sY != 0:
                        self.body[0].sX = -1
                        self.body[0].sY = 0
                if event.key == pygame.K_m:
                    pygame.mixer.Channel(0).stop()
                if event.key == pygame.K_n:
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('მარებელი.mp3'), -1)
        self.collision()

    def play_again(self):
        return self.body[0].sX == 0 and self.body[0].sY == 0

    def eat(self):
        if self.body[0].X in range(self.food.xrl, self.food.xrr) and self.body[0].Y in range(self.food.yru, self.food.yrd):
            self.score += 1
            pygame.mixer.Channel(2).play(pygame.mixer.Sound('ჭამა.mp3'), 0)
            new_hd = Body(self.body[-1].X - 15*self.body[-1].sX, self.body[-1].Y - 15*self.body[-1].sY)
            new_hd.sY = self.body[-1].sY
            new_hd.sX = self.body[-1].sX
            self.body.append(new_hd)
            new_food = Food()
            self.food = new_food

    def render(self):
        surface = self.font.render('Points: ' + str(self.score), False, (255, 0, 0))
        self.screen.blit(surface, (0, 0))
        pygame.display.flip()
        self.clock.tick(500)

    def clean_up(self):
        pass


if __name__ == "__main__":
    app = App()
    app.run()
