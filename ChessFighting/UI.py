import pygame, main, Controller, convertpath, Model, Martials
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
            quit = help_menu(surface, keys)
        elif button == 'settings':
            quit = settings(surface, keys)
        if quit:
            break
        pygame.display.flip()
    return quit
def help_menu(surface, keys):
    while True:
        quit, button, direction = Controller.help_menu(keys)
        surface.fill(BLACK)
        rect = pygame.Rect(SIZE[0]/4, 0, SIZE[0]/2, SIZE[1])
        text = f'''
    • Each game has 9 rounds total, each round alternates between chess and martial arts
    • Each player has an attribute called consciousness. The lower a player's consciousness, the less time the player can think for each move in chess
    • A player loses if they get checkmated, consciousness reaches 0, or they run out of time in chess
    • If a stalemate occurs or all 9 rounds finish, then whoever has more consciousness wins. If both players have the same amount of consciousness, player 2 wins.
    • Martial arts description: Attack 1 is a melee attack that deals {str(Martials.Blue.damage_1)} damage. Attack 2 is a long range attack that deals {str(Martials.Blue.damage_2)} damage. You can change controls in the settings menu'''
        text_surface = word_wrap(rect, pygame.font.Font('freesansbold.ttf', 30), WHITE, text)
        for i in Button.help_menu:
            surface.blit(i.surface, i.rect)
        surface.blit(text_surface, rect)
        if quit or button == 'back':
            break
        pygame.display.flip()
    return quit


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
def word_wrap(rect, font, color, text):
    ''' Wrap the text into the space of the rect, using the font object provided.
        Returns a surface of rect size with the text rendered in it.
    '''
    linesize = font.get_linesize()
    words = text.split(' ')
    width, height = rect.size
    lines = []
    line = ''
    length = 0
    surface = pygame.Surface((width, height))

    for word in words:
        if '\n' in word:
            index = word.index('\n')
            if length+font.size(word[:index])[0] > width-1:

                lines.append(line)
                line = word[:index]
                lines.append(line)

            else:

                line += word[:index]
                lines.append(line)

            length = font.size(word[index+2:]+' ')[0]

            line = word[index+1:] + ' '
        elif length+font.size(word)[0] < width-1:
            length += font.size(word+' ')[0]
            line += word+' '


        else:
            line = line[:-1]

            lines.append(line)

            length = font.size(word+' ')[0]

            line = word+' '

    line = line[:-1]
    lines.append(line)
    y = 0
    for line in lines:
        if line.startswith(' '):
            y+=linesize
        font_obj = font.render(line, True, color)
        surface.blit(font_obj, pygame.Rect(0, y, width, y+linesize))
        y += linesize

    surface.set_colorkey((0,0,0))
    return surface
if __name__ == '__main__':
    main.main()