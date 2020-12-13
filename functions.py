import pygame
from UI import SelectedPart
def update_screen(screen,chess_board,board_pieces,highlight):
	"""Wyświetlanie tła, szachownicy i figur"""
	screen.fill((200,200,200))
	for board_part in chess_board:
		board_part.draw_part()
	for selected_part in highlight:
		selected_part.draw_part()
	for piece in board_pieces:
		piece.draw_piece()
	pygame.display.flip()
def button_click(settings,screen,chess_board,highlight,check_white,
check_black,board_pieces):
	"""Akcje dostępne po kliknięciu na szachownicę"""
	#Zaznaczenie, że kliknięcie już raz nastapiło
	settings.clicked=True
	#Zaznaczenie figury, która ma się poruszyć (jeżeli wcześniej się jej
	#nie wybrało)
	if settings.moving_piece==None:
		mouse_x,mouse_y = pygame.mouse.get_pos()
		for board_part in chess_board:
			#Obliczenie możliwych ruchów, jeżeli kliknięte zostanie pole
			#zajęte przez figurę i jeżeli gracz wybrał swoją figurę
			if (board_part.rect.collidepoint(mouse_x,mouse_y) and
			board_part.occupied!=None and 
			board_part.occupied.type==settings.current_move):
				settings.avialable_moves=(
				board_part.occupied.moves)
				#Zapamiętanie figury, która jest zaznaczona i zwolnienie
				#obecnego pola
				settings.moving_piece=board_part.occupied
				board_part.occupied=None
				selected_part=SelectedPart(screen,settings,board_part)
				highlight.append(selected_part)
	#Jeżeli jedna z figur jest zaznaczona, poruszenie jej na wskazane 
	#pole (jeżeli jest to dozwolony ruch)	
	elif settings.moving_piece!=None:
		mouse_x,mouse_y = pygame.mouse.get_pos()
		for board_part in chess_board:
			if board_part.rect.collidepoint(mouse_x,mouse_y) and (
			board_part.name in settings.avialable_moves):
				#Zmiana położenie figury i przypisanie jej do nowego
				#pola
				settings.moving_piece.relocate(board_part)
				#Zapamiętanie, że figura wykonała już pierwszy ruch 
				#(Jeżeli jest pionem)
				if settings.moving_piece.piece_name=="pawn":
					settings.moving_piece.first_move=False
				#Zbicie figury, jeżeli pole jest zajmowane
				if board_part.occupied:
					board_part.occupied.kill()
				board_part.occupied=settings.moving_piece
				#Zakończenie akcji danej figury i przekazanie kolejki
				#następnemu graczowi
				settings.current_move=settings.next_move
				settings.next_move=settings.moving_piece.type
				settings.moving_piece=None
				settings.avialable_moves=None
				#Sprawdzenie nowych możliwych ruchów każdej figury
				check_moves(board_pieces,chess_board,check_white,
				check_black)
				#Usunięcie podświetlenia wybranego pola
				highlight.pop()
				#Sprawdzanie, które pola mogą być obecnie atakowane
				#przez figury danego koloru
				#for board_part in chess_board:
					#if board_part.occupied:
						#if board_part.occupied.type=="white":
							#for field in board_part.occupied.check_move(
							#chess_board,check_white,check_black):
								#check_white.append(field)
						#elif board_part.occupied.type=="black":
							#for field in board_part.occupied.check_move(
							#chess_board,check_white,check_black):
								#check_black.append(field)
				#Sprawdzenie, czy któryś z króli jest szachowany
				#for board_piece in board_pieces:
					#if board_piece
			#Jeżeli zaznaczona figura zostanie kliknięta ponownie,
			#nastąpi anulowanie poprzedniego ruchu i bedzie możliwe
			#wybranie innej figury
			elif board_part.rect.collidepoint(mouse_x,mouse_y) and (
			board_part.vertical==settings.moving_piece.vertical and 
			board_part.horizontal==settings.moving_piece.horizontal):
				board_part.occupied=settings.moving_piece
				settings.moving_piece=None
				settings.avialable_moves=None
				#Usunięcie podświetlenia wybranego pola
				highlight.pop()
				break
def check_moves(board_pieces,chess_board,check_white,check_black):
	"""Sprawdzenie możliwych ruchów poszczególnych figur"""
	check_white.clear()
	check_black.clear()
	for piece in board_pieces:
		piece.check_move(chess_board,check_white,check_black)
	#Przefiltorwanie ruchów króli i usniecie tych, na których
	#króle byłyby szachowany
	for piece in board_pieces:
		if piece.type=="white" and piece.piece_name=="king":
			copy_moves=piece.moves[:]
			for field in copy_moves:
				if field in check_black:
					piece.moves.remove(field)
		elif piece.type=="black" and piece.piece_name=="king":
			copy_moves=piece.moves[:]
			for field in copy_moves:
				if field in check_white:
					piece.moves.remove(field)

