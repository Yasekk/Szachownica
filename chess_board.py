"""Moduł odpowiedzialny za tworzenie szachownicy i figur."""

import pygame
from pygame.sprite import Sprite

from chess_pieces import Pawn, Rook, Knight, Bishop, Queen,King

class BoardPart(Sprite):
	"""Tworzenie pól na szachownicy."""
	
	def __init__(self, screen, settings):
		super().__init__()
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.rect = pygame.Rect(0, 0, settings.chess_field_size,
                                settings.chess_field_size)
		self.color = (255, 255, 255)
		#Atrybut, w którym będzie znajdowała się nazwa danego pola.
		self.name = None
		self.horizontal = None
		self.vertical = None	
		#Atrybut, który wskazuje czy dane pole jest obecnie zajmowane i
		#przez jaką figurę.
		self.occupied = None

	def draw_part(self):
		"""Wyświetlenie pola szachownicy."""
		pygame.draw.rect(self.screen, self.color, self.rect)


def create_board_and_pieces(settings, screen, chess_board, board_pieces,
                            check_white, check_black):
	"""Tworzenie szachownicy i figur, które mają przypisane początkowe 
	pozycje."""
	order_x = ["A", "B", "C", "D", "E", "F", "G", "H"]
	#Skorzystanie z listy order_y aby kolejnośc tworzenia pól pasowała
	#do typowego układu szachownicy (od 1 do 8 od dołu).
	order_y = [7, 6, 5, 4, 3, 2, 1, 0]
	for horizontal in range(8):
		for vertical in range(8):
			board_part = BoardPart(screen, settings)
			board_part.rect.left = (
			    settings.width_grid*horizontal
			    + settings.chess_field_size*horizontal
			    + 200)
			board_part.rect.bottom = (
			    settings.width_grid*order_y[vertical]
			    + settings.chess_field_size*order_y[vertical]
			    + 90)
			board_part.name = order_x[horizontal] + str(vertical+1)
			#Zapisanie pionowego i poziomego położenia danego pola.
			board_part.horizontal = horizontal+1
			board_part.vertical = vertical+1
			if (horizontal+vertical)%2 == 0:
				#Upewnienie się że przylegające pola będą miały inny 
				#kolor.
				board_part.color = (10, 50, 100)
			#Stworzenie figur szachowych i przypisanie poszczególnemu
			#polu figury, które będzie na nim domyslnie stała.
			if board_part.name == "A2":
				white_pawn_1 = Pawn("white", screen, settings)
				white_pawn_1.relocate(board_part)
				board_pieces.add(white_pawn_1)
				board_part.occupied = white_pawn_1
			elif board_part.name == "B2":
				white_pawn_2 = Pawn("white", screen, settings)
				white_pawn_2.relocate(board_part)
				board_pieces.add(white_pawn_2)
				board_part.occupied = white_pawn_2
			elif board_part.name == "C2":
				white_pawn_3 = Pawn("white", screen, settings)
				white_pawn_3.relocate(board_part)
				board_pieces.add(white_pawn_3)
				board_part.occupied = white_pawn_3
			elif board_part.name == "D2":
				white_pawn_4 = Pawn("white", screen, settings)
				white_pawn_4.relocate(board_part)
				board_pieces.add(white_pawn_4)
				board_part.occupied = white_pawn_4
			elif board_part.name == "E2":
				white_pawn_5 = Pawn("white", screen, settings)
				white_pawn_5.relocate(board_part)
				board_pieces.add(white_pawn_5)
				board_part.occupied = white_pawn_5
			elif board_part.name == "F2":
				white_pawn_6 = Pawn("white", screen, settings)
				white_pawn_6.relocate(board_part)
				board_pieces.add(white_pawn_6)
				board_part.occupied = white_pawn_6
			elif board_part.name == "G2":
				white_pawn_7 = Pawn("white", screen, settings)
				white_pawn_7.relocate(board_part)
				board_pieces.add(white_pawn_7)
				board_part.occupied = white_pawn_7
			elif board_part.name == "H2":
				white_pawn_8 = Pawn("white", screen, settings)
				white_pawn_8.relocate(board_part)
				board_pieces.add(white_pawn_8)
				board_part.occupied = white_pawn_8
			elif board_part.name == "A1":
				white_rook_1 = Rook("white", screen, settings)
				white_rook_1.relocate(board_part)
				board_pieces.add(white_rook_1)
				board_part.occupied = white_rook_1
			elif board_part.name == "H1":
				white_rook_2 = Rook("white", screen, settings)
				white_rook_2.relocate(board_part)
				board_pieces.add(white_rook_2)
				board_part.occupied = white_rook_2
			elif board_part.name == "B1":
				white_knight_1 = Knight("white", screen, settings)
				white_knight_1.relocate(board_part)
				board_pieces.add(white_knight_1)
				board_part.occupied = white_knight_1
			elif board_part.name == "G1":
				white_knight_2 = Knight("white", screen, settings)
				white_knight_2.relocate(board_part)
				board_pieces.add(white_knight_2)
				board_part.occupied = white_knight_2
			elif board_part.name == "C1":
				white_bishop_1 = Bishop("white", screen, settings)
				white_bishop_1.relocate(board_part)
				board_pieces.add(white_bishop_1)
				board_part.occupied = white_bishop_1
			elif board_part.name == "F1":
				white_bishop_2 = Bishop("white", screen, settings)
				white_bishop_2.relocate(board_part)
				board_pieces.add(white_bishop_2)
				board_part.occupied = white_bishop_2
			elif board_part.name == "D1":
				white_queen = Queen("white", screen, settings)
				white_queen.relocate(board_part)
				board_pieces.add(white_queen)
				board_part.occupied = white_queen
			elif board_part.name == "E1":
				white_king = King("white", screen, settings)
				white_king.relocate(board_part)
				board_pieces.add(white_king)
				board_part.occupied = white_king
			elif board_part.name == "A7":
				black_pawn_1 = Pawn("black", screen, settings)
				black_pawn_1.relocate(board_part)
				board_pieces.add(black_pawn_1)
				board_part.occupied = black_pawn_1
			elif board_part.name == "B7":
				black_pawn_2 = Pawn("black", screen, settings)
				black_pawn_2.relocate(board_part)
				board_pieces.add(black_pawn_2)
				board_part.occupied = black_pawn_2
			elif board_part.name == "C7":
				black_pawn_3 = Pawn("black", screen, settings)
				black_pawn_3.relocate(board_part)
				board_pieces.add(black_pawn_3)
				board_part.occupied = black_pawn_3
			elif board_part.name == "D7":
				black_pawn_4 = Pawn("black", screen, settings)
				black_pawn_4.relocate(board_part)
				board_pieces.add(black_pawn_4)
				board_part.occupied = black_pawn_4
			elif board_part.name == "E7":
				black_pawn_5 = Pawn("black", screen, settings)
				black_pawn_5.relocate(board_part)
				board_pieces.add(black_pawn_5)
				board_part.occupied = black_pawn_5
			elif board_part.name == "F7":
				black_pawn_6 = Pawn("black", screen, settings)
				black_pawn_6.relocate(board_part)
				board_pieces.add(black_pawn_6)
				board_part.occupied = black_pawn_6
			elif board_part.name == "G7":
				black_pawn_7 = Pawn("black", screen, settings)
				black_pawn_7.relocate(board_part)
				board_pieces.add(black_pawn_7)
				board_part.occupied = black_pawn_7
			elif board_part.name == "H7":
				black_pawn_8 = Pawn("black", screen, settings)
				black_pawn_8.relocate(board_part)
				board_pieces.add(black_pawn_8)
				board_part.occupied = black_pawn_8
			elif board_part.name == "A8":
				black_rook_1 = Rook("black", screen, settings)
				black_rook_1.relocate(board_part)
				board_pieces.add(black_rook_1)
				board_part.occupied = black_rook_1
			elif board_part.name == "H8":
				black_rook_2 = Rook("black", screen, settings)
				black_rook_2.relocate(board_part)
				board_pieces.add(black_rook_2)
				board_part.occupied = black_rook_2
			elif board_part.name == "B8":
				black_knight_1 = Knight("black", screen, settings)
				black_knight_1.relocate(board_part)
				board_pieces.add(black_knight_1)
				board_part.occupied = black_knight_1
			elif board_part.name == "G8":
				black_knight_2 = Knight("black", screen, settings)
				black_knight_2.relocate(board_part)
				board_pieces.add(black_knight_2)
				board_part.occupied = black_knight_2
			elif board_part.name == "C8":
				black_bishop_1 = Bishop("black", screen, settings)
				black_bishop_1.relocate(board_part)
				board_pieces.add(black_bishop_1)
				board_part.occupied = black_bishop_1
			elif board_part.name == "F8":
				black_bishop_2 = Bishop("black", screen, settings)
				black_bishop_2.relocate(board_part)
				board_pieces.add(black_bishop_2)
				board_part.occupied = black_bishop_2
			elif board_part.name == "D8":
				black_queen = Queen("black", screen, settings)
				black_queen.relocate(board_part)
				board_pieces.add(black_queen)
				board_part.occupied = black_queen
			elif board_part.name == "E8":
				black_king = King("black", screen, settings)
				black_king.relocate(board_part)
				board_pieces.add(black_king)
				board_part.occupied = black_king
			chess_board.add(board_part)
