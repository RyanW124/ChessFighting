import Chess, pygame, Controller, main, Model, convertpath

SIZE = None
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
PURPLE = (255, 0, 255)
r_value = 150
BROWN = (r_value, r_value/2, 0)
def game_chess(surface : pygame.Surface, game, clock, keys):
    global SIZE
    SIZE = (main.window_size_x, main.window_size_y)
    quit = False
    selected = None
    board_rect = pygame.Rect(SIZE[0]*0.1, SIZE[1]*0.25, SIZE[0]*0.3, SIZE[0]*0.3)
    board_rect2 = board_rect.copy()
    board_rect2.left+= SIZE[0]/2+5
    time = main.chess_time
    while True:
        clock.tick(30)
        quit, selected = Controller.chess(board_rect, board_rect2, game, selected, keys)

        if quit:
            break
        chess_update(surface, game, selected, board_rect, board_rect2, time)
        time-=clock.get_time()/1000
        if game.board.turn:
            game.p1.time-=clock.get_time()/1000
            game.p1.move_time-=clock.get_time()/1000
            if game.p1.time<=0 or game.p1.move_time<=0:
                game.winner = game.p2

        else:
            game.p2.move_time-=clock.get_time()/1000
            game.p2.time-=clock.get_time()/1000
            if game.p1.time<=0 or game.p2.move_time<=0:
                game.winner = game.p1
        if time <= 0:
            break
        pygame.display.flip()
        if game.winner:
            quit = game_end(surface, game, keys)
            if quit:
                break
    return quit
def game_end(surface, game, keys):
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
    pygame.display.flip()
    while True:
        quit = Controller.game_end(keys)
        if quit:
            break
    return quit
def chess_update(surface : pygame.Surface, game, selected, b, b2, time):

    board_rect = b.copy()
    board_rect2 = b2.copy()
    surface.fill(BLACK)
    pygame.draw.rect(surface, BLUE, pygame.Rect(0, 0.85*SIZE[1], SIZE[0]/2, 0.15*SIZE[1]))
    temp = show_con(game.p1, BLUE)
    surface.blit(temp, pygame.Rect(5, 0.85*SIZE[1]+5, temp.get_width(), temp.get_height()))
    pygame.draw.rect(surface, RED, pygame.Rect(SIZE[0]/2, 0.85*SIZE[1], SIZE[0]/2, 0.15*SIZE[1]))
    temp = show_con(game.p2, RED)
    surface.blit(temp, pygame.Rect(10+SIZE[0]/2, 0.85*SIZE[1]+5, temp.get_width(), temp.get_height()))
    pygame.draw.rect(surface, GREY, pygame.Rect(SIZE[0]/2-5, 0, 10, SIZE[1]))
    pygame.draw.polygon(surface, BLUE, [(0, 50), (200, 50), (130, 100), (175, 75), (100, 150), (0, 150)])
    pygame.draw.polygon(surface, RED, [(SIZE[0]/2+5, 50), (200+SIZE[0]/2+5, 50), (130+SIZE[0]/2+5, 100), (175+SIZE[0]/2+5, 75), (100+SIZE[0]/2+5, 150), (SIZE[0]/2+5, 150)])

    size = (100, 100)
    blit_image(surface, ['Martial Hero', 'Sprites', 'Head.png'], "topleft", (10, 151-size[1]), size)
    blit_image(surface, ['Martial Hero 2', 'Sprites', 'Head.png'], "topleft", (SIZE[0]/2+15, 151-size[1]), size)
    font = pygame.font.Font('freesansbold.ttf', 20)

    text = font.render(f"Total Time left: {str(int(game.p1.time//60))}m {str(int(game.p1.time%60))}s ", True, WHITE, BLUE)
    textRect = text.get_rect()
    textRect.bottomleft = (5, SIZE[1]-5)
    te = textRect.right
    surface.blit(text, textRect)
    text = font.render(f"Time left for this move: {str(int(game.p1.move_time))}s ", True, WHITE, BLUE)
    textRect = text.get_rect()
    textRect.bottomleft = (te+30, SIZE[1]-5)
    surface.blit(text, textRect)

    text = font.render(f"Total Time left: {str(int(game.p2.time//60))}m {str(int(game.p2.time%60))}s ", True, WHITE, RED)
    textRect = text.get_rect()
    textRect.bottomleft = (10+SIZE[0]/2, SIZE[1]-5)
    surface.blit(text, textRect)
    te = textRect.right
    text = font.render(f"Time left for this move: {str(int(game.p2.move_time))}s ", True, WHITE, RED)
    textRect = text.get_rect()
    textRect.bottomleft = (te+30, SIZE[1]-5)
    surface.blit(text, textRect)

    pygame.draw.rect(surface, BLACK, pygame.Rect(SIZE[0]*0.42, SIZE[1]*0.45, SIZE[0]*0.16, SIZE[1]*0.1))
    pygame.draw.rect(surface, PURPLE, pygame.Rect(SIZE[0]*0.42, SIZE[1]*0.45, SIZE[0]*0.16, SIZE[1]*0.1), 5)

    text = font.render(f"Round {game.round}", True, PURPLE, BLACK)
    textRect = text.get_rect()
    textRect.midtop = (SIZE[0]/2, SIZE[1]*0.47)
    surface.blit(text, textRect)

    text = font.render(f"Time left: {int(time)}s", True, PURPLE, BLACK)
    textRect = text.get_rect()
    textRect.midbottom = (SIZE[0]/2, SIZE[1]*0.53)
    surface.blit(text, textRect)

    pygame.draw.rect(surface, WHITE, board_rect)
    pygame.draw.rect(surface, WHITE, board_rect2)
    alp = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    board = game.board
    if board.turn:
        text = font.render("It is your turn...", True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.midleft = (200, 125)
        surface.blit(text, textRect)
        text = font.render("Waiting for player 1 to make a move...", True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.midleft = (205+SIZE[0]/2, 125)
        surface.blit(text, textRect)
    else:
        text = font.render("Waiting for player 2 to make a move...", True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.midleft = (200, 125)
        surface.blit(text, textRect)
        text = font.render("It is your turn...", True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.midleft = (205+SIZE[0]/2, 125)
        surface.blit(text, textRect)
    square_rect = pygame.Rect(0, 0, board_rect.width/8, board_rect.height/8)
    for r in range(8):
        for c in range(8):
            if (r+c)%2 == 1:
                square_rect.topleft = (board_rect.left+r*board_rect.width/8, board_rect.top+c*board_rect.height/8)
                pygame.draw.rect(surface, BROWN, square_rect)
                square_rect.topleft = (board_rect2.left+r*board_rect2.width/8, board_rect2.top+c*board_rect2.height/8)
                pygame.draw.rect(surface, BROWN, square_rect)
    for r in range(8):
        for c in range(8):
            if board.piece_type_at(63-r*8-c):
                if board.piece_at(63-r*8-c).color:
                    t = "white"
                else:
                    t = "black"
                if (r+c) %2==0:
                    tex = 'b'
                    tex2 = 'b'
                else:
                    tex = 'w'
                    tex2 = 'w'
                if board.turn:


                    if 63-r*8-c == selected:
                        blit_chess(surface, ['Chess Sprites', f'{t}_{Chess.piece_name(board.piece_type_at(63-r*8-c))}{tex}.png'], "center",
                        (board_rect.left+(7-c+0.5)*board_rect.width/8, board_rect.top+(r+0.5)*board_rect.height/8),
                        (int(board_rect.width/8*0.9), int(board_rect.height/8*0.9)))
                    else:
                        blit_chess(surface, ['Chess Sprites', f'{t}_{Chess.piece_name(board.piece_type_at(63-r*8-c))}{tex}.png'], "center",
                        (board_rect.left+(7-c+0.5)*board_rect.width/8, board_rect.top+(r+0.5)*board_rect.height/8),
                        (int(board_rect.width/8*0.6), int(board_rect.height/8*0.6)))
                    blit_chess(surface, ['Chess Sprites', f'{t}_{Chess.piece_name(board.piece_type_at(63-r*8-c))}{tex2}.png'], "center",
                    (board_rect2.left+(c+0.5)*board_rect2.width/8, board_rect2.top+(7-r+0.5)*board_rect.height/8),
                    (int(board_rect2.width/8*0.6), int(board_rect2.height/8*0.6)))
                else:
                    if 63-r*8-c == selected:
                        blit_chess(surface, ['Chess Sprites', f'{t}_{Chess.piece_name(board.piece_type_at(63-r*8-c))}{tex2}.png'], "center",
                        (board_rect2.left+(c+0.5)*board_rect2.width/8, board_rect2.top+(7-r+0.5)*board_rect.height/8),
                        (int(board_rect2.width/8*0.9), int(board_rect2.height/8*0.9)))
                    else:
                        blit_chess(surface, ['Chess Sprites', f'{t}_{Chess.piece_name(board.piece_type_at(63-r*8-c))}{tex2}.png'], "center",
                        (board_rect2.left+(c+0.5)*board_rect2.width/8, board_rect2.top+(7-r+0.5)*board_rect.height/8),
                        (int(board_rect2.width/8*0.6), int(board_rect2.height/8*0.6)))
                    blit_chess(surface, ['Chess Sprites', f'{t}_{Chess.piece_name(board.piece_type_at(63-r*8-c))}{tex}.png'], "center",
                    (board_rect.left+(7-c+0.5)*board_rect.width/8, board_rect.top+(r+0.5)*board_rect.height/8),
                    (int(board_rect.width/8*0.6), int(board_rect.height/8*0.6)))
    for i in range(9):

        if i!=8:
            text = font.render(str(8-i), True, WHITE, BLACK)
            textRect = text.get_rect()
            textRect.midright = (board_rect.left-5, board_rect.top+board_rect.height/8*(i+0.5))
            surface.blit(text, textRect)
            textRect.midright = (board_rect2.left-5, board_rect2.bottom - board_rect2.height/8*(i+0.5))
            surface.blit(text, textRect)

            text = font.render(alp[i], True, WHITE, BLACK)
            textRect = text.get_rect()
            textRect.midtop = (board_rect.left+board_rect.width/8*(i+0.5), board_rect.bottom+5)
            surface.blit(text, textRect)
            textRect.midtop = (board_rect2.right-board_rect2.width/8*(i+0.5), board_rect2.bottom+5)
            surface.blit(text, textRect)

        pygame.draw.line(surface, BLACK, (board_rect.left+i*board_rect.width/8, board_rect.top), (board_rect.left+i*board_rect.width/8, board_rect.bottom), 3)
        pygame.draw.line(surface, BLACK, (board_rect2.left+i*board_rect2.width/8, board_rect2.top), (board_rect2.left+i*board_rect2.width/8, board_rect2.bottom), 3)

        pygame.draw.line(surface, BLACK, (board_rect.left, board_rect.top+i*board_rect.height/8), (board_rect.right, board_rect.top+i*board_rect.height/8), 3)
        pygame.draw.line(surface, BLACK, (board_rect2.left, board_rect2.top+i*board_rect2.height/8), (board_rect2.right, board_rect2.top+i*board_rect2.height/8), 3)

def show_con(player, color):

    surface = pygame.Surface((SIZE[0]*0.4, (SIZE[1]*0.1)))
    surface.fill(color)
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render("Consciousness", True, WHITE, color)
    textRect = text.get_rect()
    textRect.topleft = (5, 5)
    surface.blit(text, textRect)
    pygame.draw.rect(surface, BLACK, pygame.Rect(5, 30, surface.get_width()*0.9, 10))
    pygame.draw.rect(surface, WHITE, pygame.Rect(7, 32, surface.get_width()*0.9*player.consciousness/100-4, 6))
    text = font.render(str(player.consciousness), True, WHITE, color)
    textRect = text.get_rect()
    textRect.topleft = (surface.get_width()*0.9, 5)
    surface.blit(text, textRect)
    return surface
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

def blit_chess(surface, path, anchor, pos, size = None):
    image = pygame.image.load(convertpath.path(path)).convert()
    if size:
        image = pygame.transform.scale(image, size)

    rect = image.get_rect()
    if anchor == "center":
        rect.center = pos
    elif anchor == "topleft":
        rect.topleft = pos
    surface.blit(image, rect)
def countdown(surface, game, clock, keys):
    global SIZE
    SIZE = (main.window_size_x, main.window_size_y)
    time = 3
    font = pygame.font.Font('freesansbold.ttf', 200)
    while True:
        clock.tick(10)
        surface.fill(BLACK)
        time -= clock.get_time()/1000
        quit = Controller.count(keys)
        if quit:
            break
        te = None
        if time>0:
            text = font.render(str(int(time)+1), True, WHITE, BLACK)
            textRect = text.get_rect()
            textRect.center = (SIZE[0]/2, SIZE[1]/2)
            surface.blit(text, textRect)
            te = textRect.bottom

        else:
            text = font.render("GO!", True, WHITE, BLACK)
            textRect = text.get_rect()
            textRect.center = (SIZE[0]/2, SIZE[1]/2)
            surface.blit(text, textRect)
            te = textRect.bottom
        secondfont = pygame.font.Font('freesansbold.ttf', 50)
        if game.round%2 == 0:
            text = "Martial Arts"
        else:
            text = "Chess"
        text = secondfont.render(f"Round {str(game.round)}: {text}", True, WHITE, BLACK)
        textRect = text.get_rect()
        textRect.midtop = (SIZE[0]/2, te+10)
        surface.blit(text, textRect)
        if time<=-1:
            break
        pygame.display.flip()
    return quit

if __name__ == "__main__":
		main.main()