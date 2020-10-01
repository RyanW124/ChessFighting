import pygame, main, Controller, convertpath
from Model import Button

SIZE = None
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
PURPLE = (255, 0, 255)
def main_menu(surface, clock, keys):
    global SIZE
    SIZE = (main.window_size_x, main.window_size_y)

    while True:
        surface.fill(BLACK)
        quit, button = Controller.main_menu(keys)
        draw_background(surface, 50, 20, 10)
        for i in Button.main_menu:
            surface.blit(i.surface, i.rect)
        if button == 'start':
           break
        elif button == 'quit':
            quit = True
        elif button == 'help':
            quit = help_menu(surface)
        elif button == 'settings':
            quit = settings(surface, keys)
        if quit:
            break
        pygame.display.flip()
    return quit
def help():
    pass

def settings(surface, keys):

    changing = None
    ori_text = None
    while True:
        surface.fill(BLACK)
        quit, button, key = Controller.settings(keys)
        if button == 'back':
            if changing:
                Button.get_button(Button.settings, changing).text = ori_text
                Button.get_button(Button.settings, changing).update()
            break
        for i in Button.settings:
            surface.blit(i.surface, i.rect)
        font = pygame.font.Font('freesansbold.ttf', 50)
        text = font.render(f"Player 1", True, BLUE, BLACK)
        textRect = text.get_rect()
        textRect.midbottom = (SIZE[0]/4, 110)
        surface.blit(text, textRect)
        text = font.render(f"Player 2", True, RED, BLACK)
        textRect = text.get_rect()
        textRect.midbottom = (SIZE[0]/2, 110)
        surface.blit(text, textRect)
        text = font.render(f"Others", True, PURPLE, BLACK)
        textRect = text.get_rect()
        textRect.midbottom = (SIZE[0]*3/4, 110)
        surface.blit(text, textRect)
        if button == False and changing:
            Button.get_button(Button.settings, changing).text = ori_text
            Button.get_button(Button.settings, changing).update()
            changing = None
        if changing and key:
            Button.get_button(Button.settings, changing).text += pygame.key.name(key.key)
            Button.get_button(Button.settings, changing).update()

            t = None
            for i in keys:
                if i == key.key:
                    if i == keys.p1_attack1:
                        t = 'p1_attack1'
                        keys.p1_attack1 = None
                        if t == changing:
                            break
                    elif i == keys.p1_attack2:
                        t = 'p1_attack2'
                        keys.p1_attack2 = None
                        if t == changing:
                            break
                    elif i == keys.p1_left:
                        t = 'p1_left'
                        keys.p1_left = None
                        if t == changing:
                            break
                    elif i == keys.p1_right:
                        t = 'p1_right'
                        keys.p1_right = None
                        if t == changing:
                            break
                    elif i == keys.p1_jump:
                        t = 'p1_jump'
                        keys.p1_jump = None
                        if t == changing:
                            break
                    elif i == keys.p2_attack1:
                        t = 'p2_attack1'
                        keys.p2_attack1 = None
                        if t == changing:
                            break
                    elif i == keys.p2_attack2:
                        t = 'p2_attack2'
                        keys.p2_attack2 = None
                        if t == changing:
                            break
                    elif i == keys.p2_left:
                        t = 'p2_left'
                        keys.p2_left = None
                        if t == changing:
                            break
                    elif i == keys.p2_right:
                        t = 'p2_right'
                        keys.p2_right = None
                        if t == changing:
                            break
                    elif i == keys.p2_jump:
                        t = 'p2_jump'
                        keys.p2_jump = None
                        if t == changing:
                            break
                    elif i == keys.quit:
                        t = 'quit'
                        keys.quit = None
                        if t == changing:
                            break
                    elif i == keys.pause:
                        t = 'pause'
                        keys.pause = None
                        if t == changing:
                            break
                    Button.get_button(Button.settings, t).text = Button.get_button(Button.settings, t).text[:Button.get_button(Button.settings, t).text.index(':')+2]+'Unbound'
                    Button.get_button(Button.settings, t).update()
            if changing == 'p1_attack1':
                keys.p1_attack1 = key.key
            elif changing == 'p1_attack2':
                keys.p1_attack2 = key.key
            elif changing == 'p1_left':
                keys.p1_left = key.key
            elif changing == 'p1_right':
                keys.p1_right = key.key
            elif changing == 'p1_jump':
                keys.p1_jump = key.key
            elif changing == 'p2_attack1':
                keys.p2_attack1 = key.key
            elif changing == 'p2_attack2':
                keys.p2_attack2 = key.key
            elif changing == 'p2_left':
                keys.p2_left = key.key
            elif changing == 'p2_right':
                keys.p2_right = key.key
            elif changing == 'p2_jump':
                keys.p2_jump = key.key
            elif changing == 'quit':
                keys.quit = key.key
            elif changing == 'pause':
                keys.pause = key.key

            changing = None

        if button and button!=changing:
            b = Button.get_button(Button.settings, button)
            if changing:
                Button.get_button(Button.settings, changing).text = ori_text
                Button.get_button(Button.settings, changing).update()

            ori_text = b.text
            b.text = b.text[:b.text.index(':')+2]
            b.update()

            changing = button

        if quit:
            break
        pygame.display.flip()
    return quit

def draw_background(surface, amp, w, rep):
    pos = [(SIZE[0]/2-amp-w if x%2==0 else SIZE[0]/2+amp, x*SIZE[1]/(rep-1)) for x in range(rep)]
    pos2 = [(x[0]+w, x[1]) for x in pos]
    pygame.draw.polygon(surface, WHITE, pos+list(reversed(pos2)))
    pygame.draw.polygon(surface, BLUE, [(0,0)]+pos+[(0, SIZE[1])])
    pygame.draw.polygon(surface, RED, [(SIZE[0],0)]+pos2+[(SIZE[0], SIZE[1])])
    blit_image(surface, ['Martial Hero', 'Sprites', 'Head.png'], "midbottom", (SIZE[0]/4, SIZE[1]), (int(SIZE[0]*0.4), int(SIZE[0]*0.4)))
    blit_image(surface, ['Martial Hero 2', 'Sprites', 'Head.png'], "midbottom", (SIZE[0]*0.8, SIZE[1]), (int(SIZE[0]*0.4), int(SIZE[0]*0.4)), True)
def blit_image(surface, path, anchor, pos, size = None, flip = False):
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
    elif anchor == "midbottom":
        rect.midbottom = pos
    if flip:
        image = pygame.transform.flip(image, True, False)
    surface.blit(image, rect)
if __name__ == '__main__':
    main.main()