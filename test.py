import tkinter as tk
from tkinter import filedialog
import os

class ChessGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Chess Game")
        self.window.geometry("600x600")  # Adjust the window size

        # Create a canvas to draw the board
        self.canvas = tk.Canvas(self.window, width=600, height=600)  # Adjust canvas size
        self.canvas.pack()

        # Load the board square images
        self.black_square_image = tk.PhotoImage(file="board/black.png")
        self.white_square_image = tk.PhotoImage(file="board/white.png")
        self.board_squares = []
        for i in range(64):
            if i % 2 == 0:
                self.board_squares.append(self.black_square_image)
            else:
                self.board_squares.append(self.white_square_image)

        # Draw the board
        square_size = 75  # Adjust square size
        for i in range(8):
            for j in range(8):
                square_index = i * 8 + j
                self.canvas.create_image(j * square_size, i * square_size, image=self.board_squares[square_index], anchor='nw')

        # Load the chess piece images
        self.chess_pieces = {}
        for piece in ["king", "queen", "rook", "bishop", "knight", "pawn"]:
            self.chess_pieces[piece] = {}
            for color in ["white", "black"]:
                piece_image = tk.PhotoImage(file=f"pieces/{color}/{piece}.png")
                # Reduce the size of the image by a factor of 2
                piece_image = piece_image.subsample(2, 2)
                self.chess_pieces[piece][color] = piece_image

        # Initialize the game state
        self.game_state = self.initialize_game_state()

        # Draw the chess pieces
        self.draw_chess_pieces()

        # Set up the event handlers
        self.canvas.bind("<Button-1>", self.handle_click)

        # Initialize the selected piece
        self.selected_piece = None

    def initialize_game_state(self):
        # Initialize the game state with the starting positions of the pieces
        game_state = []
        for i in range(8):
            row = []
            for j in range(8):
                if i == 1:
                    row.append(("pawn", "black"))
                elif i == 6:
                    row.append(("pawn", "white"))
                elif i == 0:
                    if j == 0 or j == 7:
                        row.append(("rook", "black"))
                    elif j == 1 or j == 6:
                        row.append(("knight", "black"))
                    elif j == 2 or j == 5:
                        row.append(("bishop", "black"))
                    elif j == 3:
                        row.append(("queen", "black"))
                    elif j == 4:
                        row.append(("king", "black"))
                elif i == 7:
                    if j == 0 or j == 7:
                        row.append(("rook", "white"))
                    elif j == 1 or j == 6:
                        row.append(("knight", "white"))
                    elif j == 2 or j == 5:
                        row.append(("bishop", "white"))
                    elif j == 3:
                        row.append(("queen", "white"))
                    elif j == 4:
                        row.append(("king", "white"))
                else:
                    row.append(None)
            game_state.append(row)
        return game_state

    def draw_chess_pieces(self):
        # Draw the chess pieces on the board
        square_size = 75  # Adjust square size
        for i in range(8):
            for j in range(8):
                piece = self.game_state[i][j]
                if piece:
                    piece_type, piece_color = piece
                    piece_image = self.chess_pieces[piece_type][piece_color]
                    self.canvas.create_image(j * square_size, i * square_size, image=piece_image, anchor='nw')

    def handle_click(self, event):
        # Handle the click event to move pieces around
        square_size = 75  # Adjust square size
        x = event.x // square_size
        y = event.y // square_size
        piece = self.game_state[y][x]

        if self.selected_piece:
            # Move the selected piece to the clicked square
            if piece:
                # Capture the piece
                self.game_state[y][x] = self.selected_piece
            else:
                # Move the piece
                self.game_state[y][x] = self.selected_piece
                self.game_state[self.selected_piece_y][self.selected_piece_x] = None
            self.selected_piece = None
            self.draw_chess_pieces()
        else:
            # Select the piece
            if piece:
                self.selected_piece = piece
                self.selected_piece_x = x
                self.selected_piece_y = y

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = ChessGame()
    game.run()