import pygame, os, scenes, Model, fight, Martials, UI, pickle, Controller
from time import sleep
from pygame.locals import *
import sys
global window_size_x, window_size_y
from Model import Button
window_size_y = 830
window_size_x = int(window_size_y*1.7)
SIZE = (window_size_x, window_size_y)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
PURPLE = (255, 0, 255)

def main():
    pygame.init()

    surface = pygame.display.set_mode([window_size_x,window_size_y])
    pygame.display.set_caption('Martial Chess')
    clock = pygame.time.Clock()

    quit = False
    try:
        with open("Controls.dat", "rb") as f:
            keys = pickle.load(f)
    except FileNotFoundError:
        keys = Model.Settings()
        with open("Controls.dat", "wb") as f:
            pickle.dump(keys, f)

    rect = pygame.Rect(0, 0, SIZE[0]*0.2, SIZE[1]/5)
    rect.midtop = (SIZE[0]/2, SIZE[1]/6)
    for text, name in [('Play', 'start'), ('Help', 'help'), ('Settings', 'settings'), ('Quit', 'quit')]:
        Button(rect.copy(), text, BLACK, name, PURPLE, Button.main_menu, (PURPLE, 5))
        rect.centery += SIZE[1]/6
    rect = pygame.Rect(0, 0, SIZE[0]*0.2, SIZE[1]/10)
    rect.midtop = (SIZE[0]/4, SIZE[1]/6)

    for text, name in [(f'Attack 1: {pygame.key.name(keys.p1_attack1) if keys.p1_attack1 else "Unbound"}', 'p1_attack1'),
                        (f'Attack 2: {pygame.key.name(keys.p1_attack2) if keys.p1_attack2 else "Unbound"}', 'p1_attack2'),
                        (f'Jump: {pygame.key.name(keys.p1_jump) if keys.p1_jump else "Unbound"}', 'p1_jump'),
                        (f'Move Left: {pygame.key.name(keys.p1_left) if keys.p1_left else "Unbound"}', 'p1_left'),
                        (f'Move Right: {pygame.key.name(keys.p1_right) if keys.p1_right else "Unbound"}', 'p1_right')]:
        Button(rect.copy(), text, BLACK, name, BLUE, Button.settings, (BLUE, 5))
        rect.centery += SIZE[1]/6

    rect = pygame.Rect(0, 0, SIZE[0]*0.2, SIZE[1]/10)
    rect.midtop = (SIZE[0]/2, SIZE[1]/6)

    for text, name in [(f'Attack 1: {pygame.key.name(keys.p2_attack1) if keys.p2_attack1 else "Unbound"}', 'p2_attack1'),
                        (f'Attack 2: {pygame.key.name(keys.p2_attack2) if keys.p2_attack2 else "Unbound"}', 'p2_attack2'),
                        (f'Jump: {pygame.key.name(keys.p2_jump) if keys.p2_jump else "Unbound"}', 'p2_jump'),
                        (f'Move Left: {pygame.key.name(keys.p2_left) if keys.p2_left else "Unbound"}', 'p2_left'),
                        (f'Move Right: {pygame.key.name(keys.p2_right) if keys.p2_right else "Unbound"}', 'p2_right')]:
        Button(rect.copy(), text, BLACK, name, RED, Button.settings, (RED, 5))
        rect.centery += SIZE[1]/6

    rect = pygame.Rect(0, 0, SIZE[0]*0.2, SIZE[1]/10)
    rect.midtop = (SIZE[0]*3/4, SIZE[1]/6)

    for text, name in [(f'Quit: {pygame.key.name(keys.quit) if keys.quit else "Unbound"}', 'quit'),
                        (f'Pause: {pygame.key.name(keys.pause) if keys.pause else "Unbound"}', 'pause')]:
        Button(rect.copy(), text, BLACK, name, PURPLE, Button.settings, (PURPLE, 5))
        rect.centery += SIZE[1]/6

    rect = pygame.Rect(0, 0, SIZE[0]/8, SIZE[1]/10)
    rect.midtop = (SIZE[0]/2, SIZE[1]/3)

    for text, name in [('Unpause', 'unpause'), ('Settings', 'settings'), ('Home', 'home'), ('Quit', 'quit')]:
        Button(rect.copy(), text, BLACK, name, PURPLE, Button.pause, (PURPLE, 5))
        rect.centery += SIZE[1]/10

    Button(pygame.Rect(10, 10, SIZE[0]*0.1, SIZE[1]/10), 'Back', BLACK, 'back', PURPLE, Button.settings, (PURPLE, 5))
    Button(pygame.Rect(10, 10, SIZE[0]*0.1, SIZE[1]/10), 'Back', BLACK, 'back', PURPLE, Button.help_menu, (PURPLE, 5))
    Button(pygame.Rect(10, 10, SIZE[0]*0.1, SIZE[1]/10), 'Back', BLACK, 'back', PURPLE, Button.choose, (PURPLE, 5))

    rect = pygame.Rect(0, 0, SIZE[0]/8, SIZE[1]/10)
    rect.midtop = (SIZE[0]/2, SIZE[1]/3)

    for text, name in [('New Game', 'new'), ('Continue Game', 'continue')]:
        Button(rect.copy(), text, BLACK, name, PURPLE, Button.choose, (PURPLE, 5))
        rect.centery += SIZE[1]/10
    Button(pygame.Rect(SIZE[0]/2-SIZE[0]*0.05, SIZE[1]*0.62, SIZE[0]*0.1, SIZE[1]/10), 'Home', BLACK, 'home', PURPLE, Button.end, (PURPLE, 5))
    Button(pygame.Rect(SIZE[0]/2-SIZE[0]*0.025, SIZE[1]*0.54, SIZE[0]*0.05, SIZE[1]/20), 'Hide', BLACK, 'hide', PURPLE, Button.end, (PURPLE, 5))
    click = False
    while True:
        try:
            with open("save.dat", "rb") as f:
                saved = pickle.load(f)
                if saved.finished:
                    saved = None
        except FileNotFoundError:
            saved = None
        home = False
        quit, save = UI.main_menu(surface, clock, keys, saved)
        if save == None:
            continue
        if save:
            game = saved
            game.p1.fighter = Martials.Blue(['Martial Hero', 'Sprites'], 10, window_size_y, game.p1)
            game.p2.fighter = Martials.Red(['Martial Hero 2', 'Sprites'], window_size_x-30, window_size_y, game.p2)
        else:
            game = Model.Game()
            game.p1.fighter = Martials.Blue(['Martial Hero', 'Sprites'], 10, window_size_y, game.p1)
            game.p2.fighter = Martials.Red(['Martial Hero 2', 'Sprites'], window_size_x-30, window_size_y, game.p2)
        if quit:
            break
        click = True
        clock.tick()
        while True:
            game.p1.update_time()
            game.p2.update_time()
#             game.round =2
            quit = scenes.countdown(surface, game, clock, keys)
            if quit:
                break
            if game.round%2==1:
                quit, home = scenes.game_chess(surface, game, clock, keys)
                if quit or home:
                    break
            else:
                for i in Martials.Bullet.bullets:
                    del i
                Martials.Bullet.bullets.clear()
                game.p1.fighter.x, game.p1.fighter.y = 10, window_size_y
                game.p2.fighter.x, game.p2.fighter.y = window_size_x-30, window_size_y
                quit, home = fight.game_fight(surface, game, clock, keys)
                if quit or home:
                    break
            game.round+=1
            if game.round == 10:
                break
        if click:
            game.p1.fighter=None
            game.p2.fighter=None
            with open("save.dat", 'wb') as f:
                pickle.dump(game, f)

        if home:
            continue
        if not quit:
            if game.p2.consciousness>game.p1.consciousness:
                game.winner = game.p2
            elif game.p1.consciousness>game.p2.consciousness:
                game.winner = game.p1
            else:
                game.winner = game.p2
            surface.fill(BLACK)

            quit, home = game_end(surface, game, keys)
        if home:
            continue
        if quit:
            break
    with open("Controls.dat", "wb") as f:
        pickle.dump(keys, f)

    pygame.quit()
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

if __name__ == "__main__":
    main()