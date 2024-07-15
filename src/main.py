import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):
        while True:
            # show methods
            self.game.show_bg(self.screen)
            self.game.show_last_move(self.screen)
            self.game.show_moves(self.screen)
            self.game.show_pieces(self.screen)
            self.game.show_hover(self.screen)

            if self.game.dragger.dragging:
                self.game.dragger.update_blit(self.screen)

            for event in pygame.event.get():
                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.game.dragger.update_mouse(event.pos)

                    clicked_row = self.game.dragger.mouseY // SQSIZE
                    clicked_col = self.game.dragger.mouseX // SQSIZE

                    # if clicked square has a piece ?
                    if self.game.board.squares[clicked_row][clicked_col].has_piece():
                        piece = self.game.board.squares[clicked_row][clicked_col].piece
                        # valid piece (color) ?
                        if piece.color == self.game.next_player:
                            self.game.board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            self.game.dragger.save_initial(event.pos)
                            self.game.dragger.drag_piece(piece)
                            # show methods 
                            self.game.show_bg(self.screen)
                            self.game.show_last_move(self.screen)
                            self.game.show_moves(self.screen)
                            self.game.show_pieces(self.screen)
                
                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    self.game.set_hover(motion_row, motion_col)

                    if self.game.dragger.dragging:
                        self.game.dragger.update_mouse(event.pos)
                        # show methods
                        self.game.show_bg(self.screen)
                        self.game.show_last_move(self.screen)
                        self.game.show_moves(self.screen)
                        self.game.show_pieces(self.screen)
                        self.game.show_hover(self.screen)
                        self.game.dragger.update_blit(self.screen)
                
                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    if self.game.dragger.dragging:
                        self.game.dragger.update_mouse(event.pos)

                        released_row = self.game.dragger.mouseY // SQSIZE
                        released_col = self.game.dragger.mouseX // SQSIZE

                        # create possible move
                        initial = Square(self.game.dragger.initial_row, self.game.dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # valid move ?
                        if self.game.board.valid_move(self.game.dragger.piece, move):
                            # normal capture
                            captured = self.game.board.squares[released_row][released_col].has_piece()
                            self.game.board.move(self.game.dragger.piece, move)

                            self.game.board.set_true_en_passant(self.game.dragger.piece)                            

                            # sounds
                            self.game.play_sound(captured)
                            # show methods
                            self.game.show_bg(self.screen)
                            self.game.show_last_move(self.screen)
                            self.game.show_pieces(self.screen)
                            # next turn
                            self.game.next_turn()
                    
                    self.game.dragger.undrag_piece()
                
                # key press
                elif event.type == pygame.KEYDOWN:
                    
                    # changing themes
                    if event.key == pygame.K_t:
                        self.game.change_theme()

                     # changing themes
                    if event.key == pygame.K_r:
                        self.game.reset()
                        self.game = Game()
                        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        pygame.display.set_caption('Chess')

                # quit application
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.mainloop()