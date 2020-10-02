import pygame, Controller, main, Model, convertpath, Martials
from UI import pause_menu
from random import randint
animations = [IDLE, ATTACK_ONE, ATTACK_TWO, JUMP, FALL, RUN, TAKE_HIT, DEATH] = range(8)
SIZE = None
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
PURPLE = (255, 0, 255)
r_value = 150
BROWN = (r_value, r_value/2, 0)
def game_fight(surface : pygame.Surface, game, clock, keys):
    global SIZE
    SIZE = (main.window_size_x, main.window_size_y)
    quit = False
    bkgrnd = str(randint(1, 2))

    blit_image(surface, ['Background', bkgrnd+'.png'], "topleft", (0,0), (int(SIZE[0]), int(SIZE[1])))
#     blit_image(surface, ['Martial Hero', 'Sprites', 'Idle.png'], "topleft", (0,0))

    p1 = game.p1.fighter
    p2 = game.p2.fighter
    pl = False
    pr = False
    p1j = False
    pl2 = False
    pr2 = False
    p2j = False
    home = False
    music = Model.AudioController('fight.wav', 0.2, -1)
    while True:
        clock.tick(30)
        surface.fill((0,0,0))
        quit, pause, shoot, pl, pr, p1j, shoot2, pl2, pr2, p2j, s1, s2= Controller.fight1(game, pl, pr, p1j, pl2, pr2, p2j, keys)

        if pl2 and not pr2 and p2.animation!=TAKE_HIT and p2.rect.left>p2.speed:
            p2.dir = False
            p2.x-=p2.speed
            if not p2.animation in [ATTACK_ONE, ATTACK_TWO, RUN]:
                p2.animate(2, RUN, True)
        elif pr2 and not pl2 and p2.animation!=TAKE_HIT and p2.rect.right<SIZE[0]-p2.speed:
            p2.dir = True
            p2.x+=p2.speed
            if not p2.animation in [ATTACK_ONE, ATTACK_TWO, RUN]:
                p2.animate(2, RUN, True)
        else:
            if not p2.animation in [ATTACK_ONE, ATTACK_TWO, TAKE_HIT]:
                p2.animation = IDLE
        if p2j and p2.y>=SIZE[1]*0.8:
            p2.jump()
        if shoot2 and p2.t1>=p2.cd1 and not p2.animation in [ATTACK_ONE, ATTACK_TWO]:
            p2.animate(2, ATTACK_ONE, False)
            p2.t1 = 0
        if s2 and p2.t2>=p2.cd2 and not p2.animation in [ATTACK_ONE, ATTACK_TWO]:
            p2.animate(2, ATTACK_TWO, False)
            Martials.Bullet(2, game.p2.fighter, game.p1.fighter)
            p2.t2 = 0


        if pl and not pr and p1.animation!=TAKE_HIT and p1.rect.left>p1.speed:
            p1.dir = False
            p1.x-=p1.speed
            if not p1.animation in [ATTACK_ONE, ATTACK_TWO, RUN]:
                p1.animate(2, RUN, True)
        elif pr and not pl and p1.animation!=TAKE_HIT and p1.rect.right<SIZE[0]-p1.speed:
            p1.dir = True
            p1.x+=p1.speed
            if not p1.animation in [ATTACK_ONE, ATTACK_TWO, RUN]:
                p1.animate(2, RUN, True)
        else:
            if not p1.animation in [ATTACK_ONE, ATTACK_TWO, TAKE_HIT]:
                p1.animation = IDLE
        if p1j and p1.y>=SIZE[1]*0.8:
            p1.jump()

        if shoot and p1.t1>=p1.cd1 and not p1.animation in [ATTACK_ONE, ATTACK_TWO]:
            p1.animate(2, ATTACK_ONE, False)
            p1.t1 = 0
        if s1 and p1.t2>=p1.cd2 and not p1.animation in [ATTACK_ONE, ATTACK_TWO]:
            p1.animate(2, ATTACK_TWO, False)
            Martials.Bullet(1, game.p1.fighter, game.p2.fighter)
            p1.t2 = 0
        blit_image(surface, ['Background', bkgrnd+'.png'], "topleft", (0,0), (int(SIZE[0]), int(SIZE[1]*0.8)))
        p1.update(p2)
        p1_surface = p1.draw()
        p2.update(p1)
        p2_surface = p2.draw()

        surface.blit(p1_surface, p1.rect)
        surface.blit(p2_surface, p2.rect)
        for i in Martials.Bullet.bullets:
            i.update()
            i.draw(surface)
        update_UI(surface, game)


        pygame.display.flip()
        if quit:
            break

        if game.p1.consciousness<=0:
            game.winner = game.p2

            quit, home = game_end(surface, game, keys)
        if game.p2.consciousness<=0:
            game.winner = game.p1
            quit, home = game_end(surface, game, keys)
        if pause:
            quit, home = pause_menu(surface, keys)
            clock.tick()
        else:
            game.fight_time-=clock.get_time()/1000
        if quit or home:
            break
        if game.fight_timetime<=0:
            game.fight_time = 30
            break
        pygame.display.flip()
    music.stop()
    return quit, home
def update_UI(surface, game):
    pygame.draw.rect(surface, PURPLE, pygame.Rect(SIZE[0]*0.4, -5, SIZE[0]/5, SIZE[1]*0.1), 5)
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render(f"Round {str(game.round)}", True, PURPLE, BLACK)
    textRect = text.get_rect()
    textRect.midtop = (SIZE[0]/2, 5)
    surface.blit(text, textRect)
    text = font.render(f"Time left: {str(int(game.fight_time))}", True, PURPLE, BLACK)
    textRect = text.get_rect()
    textRect.midbottom = (SIZE[0]/2, SIZE[1]*0.09)
    surface.blit(text, textRect)
    pygame.draw.rect(surface, BLUE, pygame.Rect(0, SIZE[1]*0.8, SIZE[0]/2-5, SIZE[1]*0.2))
    pygame.draw.rect(surface, RED, pygame.Rect(SIZE[0]/2+5, SIZE[1]*0.8, SIZE[0]/2-5, SIZE[1]*0.2))
    pygame.draw.rect(surface, GREY, pygame.Rect(SIZE[0]/2-5, SIZE[1]*0.8, 10, SIZE[1]*0.2))
    size = (100, 100)
    blit_image(surface, ['Martial Hero', 'Sprites', 'Head.png'], "topleft", (10, SIZE[1]*0.82), size)
    blit_image(surface, ['Martial Hero 2', 'Sprites', 'Head.png'], "topleft", (SIZE[0]/2+15, SIZE[1]*0.82), size)
    temp = show_con(game.p1, BLUE)
    surface.blit(temp, pygame.Rect(5, 0.95*SIZE[1], temp.get_width(), temp.get_height()))
    temp = show_con(game.p2, RED)
    surface.blit(show_cd(game.p1, BLUE), (SIZE[0]*0.08, SIZE[1]*0.82))
    surface.blit(show_cd(game.p2, RED), (SIZE[0]*0.58+5, SIZE[1]*0.82))
    surface.blit(temp, pygame.Rect(SIZE[0]/2+10, 0.95*SIZE[1], temp.get_width(), temp.get_height()))
def blit_image(surface, path, anchor, pos, size = None):
    image = pygame.image.load(convertpath.path(path)).convert()
    if size:
        image = pygame.transform.scale(image, size)
    image.set_colorkey(image.get_at((0,0)))
#     image.set_colorkey(BLACK)
    rect = image.get_rect()
    if anchor == "center":
        rect.center = pos
    elif anchor == "topleft":
        rect.topleft = pos
    surface.blit(image, rect)
def game_end(surface, game, keys):
    game.finished = True
    font = pygame.font.Font('freesansbold.ttf', 50)
    rect = pygame.Rect(0, 0, SIZE[0]*0.6, SIZE[1]*0.2)
    rect.center = (SIZE[0]/2, SIZE[1]/2)
    pygame.draw.rect(surface, BLACK, rect)
    if game.winner == game.p1:
        pygame.draw.rect(surface, BLUE, rect, 5)
        text = font.render("Player 1 Won", True, BLUE, BLACK)
    elif game.winner == game.p2:
        pygame.draw.rect(surface, RED, rect, 5)
        text = font.render("Player 2 Won", True, RED, BLACK)
    else:
        text = font.render("Tie", True, PURPLE, BLACK)
    textRect = text.get_rect()
    textRect.center = (SIZE[0]/2, SIZE[1]/2)
    surface.blit(text, textRect)
    for i in Model.Button.end:
        surface.blit(i.surface, i.rect)
    pygame.display.flip()
    home = False
    while True:
        quit, button = Controller.game_end(keys)
        if quit or button == 'home':
            home = button=='home'

            break
    return quit, home
def show_con(player, color):

    surface = pygame.Surface((SIZE[0]*0.4, (SIZE[1]*0.1)))
    surface.fill(color)
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render("Consciousness", True, WHITE, color)
    textRect = text.get_rect()
    textRect.topleft = (5, 5)
    surface.blit(text, textRect)
    pygame.draw.rect(surface, BLACK, pygame.Rect(5, 30, surface.get_width()*0.9, 10))
    text = font.render(str(player.consciousness) if player.consciousness>=0 else '0', True, WHITE, color)
    textRect = text.get_rect()
    textRect.topleft = (surface.get_width()*0.9, 5)
    surface.blit(text, textRect)
    if player.consciousness>0:
        pygame.draw.rect(surface, WHITE, pygame.Rect(7, 32, surface.get_width()*0.9*player.consciousness/100-4, 6))
    return surface
def show_cd(player, color):

    surface = pygame.Surface((SIZE[0]*0.4, (SIZE[1]*0.1)))
    surface.fill(color)
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render("Attack 1 cooldown", True, WHITE, color)
    textRect = text.get_rect()
    textRect.topleft = (5, 5)
    surface.blit(text, textRect)
    pygame.draw.rect(surface, BLACK, pygame.Rect(5, 30, surface.get_width()*0.4, 10))

    pygame.draw.rect(surface, WHITE, pygame.Rect(7, 32, surface.get_width()*0.4*player.fighter.t1/player.fighter.cd1-4, 6))

    text = font.render("Attack 2 cooldown", True, WHITE, color)
    textRect = text.get_rect()
    textRect.topleft = (surface.get_width()*0.41+5, 5)
    surface.blit(text, textRect)
    pygame.draw.rect(surface, BLACK, pygame.Rect(surface.get_width()*0.41+5, 30, surface.get_width()*0.4, 10))

    pygame.draw.rect(surface, WHITE, pygame.Rect(surface.get_width()*0.41+5, 32, surface.get_width()*0.4*player.fighter.t2/player.fighter.cd2-4, 6))
    return surface
if __name__ == "__main__":
    main.main()