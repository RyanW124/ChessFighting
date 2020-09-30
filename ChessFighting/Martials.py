import pygame, convertpath, main
animations = [IDLE, ATTACK_ONE, ATTACK_TWO, JUMP, FALL, RUN, TAKE_HIT, DEATH] = range(8)
SIZE = (1.7*830, 830)
class Blue(pygame.sprite.Sprite):
    max_jump = 30
    gravity = 6
    def __init__(self, sprite_path, x, y, parent):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.cd1 = 20
        self.cd2 = 50
        self.t1 = self.cd1
        self.t2 = self.cd2
        self.speed = 10
        self.path = sprite_path
        self.parent = parent
        self.rect = None
        self.animation = 0
        self.dir = True
        self.timer = 0
        self.loop = False
        self.knockback = 0
        self.jump_power = self.max_jump
        self.images = []
        self.already = False
        for i in ['Idle', 'Attack1', 'Attack2', 'Jump', 'Fall', 'Run', 'Take hit', 'Death']:
            self.images.append(pygame.image.load(convertpath.path(sprite_path+[f'{i}.png'])).convert())

        self.frames = 0
#         for i in range(len(self.images)):
#             self.images[i].set_colorkey(self.images[i].get_at((0,0)))
        # self.animations = [[pygame.Rect(80, 70, 36, 59)],
#                             [pygame.Rect(472, 69, 41, 53), pygame.Rect(673, 69, 41, 53), pygame.Rect(882, 53, 109, 69), pygame.Rect(107, 69, 1082, 53)]
#         ]
        self.animations = [[pygame.Rect(80, 70, 36, 59)],
                            [pygame.Rect(76, 63, 30, 65), pygame.Rect(271, 63, 35, 65), pygame.Rect(493, 68, 90, 60), pygame.Rect(693, 74, 34, 54)],
                            [pygame.Rect(82, 77, 45, 51), pygame.Rect(279, 72, 49, 56), pygame.Rect(490, 43, 96, 83), pygame.Rect(693, 86, 72, 42)],
                            [pygame.Rect(86, 72, 36, 56), pygame.Rect(286, 73, 36, 54)],
                            [pygame.Rect(83, 75, 36, 53), pygame.Rect(283, 74, 37, 54)],
                            [pygame.Rect(72, 81, 44, 47), pygame.Rect(272, 81, 44, 47), pygame.Rect(472, 81, 44, 47), pygame.Rect(672, 81, 44, 47),
                            pygame.Rect(872, 81, 44, 47), pygame.Rect(1072, 81, 44, 47), pygame.Rect(1272, 81, 44, 47), pygame.Rect(1472, 81, 44, 47)],
                            [pygame.Rect(80, 71, 36, 55), pygame.Rect(280, 72, 30, 56), pygame.Rect(481, 72, 33, 56)]
        ]
        self.animate(IDLE)
    def jump(self):
        self.jump_power=self.max_jump
        self.y-=self.jump_power
        self.animate(2, JUMP, True)
    def take_damage(self, damage, pos):
        self.parent.consciousness -= damage
        self.animate(7, TAKE_HIT, False)
        if pos>self.x:
            self.dir = True
            self.knockback = -5
        else:
            self.dir = False
            self.knockback = 5
    def update(self, oppo):

        self.animate()
        if self.t1<self.cd1:
            self.t1+=1
        if self.t2<self.cd2:
            self.t2+=1
        if self.animation == ATTACK_ONE and self.rect.colliderect(oppo.rect) and not self.already:
            self.already = True
            oppo.take_damage(10, self.x)
        if self.knockback<0:
            self.x+=self.knockback
            self.knockback+=1
        elif self.knockback>0:
            self.x+=self.knockback
            self.knockback-=1
#         print(self.animation)
        if self.y!=SIZE[1]*0.8:
            self.y-=self.jump_power

            if SIZE[1]*0.8-self.y<self.jump_power:
                self.y = SIZE[1]*0.8
            else:
                self.jump_power-=self.gravity
                if self.jump_power <=0 and not self.animation in [FALL, ATTACK_ONE, ATTACK_TWO]:
                    self.animate(2, FALL, True)
        if self.y >= SIZE[1]*0.8 and not self.animation in [IDLE, RUN, ATTACK_ONE, ATTACK_TWO, TAKE_HIT]:
            self.animation = IDLE
        self.rect = self.draw_rect.copy()

        self.rect.midbottom = (self.x, self.y)
        # if self.dir:
#             self.rect.bottomleft = (self.x, self.y)
#         else:
#             self.rect.bottomright = (self.x, self.y)
    def draw(self):
        surface = pygame.Surface(self.rect.size)
        surface.blit(self.images[self.animation], (0,0), self.draw_rect)
        if not self.dir:
            surface = pygame.transform.flip(surface, True, False)
        surface.set_colorkey(surface.get_at((0,0)))

        return surface
    def animate(self, frames = None, a = None, loop= None):
        if frames:
            self.frames = frames
        if loop!=None:
            self.loop = loop
        if a:
            self.timer= 0
            self.animation = a
        if self.animation!= IDLE:
            self.draw_rect = self.animations[self.animation][self.timer//self.frames]
            if self.timer//self.frames == len(self.animations[self.animation])-1:
                self.timer = 0
                if not self.loop:
                    if self.animation == ATTACK_ONE:
                        self.already = False
                    self.animation = IDLE
            self.timer+=1
        else:
            self.draw_rect = self.animations[self.animation][0]
class Red(Blue):
    def __init__(self, sprite_path, x, y, parent):
        super().__init__(sprite_path, x, y, parent)
        self.dir = False
        self.animations = [[pygame.Rect(80, 70, 36, 59)],
                            [pygame.Rect(472, 69, 41, 53), pygame.Rect(673, 69, 41, 53), pygame.Rect(882, 53, 109, 69), pygame.Rect(1082, 69, 107, 53)],
                            [pygame.Rect(484, 57, 47, 65), pygame.Rect(684, 57, 47, 65), pygame.Rect(884, 69, 109, 53), pygame.Rect(1085, 75, 107, 53)],
                            [pygame.Rect(86, 72, 36, 56), pygame.Rect(286, 73, 36, 54)],
                            [pygame.Rect(80, 75, 36, 53), pygame.Rect(280, 74, 37, 54)],
                            [pygame.Rect(72, 81, 44, 47), pygame.Rect(272, 81, 44, 47), pygame.Rect(472, 81, 44, 47), pygame.Rect(672, 81, 44, 47),
                            pygame.Rect(872, 81, 44, 47), pygame.Rect(1072, 81, 44, 47), pygame.Rect(1272, 81, 44, 47), pygame.Rect(1472, 81, 44, 47)],
                            [pygame.Rect(80, 71, 36, 55), pygame.Rect(280, 72, 30, 56), pygame.Rect(481, 72, 33, 56)]
        ]
class Bullet(pygame.sprite.Sprite):
    speed = 40
    bullets = []
    def __init__(self, player, parent, oppo):
        pygame.sprite.Sprite.__init__(self)
        Bullet.bullets.append(self)
        self.dir = parent.dir
        self.oppo = oppo

        if player ==2:
            self.image = pygame.image.load(convertpath.path(['Martial Hero 2', 'Sprites', 'bullet.png'])).convert()
        else:
            self.image = pygame.image.load(convertpath.path(['Martial Hero', 'Sprites', 'bullet.png'])).convert()
        self.image.set_colorkey(self.image.get_at((0,0)))
        if self.dir:
            self.x, self.y = parent.rect.midright
            self.rect = self.image.get_rect()
            self.rect.midleft = (self.x-100, self.y)
        else:
            self.x, self.y = parent.rect.midleft
            self.rect = self.image.get_rect()
            self.rect.midright = (self.x+100, self.y)

    def update(self):
        if self.dir:
            self.x+=self.speed
            self.rect.centerx+=self.speed
        else:
            self.x-=self.speed
            self.rect.centerx-=self.speed
        if self.rect.colliderect(self.oppo.rect):
            self.oppo.parent.consciousness-=3
            Bullet.bullets.remove(self)
            del self
    def draw(self, surface):
        im = self.image
        if not self.dir:
            im = pygame.transform.flip(self.image, True, False)
        surface.blit(im, self.rect)
if __name__ == '__main__':
    main.main()