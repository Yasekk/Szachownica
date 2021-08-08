"""Moduł zawierający główne funckcje programu."""

import pygame

from UI import SelectedPart, WinningScreen

def update_screen(screen, chess_board, board_pieces, highlight,
                  game_end):
	"""Wyświetlanie tła, szachownicy i figur."""
	screen.fill((200, 200, 200))
	for board_part in chess_board:
		board_part.draw_part()
	for selected_part in highlight:
		selected_part.draw_part()
	for piece in board_pieces:
		piece.draw_piece()
	for winning_screen in game_end:
		winning_screen.draw_message()
	pygame.display.flip()


def end_game(chess_board, screen, settings, message, game_end):
	"""Usunięcie planszy i pokazanie komunikatu końca gry."""
	winning_screen = WinningScreen(screen, settings, message)
	game_end.append(winning_screen)
	for board_part in chess_board:
		if board_part.occupied:
			board_part.occupied.kill()
		board_part.kill()


def button_click(settings, screen, chess_board, highlight, check_white,
                 check_black, board_pieces, game_end, king_attack_path):
	"""Akcje dostępne po kliknięciu na szachownicę."""
	#Zaznaczenie, że kliknięcie już raz nastapiło.
	settings.clicked = True
	#Zaznaczenie figury, która ma się poruszyć (jeżeli wcześniej się jej
	#nie wybrało).
	if settings.moving_piece == None:
		mouse_x, mouse_y = pygame.mouse.get_pos()
		for board_part in chess_board:
			#Obliczenie możliwych ruchów, jeżeli kliknięte zostanie pole
			#zajęte przez figurę i jeżeli gracz wybrał swoją figurę
			if (board_part.rect.collidepoint(mouse_x, mouse_y)
			and board_part.occupied != None
			and board_part.occupied.type == settings.current_move):
				settings.avialable_moves = board_part.occupied.moves
				#Zapamiętanie figury, która jest zaznaczona i zwolnienie
				#obecnego pola.
				settings.moving_piece = board_part.occupied
				board_part.occupied = None
				selected_part = SelectedPart(screen, settings,
				                             board_part)
				highlight.append(selected_part)
	#Jeżeli jedna z figur jest zaznaczona, poruszenie jej na wskazane 
	#pole (jeżeli jest to dozwolony ruch).	
	elif settings.moving_piece != None:
		mouse_x, mouse_y = pygame.mouse.get_pos()
		for board_part in chess_board:
			if (board_part.rect.collidepoint(mouse_x, mouse_y)
			and (board_part.name in settings.avialable_moves)):
				#Zmiana położenie figury i przypisanie jej do nowego
				#pola.
				settings.moving_piece.relocate(board_part)
				#Zapamiętanie, że figura wykonała już pierwszy ruch 
				#(Jeżeli jest pionem).
				if settings.moving_piece.piece_name == "pawn":
					settings.moving_piece.first_move = False
				#Zbicie figury, jeżeli pole jest zajmowane.
				if board_part.occupied:
					board_part.occupied.kill()
				board_part.occupied = settings.moving_piece
				#Zakończenie akcji danej figury i przekazanie kolejki
				#następnemu graczowi.
				settings.current_move = settings.next_move
				settings.next_move = settings.moving_piece.type
				settings.moving_piece = None
				settings.avialable_moves = None
				#Sprawdzenie nowych możliwych ruchów każdej figury.
				check_moves(board_pieces, chess_board, check_white,
				            check_black, king_attack_path)
				#Usunięcie podświetlenia wybranego pola.
				highlight.pop()
				#Sprawdzenie czy nastąpił szach mat.
				check_mate(chess_board, check_white, check_black,
                           game_end, screen,settings, king_attack_path)
			#Jeżeli zaznaczona figura zostanie kliknięta ponownie,
			#nastąpi anulowanie poprzedniego ruchu i bedzie możliwe
			#wybranie innej figury.
			elif (board_part.rect.collidepoint(mouse_x, mouse_y)
			and (board_part.vertical == settings.moving_piece.vertical
			and (board_part.horizontal
			     == settings.moving_piece.horizontal))):
				board_part.occupied = settings.moving_piece
				settings.moving_piece = None
				settings.avialable_moves = None
				#Usunięcie podświetlenia wybranego pola.
				highlight.pop()
				break


def check_moves(board_pieces, chess_board, check_white, check_black,
                king_attack_path):
	"""Sprawdzenie możliwych ruchów poszczególnych figur."""
	king_attack_path.clear()
	check_white.clear()
	check_black.clear()
	for piece in board_pieces:
		piece.check_move(chess_board, check_white, check_black,
                         king_attack_path)
	#Przefiltorwanie ruchów króli i usniecie tych, na których
	#króle byłyby szachowany.
	for piece in board_pieces:
		if piece.type == "white" and piece.piece_name == "king":
			copy_moves = piece.moves[:]
			for field in copy_moves:
				if field in check_black:
					piece.moves.remove(field)
		elif piece.type == "black" and piece.piece_name == "king":
			copy_moves = piece.moves[:]
			for field in copy_moves:
				if field in check_white:
					piece.moves.remove(field)


def check_mate(chess_board, check_white, check_black, game_end, screen,
               settings, king_attack_path):
	"""Sprawdzenie czy któryś z królów jest szachowany i czy nie może
	się ruszyć.
	"""
	#Jeżeli król jest szachowany przez figurę, która porusza się w 
	#rzedzie, sprawdzenie, czy jst jakaś figura, która może szałonić 
	#króla lub zbić atakująca figurę.
	skip_checkmate = False		
	if settings.current_move == "white":
		for board_part in chess_board:
			if board_part.occupied:
				if (board_part.occupied.type == "white"
				and board_part.occupied.piece_name != "king"):
					for move in board_part.occupied.moves:
						if move in king_attack_path:
							skip_checkmate = True
				#Jeżeli jest ruch białych (czyli zakończył się ruch
				#czarnych) a czarny król nadal jest szachowany,
				#następuje szach mat.
				elif (board_part.occupied.type == "black"
				and board_part.occupied.piece_name=="king"):
					if board_part.name in check_white:
						end_game(chess_board, screen, settings,
						         "wygrały białe", game_end)
	elif settings.current_move == "black":
		for board_part in chess_board:
			if board_part.occupied:
				if (board_part.occupied.type == "black"
				and board_part.occupied.piece_name != "king"):
					for move in board_part.occupied.moves:
						if move in king_attack_path:
							skip_checkmate = True
				#Jeżeli jest ruch czarnych (czyli zakończył się ruch
				#białych) a biały król nadal jest szachowany,
				#następuje szach mat.
				elif (board_part.occupied.type == "white"
				and board_part.occupied.piece_name == "king"):
					if board_part.name in check_black:
						end_game(chess_board, screen, settings,
						         "wygrały czarne", game_end)
	if skip_checkmate == False:
		for board_part in chess_board:
			if board_part.occupied:
				if (board_part.occupied.type == "white"
				and board_part.occupied.piece_name == "king"):
					if (board_part.name in check_black
					and len(board_part.occupied.moves) == 0):
							end_game(chess_board, screen, settings,
							         "wygrały czarne", game_end)
							break
				elif (board_part.occupied.type == "black"
				and board_part.occupied.piece_name == "king"):
					if (board_part.name in check_white
					and len(board_part.occupied.moves) == 0):
							end_game(chess_board, screen, settings,
							         "wygrały białe", game_end)
							break
