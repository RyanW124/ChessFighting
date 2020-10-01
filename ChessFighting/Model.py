import main, pygame, Chess

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

class Button:
    main_menu = []
    settings = []
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
    def get_button(self, scene, name):
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


if __name__ == "__main__":
    main.main()