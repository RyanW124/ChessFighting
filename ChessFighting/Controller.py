import pygame, main, Chess
from string import ascii_lowercase




def fight1(game, p1_left, p1_right, p1j, p2_left, p2_right, p2j):
    quit = False
    shoot = False
    pl = p1_left
    pr = p1_right
    p1_jump = p1j
    shoot2 = False
    s1 = False
    s2 = False
    pl2 = p2_left
    pr2 = p2_right
    p2_jump = p2j
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                shoot2 = True
            if event.key == pygame.K_x:
                s2 = True
            if event.key == pygame.K_LEFT:
                pl2 = True
            if event.key == pygame.K_RIGHT:
                pr2 = True
            if event.key == pygame.K_UP:
                p2_jump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                pl2 = False
            if event.key == pygame.K_RIGHT:
                pr2 = False
            if event.key == pygame.K_UP:
                p2_jump = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit = True
            if event.key == pygame.K_ESCAPE:
                quit = True
            if event.key == pygame.K_y:
                s1 = True
            if event.key == pygame.K_t:
                shoot = True
            if event.key == pygame.K_a:
                pl = True
            if event.key == pygame.K_d:
                pr = True
            if event.key == pygame.K_w:
                p1_jump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                pl = False
            if event.key == pygame.K_d:
                pr = False
            if event.key == pygame.K_w:
                p1_jump = False


    return quit, shoot, pl, pr, p1_jump, shoot2, pl2, pr2, p2_jump, s1, s2
def count():
    quit = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit = True
            if event.key == pygame.K_ESCAPE:
                quit = True
    return quit
def game_end():
    quit = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit = True
            if event.key == pygame.K_ESCAPE:
                quit = True
    return quit
def chess(b, b2, game, sq):
    square = sq
    quit = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit = True
            if event.key == pygame.K_ESCAPE:
                quit = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                move_made = False
                if b.collidepoint(event.pos) and game.board.turn:
                    square = ((event.pos[0]-b.left)*8//b.width)+(7-((event.pos[1]-b.top)*8//b.height))*8
                    if game.board.piece_at(square):
                        if not game.board.piece_at(square).color:
                            if sq:
                                move = ascii_lowercase[sq%8] + str(sq//8+1) + ascii_lowercase[square%8] + str(square//8+1)
                                if Chess.Move.from_uci(move) in game.board.legal_moves:
                                    game.board.push(Chess.Move.from_uci(move))
                                    move_made = True
                            square = None

                    else:
                        if sq:
                            move = ascii_lowercase[sq%8] + str(sq//8+1) + ascii_lowercase[square%8] + str(square//8+1)
                            if Chess.Move.from_uci(move) in game.board.legal_moves:
                                game.board.push(Chess.Move.from_uci(move))
                                move_made = True
                        square = None
                if b2.collidepoint(event.pos) and not game.board.turn:
                    square = 7-((event.pos[0]-b2.left)*8//b2.width)+(((event.pos[1]-b2.top)*8//b2.height))*8
                    if game.board.piece_at(square):
                        if game.board.piece_at(square).color:
                            if sq:
                                move = ascii_lowercase[sq%8] + str(sq//8+1) + ascii_lowercase[square%8] + str(square//8+1)
                                if Chess.Move.from_uci(move) in game.board.legal_moves:
                                    game.board.push(Chess.Move.from_uci(move))
                                    move_made = True
                            square = None
                    else:
                        if sq:
                            move = ascii_lowercase[sq%8] + str(sq//8+1) + ascii_lowercase[square%8] + str(square//8+1)
                            if Chess.Move.from_uci(move) in game.board.legal_moves:
                                game.board.push(Chess.Move.from_uci(move))
                                move_made = True
                        square = None
                if move_made:
                    if game.board.turn:
                        game.p2.update_time()
                    else:
                        game.p1.update_time()
                    if game.board.is_game_over():
                        if game.board.is_checkmate():
                            if game.board.turn:
                                game.winner = game.p2
                            else:
                                game.winner = game.p1
                        elif game.board.is_stalemate() or game.board.is_fivefold_repetition() or game.board.is_insufficient_material():
                            if game.p2.consciousness>game.p1.consciousness:
                                game.winner = game.p2
                            elif game.p1.consciousness>game.p2.consciousness:
                                game.winner = game.p1
                            else:
                                game.winner = game.p2
    return quit, square
if __name__ == "__main__":
    main.main()