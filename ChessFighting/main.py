import pygame, os, scenes, Model, fight, Martials
import sys
window_size_y = 830
window_size_x = int(window_size_y*1.7)

def main():
    pygame.init()
    game = Model.Game()
    surface = pygame.display.set_mode([window_size_x,window_size_y])
    pygame.display.set_caption('Martial Chess')
    clock = pygame.time.Clock()
    game.p1.fighter = Martials.Blue(['Martial Hero', 'Sprites'], 10, window_size_y, game.p1)
    game.p2.fighter = Martials.Red(['Martial Hero 2', 'Sprites'], window_size_x-30, window_size_y, game.p2)
    while True:
        game.p1.update_time()
        game.p2.update_time()
        scenes.countdown(surface, game, clock)
        quit = scenes.game_chess(surface, game, clock)
        if quit:
            break
        game.round+=1
        if game.round == 10:
            break
        scenes.countdown(surface, game, clock)
        quit = fight.game_fight(surface, game, clock)
        if quit:
            break
        game.round+=1

    if not quit:
        if game.p2.consciousness>game.p1.consciousness:
            game.winner = game.p2
        elif game.p1.consciousness>game.p2.consciousness:
            game.winner = game.p1
        else:
            game.winner = game.p2
        surface.fill(BLACK)
        game_end(surface, game)
    pygame.quit()
def game_end(surface, game):
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
        quit = Controller.game_end()
        if quit:
            break
    return quit

if __name__ == "__main__":
    main()