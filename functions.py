import pygame
def update_screen(screen,chess_board,board_pieces):
	"""Wyświetlanie tła, szachownicy i figur"""
	screen.fill((200,200,200))
	for board_part in chess_board:
		board_part.draw_part()
	for piece in board_pieces:
		piece.draw_piece()
	pygame.display.flip()
def button_click(settings,chess_board):
	"""Akcje dostępne po kliknięciu na szachownicę"""
	#Zaznaczenie, że kliknięcie już raz nastapiło
	settings.clicked=True
	#Zaznaczenie figury, która ma się poruszyć
	if settings.moving_piece==None:
		mouse_x,mouse_y = pygame.mouse.get_pos()
		for board_part in chess_board:
			#Obliczenie możliwych ruchów, jeżeli kliknięte zostanie pole
			#zajęte przez figurę
			if board_part.rect.collidepoint(mouse_x,mouse_y) and (
			board_part.occupied!=None):
				settings.avialable_moves=(
				board_part.occupied.check_move(chess_board))
				#Zapamiętanie figury, która jest zaznaczona i zwolnienie
				#obecnego pola
				settings.moving_piece=board_part.occupied
				board_part.occupied=None
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
				#Zbicie figury, jeżeli pole jest zajmowane
				if board_part.occupied:
					board_part.occupied.kill()
				board_part.occupied=settings.moving_piece
				#Zakończenie akcji danej figury
				settings.moving_piece=None
				settings.avialable_moves=None
			#Jeżeli zaznaczona figura zostanie kliknięta ponownie,
			#nastąpi anulowanie poprzedniego ruchu i bedzie możliwe
			#wybranie innej figury
			elif board_part.rect.collidepoint(mouse_x,mouse_y) and (
			board_part.vertical==settings.moving_piece.vertical and 
			board_part.vertical==settings.moving_piece.vertical):
				board_part.occupied=settings.moving_piece
				settings.moving_piece=None
				settings.avialable_moves=None
				break

