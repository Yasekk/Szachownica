"""Moduł odpowiedzialny za figury szachowe i powiązane z nimi funkcje."""

import json
import pygame
from pygame.sprite import Sprite, Group

def check_move_jump(self, chess_field, avialable_fields, check_white,
                    check_black, horizontal, vertical,
                    king_attack_path):
	"""Sprawdzanie dostepnych pól dla figur skaczących."""
	if (chess_field.horizontal == self.horizontal + horizontal
	and chess_field.vertical == self.vertical + vertical):
		#Możiwość przejścia na pola, które są albo puste albo 
		#zajęte przez figurę przeciwnika.
		if chess_field.occupied == None: 
			avialable_fields.append(chess_field.name)
		elif self.type != chess_field.occupied.type:
			avialable_fields.append(chess_field.name)
			if chess_field.occupied.piece_name == "king":
				king_attack_path.append(chess_field.name)
			#Jeżeli pole jest zajęte przez figurę tego samego koloru
			#to zostanie dodane do pól potencjalnie szachowanych.
		elif (chess_field.occupied != None
		and self.type == chess_field.occupied.type):
			if self.type == "white":
				check_white.append(chess_field.name)
			elif self.type == "black":
				check_black.append(chess_field.name)


def check_move_row(obstacle_found, king_found, chess_board,
                   self,vertical, horizontal, avialable_fields,
                   check_white, check_black, king_attack_path):
	"""Sprawdzenie dostępnych pól dla figur poruszających się w
	rzędzie.
	"""
	for next_field in range(1, 8):
		#Zaprzestanie szukania w danym rzędzie, jeżeli natafiło się
		#już na inną figurę.
		if obstacle_found == True:
			break
		#Szukanie pól, które mają kolejne pozycje w danym rzedzie.
		for chess_field in chess_board:
			if ((chess_field.vertical
			     == self.vertical + next_field*vertical)
			and (chess_field.horizontal
			     == self.horizontal + next_field*horizontal)):
				if chess_field.occupied:
					#Jeżeli pole jest zajęte przez figurę innego
					#koloru, będzie możliwe stanie na tym polu, ale 
					#nie dalej.
					if chess_field.occupied.type != self.type:
						if (chess_field.occupied.piece_name != "king"
						and king_found == False):
							avialable_fields.append(chess_field.name)
							obstacle_found = True
							break
						#Jeżeli dana figura stoi za królem, iteracja
						#jest zakończona.
						elif (chess_field.occupied.piece_name != "king" 
						and king_found == True):
							obstacle_found = True
							break
						#Jeżeli natrafi sie na króla, iteracja jest
						#kontynuowana. Dalsze pola nie będą możliwymi
						#ruchami ale polami, na które król nie będzie
						#mógł się ruszyć.
						else:
							avialable_fields.append(chess_field.name)
							king_found = True
							#Pola na którym stoi figura zagrażająca 
							#królowi raz cała ścieżka prowaząca do niego
							#są dodane do osobnej listy. Pomoże to 
							#wykluczyć szachmta, jeżeli da się zasłonić 
							#tę ścieżkę.
							for next_one in range(0, next_field):
								for chess_part in chess_board:
									if ((chess_part.vertical 
									     == self.vertical
									     + next_one*vertical) 
									and (chess_part.horizontal
									     == self.horizontal
									     + next_one*horizontal)):
										king_attack_path.append(
										    chess_part.name)
					#Jezeli pole jest zajęte przez figurę tego
					#samego koloru, nie będzie mozna zając tego
					#pola ani żadnego dalszego, ale zostanie dodane 
					#to pole do pól szachowanych.
					elif chess_field.occupied.type == self.type:
						if self.type == "white":
							check_white.append(chess_field.name)
						elif self.type == "black":
							check_black.append(chess_field.name)
						obstacle_found = True
						break
				#Pozostałe wolne pola są dodane do puli możliwych
				#ruchów (albo tylko do pól potencjalnie szachowanych
				#jeżeli stoją za królem).
				else:
					if not king_found:
						avialable_fields.append(chess_field.name)
					elif king_found:
						if self.type=="white":
							check_white.append(chess_field.name)
						elif self.type=="black":
							check_black.append(chess_field.name)


def load_picture(screen, settings, piece_type, piece_name, picture):
	"""Wczytywanie obrazku figury."""
	with open("Pictures/" + piece_type + "_" + piece_name + ".json",
	          "r") as (picture_load):
		#Wczytywanie danych z pliku pasującego do nazwy konkretnej
		#figury i odtwarzanie z nich rysunku figury.
		picture_data = json.load(picture_load)
		for picture_element_data in picture_data:
			picture_element = PiecePart(screen,
			                            settings,
			                            picture_element_data[1])
			picture_element.rect.center = picture_element_data[0]
			picture.add(picture_element)


def set_position(picture):
	"""Ustalenie wzglednego położenia każdego elementu rysunku w
	stosunku do środka rysunku.
	"""
	positions_x = []
	positions_y = []
	#Ustalenie skrajnych wartości pozycji elementów i wyliczenie ich 
	#połów (które w pionie i poziomie określą środek rysuknu).
	for picture_part in picture:
		positions_x.append(picture_part.rect.centerx)
		positions_y.append(picture_part.rect.centery)
	center_x = (min(positions_x) + max(positions_x)) / 2
	center_y = (min(positions_y) + max(positions_y)) / 2
	#Określenie pozycji każdego elementów rysunku względem środka.
	for picture_part in picture:
		picture_part.position_x = picture_part.rect.centerx - center_x
		picture_part.position_y = picture_part.rect.centery - center_y


class PiecePart(Sprite):
	"""Tworzenie sprite'ów, z których będą składały się figury."""

	def __init__(self, screen, settings, color):
		super().__init__()
		self.screen = screen
		self.screen_rect = screen.get_rect()
		#Wymiary są nieco większe niż wyliczone proporcje, żeby
		#zaokrąglenia do liczb całkowitych nie tworzyły dziur.
		self.rect = pygame.Rect(0, 0, settings.width_grid*1.1,
		                        settings.height_grid*1.1)
		self.color = color
		#Dodanie atrybutów, które będą zawierały informację o wzglednym
		#położeniu elementu w stosunku do środka rysunku.
		self.position_x = None
		self.postion_y = None

	def draw_part(self):
		"""Wyświetlenie elementu rysunku."""
		pygame.draw.rect(self.screen, self.color, self.rect)


class Pawn(Sprite):
	"""Klasa odpowiedzialna za tworzenie pionka i określanie jego
	ruchów.
	"""
	
	def __init__(self, piece_type, screen, settings):
		super().__init__()
		self.type = piece_type
		self.picture = Group()
		self.screen = screen
		self.settings = settings
		self.piece_name = "pawn"
		self.type = piece_type
		#Upewnienie się, że ruch o dwa pola będzie mozliwy tylko
		#raz.
		self.first_move = True
		#Atrybut zawierający położenie w jakim obecnie znajduje się 
		#figura.
		self.vertical = None
		self.horizontal = None
		#Tworzenie rysunku figury z pliku.
		load_picture(screen, settings, piece_type, self.piece_name,
                     self.picture)
		#Określenie względnej pozycji każego elementu rysunku.
		set_position(self.picture)
		#Aktualnie mozliwe ruchy danej figury.
		self.moves = None

	def draw_piece(self):
		"""Wyświetlenie wszystkich elementów z których składa się 
		figura.
		"""
		for picture_part in self.picture:
			picture_part.draw_part()

	def relocate(self, board_field):
		"""Zmiana pozycji figury wzgledem podanych parametrów i 
		zapisanie pola na jakim znajduje się figura.
		"""
		self.field = board_field
		for picture_element in self.picture:
			picture_element.rect.centerx = (self.field.rect.centerx
			                                +picture_element.position_x)
			picture_element.rect.centery = (self.field.rect.centery
			                                +picture_element.position_y)
		#Przypisanie położenia pola, na którym znajduje się figura.
		self.vertical = board_field.vertical
		self.horizontal = board_field.horizontal

	def check_move(self, chess_board, check_white, check_black,
	               king_attack_path):
		"""Sprawdzanie pól dostępnych w danym ruchu."""
		avialable_fields = []
		#Ruch dla pionów białych.
		if self.type == "white":
			if self.first_move:
				#W pierwszym ruchu mozna poruszyć się pionem o jedno lub
				#dwa pola do przodu, chyba że natrafi się na inną
				#figurę.
				obstacle_found = False
				for distance in range(1, 3):
					if obstacle_found:
						break
					for chess_field in chess_board:
						#Znalezienie pól na szachownicy, które mają 
						#takie samo położenie poziome co obecnie 
						#zajmowane i jedno lub dwa pola wyższe.
						if ((chess_field.vertical
						     == self.vertical + distance)
						and chess_field.horizontal == self.horizontal):
							if chess_field.occupied != None:
								obstacle_found = True
								break
							avialable_fields.append(chess_field.name)
				#Ewentualnie bicie po skosie.
				for chess_field in chess_board:
					if (chess_field.vertical == self.vertical+1
					and chess_field.horizontal == self.horizontal+1): 
						#Jeżeli pole po skosie jest zajęte, zostanie
						#dodane do możwliwych ruchów (jeżeli stoi tam
						#figura przeciwnika) lub zostanie tylko dodane 
						#do pól potencjalnie szachowanych jeśli stoi tam 
						#własna figura.
						if chess_field.occupied != None:
							if chess_field.occupied.type != self.type:
								avialable_fields.append(
								    chess_field.name)
								check_white.append(chess_field.name)
							else:
								check_white.append(chess_field.name)
						#Jeśli pole jest puste, zostanie dodane do listy
						#pól potencjalnie szachowanych.
						else:
							check_white.append(chess_field.name)
					elif (chess_field.vertical == self.vertical+1
					and chess_field.horizontal == self.horizontal-1): 
						if chess_field.occupied != None:
							if chess_field.occupied.type != self.type:
								avialable_fields.append(
								    chess_field.name)
								check_white.append(chess_field.name)
							else:
								check_white.append(chess_field.name)
						else:
							check_white.append(chess_field.name)
			else:
				#W drugim ruchu można poruszyć się o jedno wolne pole do
				#przodu albo zbić przeciwną figurę po skosie.
				for chess_field in chess_board:
					if (chess_field.vertical == self.vertical+1
					and chess_field.horizontal == self.horizontal
					and chess_field.occupied == None):
						avialable_fields.append(chess_field.name)
					elif (chess_field.vertical == self.vertical+1
					and chess_field.horizontal == self.horizontal+1): 
						#Jeżeli pole po skosie jest zajęte, zostanie
						#dodane do możwliwych ruchów (jeżeli stoi tam
						#figura przeciwnika) lub zostanie tylko dodane 
						#do pól potencjalnie szachowanych jeśli stoi tam 
						#własna figura.
						if chess_field.occupied != None:
							if chess_field.occupied.type != self.type:
								avialable_fields.append(
								    chess_field.name)
								check_white.append(chess_field.name)
							else:
								check_white.append(chess_field.name)
						#Jeśli pole jest puste, zostanie dodane do listy
						#pól potencjalnie szachowanych.
						else:
							check_white.append(chess_field.name)
					elif (chess_field.vertical == self.vertical+1
					and chess_field.horizontal == self.horizontal-1): 
						if chess_field.occupied != None:
							if chess_field.occupied.type != self.type:
								avialable_fields.append(
								    chess_field.name)
								check_white.append(chess_field.name)
							else:
								check_white.append(chess_field.name)
						else:
							check_white.append(chess_field.name)
		#Ruch dla pionów czarnych
		if self.type == "black":
			if self.first_move:
				#W pierwszym ruchu mozna poruszyć się pionem o jedno lub
				#dwa pola do przodu, chyba że natrafi się na inną
				#figurę.
				obstacle_found = False
				for distance in range(1, 3):		
					if obstacle_found:
						break
					for chess_field in chess_board:
						#Znalezienie pól na szachownicy, które mają 
						#takie samo położenie poziome co obecnie 
						#zajmowane i jedno lub dwa pola wyższe.
						if ((chess_field.vertical
						     == self.vertical - distance)
						and chess_field.horizontal == self.horizontal):
							if chess_field.occupied != None:
								obstacle_found = True
								break
							avialable_fields.append(chess_field.name)
				#Ewentualnie bicie po skosie, jeżeli znajduje się 
				#tam figura przeiwnika (i dopisane tych pól do pól 
				#szachowanych).
				for chess_field in chess_board:
					if (chess_field.vertical == self.vertical-1
					and chess_field.horizontal == self.horizontal+1): 
						#Jeżeli pole po skosie jest zajęte, zostanie
						#dodane do możwliwych ruchów (jeżeli stoi tam
						#figura przeciwnika) lub zostanie tylko dodane 
						#do pól potencjalnie szachowanych jeśli stoi tam 
						#własna figura.
						if chess_field.occupied != None:
							if chess_field.occupied.type != self.type:
								avialable_fields.append(
								    chess_field.name)
								check_black.append(chess_field.name)
							else:
								check_black.append(chess_field.name)
						#Jeśli pole jest puste, zostanie dodane do listy
						#pól potencjalnie szachowanych.
						else:
							check_black.append(chess_field.name)
					elif (chess_field.vertical == self.vertical
					and chess_field.horizontal == self.horizontal-1): 
						if chess_field.occupied != None:
							if chess_field.occupied.type != self.type:
								avialable_fields.append(
								    chess_field.name)
								check_black.append(chess_field.name)
							else:
								check_black.append(chess_field.name)
						else:
							check_black.append(chess_field.name)
			else:
				#W drugim ruchu można poruszyć się o jedno wolne pole do
				#przodu albo zbić przeciwną figurę po skosie (dopisane 
				#też tych pól do pól szachowanych).
				for chess_field in chess_board:
					if (chess_field.vertical == self.vertical-1
					and chess_field.horizontal == self.horizontal
					and chess_field.occupied == None):
						avialable_fields.append(chess_field.name)
					elif (chess_field.vertical == self.vertical-1
					and chess_field.horizontal == self.horizontal+1): 
						#Jeżeli pole po skosie jest zajęte, zostanie
						#dodane do możwliwych ruchów (jeżeli stoi tam
						#figura przeciwnika) lub zostanie tylko dodane 
						#do pól potencjalnie szachowanych jeśli stoi tam 
						#własna figura.
						if chess_field.occupied != None:
							if chess_field.occupied.type != self.type:
								avialable_fields.append(
								    chess_field.name)
								check_black.append(chess_field.name)
							else:
								check_black.append(chess_field.name)
						#Jeśli pole jest puste, zostanie dodane do listy
						#pól potencjalnie szachowanych.
						else:
							check_black.append(chess_field.name)
					elif (chess_field.vertical == self.vertical-1
					and chess_field.horizontal == self.horizontal-1): 
						if chess_field.occupied != None:
							if chess_field.occupied.type != self.type:
								avialable_fields.append(
								    chess_field.name)
								check_black.append(chess_field.name)
							else:
								check_black.append(chess_field.name)
						else:
							check_black.append(chess_field.name)	
		self.moves = avialable_fields


class Rook(Sprite):
	"""Tworzenie wieży"""
	def __init__(self,piece_type,screen,settings):
		super().__init__()
		self.type=piece_type
		self.picture=Group()
		self.screen=screen
		self.settings=settings
		self.piece_name="rook"
		#Atrybut zawierający pole na jakim obecnie znajduje się figura
		self.field=None
		#Tworzenie rysunku figury z pliku
		load_picture(screen,settings,piece_type,self.piece_name,
		self.picture)
		#Określenie względnej pozycji każego elementu rysunku
		set_position(self.picture)
		#Aktualnie mozliwe ruchy danej figury
		self.moves=None
	def draw_piece(self):
		"""Wyświetlenie wszystkich elementów z których składa się 
		figura"""
		for picture_part in self.picture:
			picture_part.draw_part()
	def relocate(self,board_field):
		"""Zmiana pozycji figury wzgledem podanych parametrów i 
		zapisanie pola na jakim znajduje się figura"""
		self.field=board_field
		for picture_element in self.picture:
			picture_element.rect.centerx=(self.field.rect.centerx+
			picture_element.position_x)
			picture_element.rect.centery=(self.field.rect.centery+
			picture_element.position_y)
		#Przypisanie położenia pola, na którym znajduje się figura
		self.vertical=board_field.vertical
		self.horizontal=board_field.horizontal
	def check_move(self,chess_board,check_white,check_black,
	king_attack_path):
		"""Sprawdzanie pól dostępnych w danym ruchu"""
		avialable_fields=[]
		#Dodanie zmiennych, które zawierają informację, czy pole w 
		#rzędzie jest zablokowane i czy nie można przesunąć się dalej
		field_up_obstacle_found=False
		field_up_king_found=False
		field_down_obstacle_found=False
		field_down_king_found=False
		field_left_obstacle_found=False
		field_left_king_found=False
		field_right_obstacle_found=False
		field_right_king_found=False
		#Sprawdzenie dostępnych pól w rzędzie w górę
		check_move_row(field_up_obstacle_found,field_up_king_found,
		chess_board,self,1,0,avialable_fields,check_white,check_black,
		king_attack_path)
		#Sprawdzenie dostępnych pól w rzędzie w dół
		check_move_row(field_down_obstacle_found,field_down_king_found,
		chess_board,self,-1,0,avialable_fields,check_white,check_black,
		king_attack_path)
		#Sprawdzenie dostępnych pól w rzędzie w lewo
		check_move_row(field_left_obstacle_found,field_left_king_found,
		chess_board,self,0,-1,avialable_fields,check_white,check_black,
		king_attack_path)
		#Sprawdzenie dostępnych pól w rzędzie w prawo
		check_move_row(field_right_obstacle_found,
		field_right_king_found,chess_board,self,0,1,avialable_fields,
		check_white,check_black,king_attack_path)
		self.moves=avialable_fields
		#Dopisanie możliwych ruchów do listy pól potencjalnie 
		#szachowanych
		if self.type=="white":
			for move in self.moves:
				check_white.append(move)
		elif self.type=="black":
			for move in self.moves:
				check_black.append(move)


class Knight(Sprite):
	"""Tworzenie skoczka"""
	def __init__(self,piece_type,screen,settings):
		super().__init__()
		self.type=piece_type
		self.picture=Group()
		self.screen=screen
		self.settings=settings
		self.piece_name="knight"
		#Atrybut zawierający pole na jakim obecnie znajduje się figura
		self.field=None
		#Tworzenie rysunku figury z pliku
		load_picture(screen,settings,piece_type,self.piece_name,
		self.picture)
		#Określenie względnej pozycji każego elementu rysunku
		set_position(self.picture)
		#Aktualnie mozliwe ruchy danej figury
		self.moves=None
	def draw_piece(self):
		"""Wyświetlenie wszystkich elementów z których składa się 
		figura"""
		for picture_part in self.picture:
			picture_part.draw_part()
	def relocate(self,board_field):
		"""Zmiana pozycji figury wzgledem podanych parametrów i 
		zapisanie pola na jakim znajduje się figura"""
		self.field=board_field
		for picture_element in self.picture:
			picture_element.rect.centerx=(self.field.rect.centerx+
			picture_element.position_x)
			picture_element.rect.centery=(self.field.rect.centery+
			picture_element.position_y)
		#Przypisanie położenia pola, na którym znajduje się figura
		self.vertical=board_field.vertical
		self.horizontal=board_field.horizontal
	def check_move(self,chess_board,check_white,check_black,
	king_attack_path):
		"""Sprawdzanie pól dostępnych w danym ruchu"""
		avialable_fields=[]
		#Sprawdzenie wszystkich możliwych ruchów konia
		for chess_field in chess_board:
			check_move_jump(self,chess_field,avialable_fields,
			check_white,check_black,1,2,king_attack_path)
			check_move_jump(self,chess_field,avialable_fields,
			check_white,check_black,1,-2,king_attack_path)
			check_move_jump(self,chess_field,avialable_fields,
			check_white,check_black,-1,2,king_attack_path)
			check_move_jump(self,chess_field,avialable_fields,
			check_white,check_black,-1,-2,king_attack_path)
			check_move_jump(self,chess_field,avialable_fields,
			check_white,check_black,2,1,king_attack_path)
			check_move_jump(self,chess_field,avialable_fields,
			check_white,check_black,2,-1,king_attack_path)
			check_move_jump(self,chess_field,avialable_fields,
			check_white,check_black,-2,1,king_attack_path)
			check_move_jump(self,chess_field,avialable_fields,
			check_white,check_black,-2,-1,king_attack_path)
		self.moves=avialable_fields
		#Uzupełnienie listy pól potencjalnie szachowanych wszystkimi 
		#polami, na które skoczek może przejść
		if self.type=="white":
			for move in self.moves:
				check_white.append(move)
		elif self.type=="black":
			for move in self.moves:
				check_black.append(move)


class Bishop(Sprite):
	"""Tworzenie gońca"""
	def __init__(self,piece_type,screen,settings):
		super().__init__()
		self.type=piece_type
		self.picture=Group()
		self.screen=screen
		self.settings=settings
		self.piece_name="bishop"
		#Atrybut zawierający pole na jakim obecnie znajduje się figura
		self.field=None
		#Tworzenie rysunku figury z pliku
		load_picture(screen,settings,piece_type,self.piece_name,
		self.picture)
		#Określenie względnej pozycji każego elementu rysunku
		set_position(self.picture)
		#Aktualnie mozliwe ruchy danej figury
		self.moves=None
	def draw_piece(self):
		"""Wyświetlenie wszystkich elementów z których składa się 
		figura"""
		for picture_part in self.picture:
			picture_part.draw_part()
	def relocate(self,board_field):
		"""Zmiana pozycji figury wzgledem podanych parametrów i 
		zapisanie pola na jakim znajduje się figura"""
		self.field=board_field
		for picture_element in self.picture:
			picture_element.rect.centerx=(self.field.rect.centerx+
			picture_element.position_x)
			picture_element.rect.centery=(self.field.rect.centery+
			picture_element.position_y)
		#Przypisanie położenia pola, na którym znajduje się figura
		self.vertical=board_field.vertical
		self.horizontal=board_field.horizontal
	def check_move(self,chess_board,check_white,check_black,
	king_attack_path):
		"""Sprawdzanie pól dostępnych w danym ruchu"""
		avialable_fields=[]
		#Dodanie zmiennych, które zawierają informację, czy pole w 
		#rzędzie jest zablokowane i czy nie można przesunąć się dalej
		field_NE_obstacle_found=False
		field_NE_king_found=False
		field_SE_obstacle_found=False
		field_SE_king_found=False
		field_SW_obstacle_found=False
		field_SW_king_found=False
		field_NW_obstacle_found=False
		field_NW_king_found=False
		#Sprawdzenie dostępnych pól w rzędzie w na północny-wschód
		check_move_row(field_NE_obstacle_found,field_NE_king_found,
		chess_board,self,1,1,avialable_fields,check_white,check_black,
		king_attack_path)
		#Sprawdzenie dostępnych pól w rzędzie na południowy-wschód
		check_move_row(field_SE_obstacle_found,field_SE_king_found,
		chess_board,self,-1,1,avialable_fields,check_white,check_black,
		king_attack_path)
		#Sprawdzenie dostępnych pól w rzędzie na połódniowy-zachód
		check_move_row(field_SW_obstacle_found,field_SW_king_found,
		chess_board,self,-1,-1,avialable_fields,check_white,check_black,
		king_attack_path)
		#Sprawdzenie dostępnych pól w rzędzie na północny-zachód
		check_move_row(field_NW_obstacle_found,field_NW_king_found,
		chess_board,self,1,-1,avialable_fields,check_white,check_black,
		king_attack_path)
		self.moves=avialable_fields
		#Dopisanie możliwych ruchów do listy pól potencjalnie 
		#szachowanych
		if self.type=="white":
			for move in self.moves:
				check_white.append(move)
		elif self.type=="black":
			for move in self.moves:
				check_black.append(move)


class Queen(Sprite):
	"""Tworzenie królowej"""
	def __init__(self,piece_type,screen,settings):
		super().__init__()
		self.type=piece_type
		self.picture=Group()
		self.screen=screen
		self.settings=settings
		self.piece_name="queen"
		#Atrybut zawierający pole na jakim obecnie znajduje się figura
		self.field=None
		#Tworzenie rysunku figury z pliku
		load_picture(screen,settings,piece_type,self.piece_name,
		self.picture)
		#Określenie względnej pozycji każego elementu rysunku
		set_position(self.picture)
		#Aktualnie mozliwe ruchy danej figury
		self.moves=None
	def draw_piece(self):
		"""Wyświetlenie wszystkich elementów z których składa się 
		figura"""
		for picture_part in self.picture:
			picture_part.draw_part()
	def relocate(self,board_field):
		"""Zmiana pozycji figury wzgledem podanych parametrów i 
		zapisanie pola na jakim znajduje się figura"""
		self.field=board_field
		for picture_element in self.picture:
			picture_element.rect.centerx=(self.field.rect.centerx+
			picture_element.position_x)
			picture_element.rect.centery=(self.field.rect.centery+
			picture_element.position_y)
		#Przypisanie położenia pola, na którym znajduje się figura
		self.vertical=board_field.vertical
		self.horizontal=board_field.horizontal
	def check_move(self,chess_board,check_white,check_black,
	king_attack_path):
		"""Sprawdzanie pól dostępnych w danym ruchu"""
		avialable_fields=[]
		#Dodanie zmiennych, które zawierają informację, czy pole w 
		#rzędzie jest zablokowane i czy nie można przesunąć się dalej
		field_up_obstacle_found=False
		field_up_king_found=False
		field_down_obstacle_found=False
		field_down_king_found=False
		field_left_obstacle_found=False
		field_left_king_found=False
		field_right_obstacle_found=False
		field_right_king_found=False
		field_NE_obstacle_found=False
		field_NE_king_found=False
		field_SE_obstacle_found=False
		field_SE_king_found=False
		field_SW_obstacle_found=False
		field_SW_king_found=False
		field_NW_obstacle_found=False
		field_NW_king_found=False
		#Sprawdzenie dostępnych pól w rzędzie w górę
		check_move_row(field_up_obstacle_found,field_up_king_found,
		chess_board,self,1,0,avialable_fields,check_white,check_black,
		king_attack_path)
		#Sprawdzenie dostępnych pól w rzędzie w dół
		check_move_row(field_down_obstacle_found,field_down_king_found,
		chess_board,self,-1,0,avialable_fields,check_white,check_black,
		king_attack_path)
		#Sprawdzenie dostępnych pól w rzędzie w lewo
		check_move_row(field_left_obstacle_found,field_left_king_found,
		chess_board,self,0,-1,avialable_fields,check_white,check_black,
		king_attack_path)
		#Sprawdzenie dostępnych pól w rzędzie w prawo
		check_move_row(field_right_obstacle_found,
		field_right_king_found,chess_board,self,0,1,avialable_fields,
		check_white,check_black,king_attack_path)
		#Sprawdzenie dostępnych pól w rzędzie na północny-wschód
		check_move_row(field_NE_obstacle_found,field_NE_king_found,
		chess_board,self,1,1,avialable_fields,check_white,check_black,
		king_attack_path)
		#Sprawdzenie dostępnych pól w rzędzie na południowy-wschód
		check_move_row(field_SE_obstacle_found,field_SE_king_found,
		chess_board,self,-1,1,avialable_fields,check_white,check_black,
		king_attack_path)
		#Sprawdzenie dostępnych pól w rzędzie na południowy-zachód
		check_move_row(field_SW_obstacle_found,field_SW_king_found,
		chess_board,self,-1,-1,avialable_fields,check_white,check_black,
		king_attack_path)
		#Sprawdzenie dostępnych pól w rzędzie na północny-zachód
		check_move_row(field_NW_obstacle_found,field_NW_king_found,
		chess_board,self,1,-1,avialable_fields,check_white,check_black,
		king_attack_path)
		self.moves=avialable_fields
		#Dopisanie możliwych ruchów do listy pól potencjalnie 
		#szachowanych
		if self.type=="white":
			for move in self.moves:
				check_white.append(move)
		elif self.type=="black":
			for move in self.moves:
				check_black.append(move)


class King(Sprite):
	"""Tworzenie króla"""
	def __init__(self,piece_type,screen,settings):
		super().__init__()
		self.type=piece_type
		self.picture=Group()
		self.screen=screen
		self.settings=settings
		self.piece_name="king"
		#Atrybut zawierający pole na jakim obecnie znajduje się figura
		self.field=None
		#Tworzenie rysunku figury z pliku
		load_picture(screen,settings,piece_type,self.piece_name,
		self.picture)
		#Określenie względnej pozycji każego elementu rysunku
		set_position(self.picture)
		#Aktualnie mozliwe ruchy danej figury
		self.moves=None
	def draw_piece(self):
		"""Wyświetlenie wszystkich elementów z których składa się 
		figura"""
		for picture_part in self.picture:
			picture_part.draw_part()
	def relocate(self,board_field):
		"""Zmiana pozycji figury wzgledem podanych parametrów i 
		zapisanie pola na jakim znajduje się figura"""
		self.field=board_field
		for picture_element in self.picture:
			picture_element.rect.centerx=(self.field.rect.centerx+
			picture_element.position_x)
			picture_element.rect.centery=(self.field.rect.centery+
			picture_element.position_y)
		#Przypisanie położenia pola, na którym znajduje się figura
		self.vertical=board_field.vertical
		self.horizontal=board_field.horizontal
	def check_move(self,chess_board,check_white,check_black,
	king_attack_path):
		"""Sprawdzanie pól dostępnych w danym ruchu"""
		avialable_fields=[]
		#Sprawdzenie wszystkich ruchów dostępnych dla króla
		for chess_field in chess_board:
			check_move_jump(self,chess_field,avialable_fields,
			check_white,check_black,0,1,king_attack_path)
			check_move_jump(self,chess_field,avialable_fields,
			check_white,check_black,1,1,king_attack_path)
			check_move_jump(self,chess_field,avialable_fields,
			check_white,check_black,1,0,king_attack_path)
			check_move_jump(self,chess_field,avialable_fields,
			check_white,check_black,1,-1,king_attack_path)
			check_move_jump(self,chess_field,avialable_fields,
			check_white,check_black,0,-1,king_attack_path)
			check_move_jump(self,chess_field,avialable_fields,
			check_white,check_black,-1,-1,king_attack_path)
			check_move_jump(self,chess_field,avialable_fields,
			check_white,check_black,-1,0,king_attack_path)
			check_move_jump(self,chess_field,avialable_fields,
			check_white,check_black,-1,1,king_attack_path)
		self.moves=avialable_fields
		#Dopisanie możliwych ruchów do listy pól potencjalnie 
		#szachowanych
		if self.type=="white":
			for move in self.moves:
				check_white.append(move)
		elif self.type=="black":
			for move in self.moves:
				check_black.append(move)
