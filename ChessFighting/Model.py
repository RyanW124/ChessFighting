import main, pygame, Chess, convertpath
from random import randint
window_size_y = 830
window_size_x = int(window_size_y*1.7)
SIZE = (window_size_x, window_size_y)
class Player:
    def __init__(self, consciousness):
        self.consciousness = consciousness
        self.time = 300
        self.fighter = None
        self.move_time = 30
    def update_time(self):
        self.move_time = int(self.consciousness*0.3)
        if self.move_time<5:
            self.move_time=5
        if self.move_time>self.time:
            self.move_time = self.time

class Game:
    def __init__(self):
        self.round = 1
        self.p1 = Player(100)
        self.p2 = Player(100)
        self.board = Chess.Board()
        self.winner = None
        self.finished = False
        self.fight_time = 30
        self.chess_time = 60

class Button:
    main_menu = []
    settings = []
    help_menu = []
    pause = []
    end = []
    choose = []
    def __init__(self, rect, text, color, name, textColor, scene, outline = None):
        self.rect = rect
        self.text = text
        self.color = color
        self.name = name
        self.textColor = textColor
        self.surface = pygame.Surface(self.rect.size)
        self.outline = outline
        self.surface.fill(self.color)
        if outline:
            pygame.draw.rect(self.surface, outline[0], pygame.Rect((0,0), self.rect.size), outline[1])
        font = pygame.font.Font('freesansbold.ttf', self.rect.height//4)
        text = font.render(text, True, self.textColor, self.color)
        textRect = text.get_rect()
        textRect.center = self.surface.get_rect().center
        self.surface.blit(text, textRect)
        scene.append(self)
    def update(self):
        self.surface = pygame.Surface(self.rect.size)
        self.surface.fill(self.color)
        if self.outline:
            pygame.draw.rect(self.surface, self.outline[0], pygame.Rect((0,0), self.rect.size), self.outline[1])
        font = pygame.font.Font('freesansbold.ttf', self.rect.height//4)
        text = font.render(self.text, True, self.textColor, self.color)
        textRect = text.get_rect()
        textRect.center = self.surface.get_rect().center
        self.surface.blit(text, textRect)
    @classmethod
    def get_button(cls, scene, name):
        for i in scene:
            if i.name == name:
                return i
        return None
class Settings:
    def __init__(self):
        self.p2_attack1 = pygame.K_COMMA
        self.p2_attack2 = pygame.K_PERIOD
        self.p2_jump = pygame.K_UP
        self.p2_left = pygame.K_LEFT
        self.p2_right = pygame.K_RIGHT

        self.p1_attack1 = pygame.K_t
        self.p1_attack2 = pygame.K_y
        self.p1_jump = pygame.K_w
        self.p1_left = pygame.K_a
        self.p1_right = pygame.K_d

        self.quit = pygame.K_q
        self.pause = pygame.K_ESCAPE

    def __iter__(self):
        for i in [self.p2_attack1, self.p2_attack2, self.p2_jump, self.p2_left, self.p2_right, self.p1_attack1, self.p1_attack2,
                self.p1_jump, self.p1_left, self.p1_right, self.quit]:
                    yield i


class AudioController:

    def __init__(self, filename, v=0.5, loop=0):
        self.volume = v
        self.right_channel = 0.5
        path = convertpath.path(['sounds', filename])
        self.mix = pygame.mixer.Sound(path)
        self.channel = pygame.mixer.find_channel()
        self.channel.play(self.mix, loops = loop)
        self.channel.set_volume(self.volume)
    def stop(self):
        self.channel.stop()
class MeteorWarning:
    initial_frequence = 7
    def __init__(self, w, h, color):
        self.fading = False
        self.h = h
        self.color = color
        self.frequency = 5
        self.surface = pygame.Surface((w, h))
        self.dropping = False
        self.surface.fill(color)
        self.surface.set_alpha(125)
        self.meteor = Meteor(self.surface, h)

    def update(self):
        if self.dropping:
            self.surface.fill((0,0,0))
            self.surface.set_alpha(255)

            self.meteor.draw()
            self.surface.set_colorkey(self.surface.get_at((0,0)))
            if self.meteor.y >= self.h:
                self.dropping = False
                self.surface.fill(self.color)
                self.surface.set_alpha(125)
                self.meteor.set_y(-50)
                return True
        else:
            if self.frequency==2:
                self.frequency=5
                self.dropping = True

            else:
                if self.fading:
                    self.surface.set_alpha(self.surface.get_alpha()-125/self.frequency)
                    if self.surface.get_alpha()<=0:
                        self.fading = False
                        self.frequency-=1
                else:
                    self.surface.set_alpha(self.surface.get_alpha()+125/self.frequency)
                    if self.surface.get_alpha()>=125:
                        self.fading = True
        return False
class Meteor:
    def __init__(self, surface, h):
        self.y = -50
        self.h = h
        self.surface = surface
        self.image = pygame.image.load(convertpath.path(['sprites', 'meteor.png'])).convert()
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = self.surface.get_rect().center
        self.rect.bottom = self.y
    def set_y(self, num):
        self.y = num
        self.rect.bottom = self.y
    def draw(self):
        self.y+=50
        if self.y>=self.h:
            self.y = self.h
        self.rect.bottom = self.y
        self.surface.blit(self.image, self.rect)


class Zone:

    def __init__(self, width, time, p1, p2):
        self.width = width
        self.left = 0
        self.p1 = p1
        self.p1_dmg = 0
        self.p2 = p2
        self.p2_dmg = 0
        self.time = time
        self.dist_left = 0
        self.dest_right = 0
        self.right = SIZE[0]
        self.new()
    def update(self):
        self.left+=self.dist_left/self.time
        self.right+=self.dist_right/self.time
        self.p1_dmg+=1
        if (self.p1.rect.centerx < self.left or self.p1.rect.centerx > self.right) and self.p1_dmg>=10:
            self.p1.parent.consciousness-=1
            self.p1_dmg=0
        self.p2_dmg+=1
        if (self.p2.rect.centerx < self.left or self.p2.rect.centerx > self.right) and self.p2_dmg>=10:
            self.p2.parent.consciousness-=1
            self.p2_dmg=0
        if (self.dist_right>0 and self.right>=self.dest_right) or (self.dist_right<0 and self.right<=self.dest_right):
            self.new()
    def draw(self):
        surface=pygame.Surface(SIZE)
        pygame.draw.rect(surface, (255, 0, 255, 20), pygame.Rect(0,0,self.left, SIZE[1]*0.8))
        pygame.draw.rect(surface, (255, 0, 255, 20), pygame.Rect(self.right,0,SIZE[0]-self.right, SIZE[1]*0.8))

        surface.set_alpha(50)
        return surface
    def new(self):
        self.dist_right = 0
        while abs(self.dist_right)<200:
            self.dest_left = randint(0, SIZE[0]-self.width)
            self.dest_right = self.dest_left+self.width
            self.dist_left = self.dest_left-self.left

            self.dist_right = self.dest_right-self.right


if __name__ == "__main__":
    main.main()