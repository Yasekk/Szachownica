import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
import json
def load_picture(screen,settings,piece_type,piece_name,picture):
	"""Wczytywanie obrazku figury"""
	with open("Pictures/"+piece_type+"_"+piece_name+".json","r") as (
	picture_load):
		#Wczytywanie danych z pliku pasującego do nazwy konkretnej
		#figury i odtwarzanie z nich rysunku figury
		picture_data=json.load(picture_load)
		for picture_element_data in picture_data:
			picture_element=PiecePart(screen,
			settings,picture_element_data[1])
			picture_element.rect.center=picture_element_data[0]
			picture.add(picture_element)
def set_position(picture):
	"""Ustalenie wzglednego położenia każdego elementu rysunku w
	stosunku do środka rysunku"""
	positions_x=[]
	positions_y=[]
	#Ustalenie skrajnych wartości pozycji elementów i wyliczenie ich 
	#połów (które w pionie i poziomie określą środek rysuknu)
	for picture_part in picture:
		positions_x.append(picture_part.rect.centerx)
		positions_y.append(picture_part.rect.centery)
	center_x=(min(positions_x)+max(positions_x))/2
	center_y=(min(positions_y)+max(positions_y))/2
	#Określenie pozycji każdego elementów rysunku względem środka
	for picture_part in picture:
		picture_part.position_x=picture_part.rect.centerx-center_x
		picture_part.position_y=picture_part.rect.centery-center_y
class PiecePart(Sprite):
	"""Tworzenie sprite'ów, z których będą składały się figury"""
	def __init__(self,screen,settings,color):
		super().__init__()
		self.screen=screen
		self.screen_rect=screen.get_rect()
		#Wymiary są nieco większe niż wyliczone proporcje, żeby
		#zaokrąglenia do liczb całkowitych nie tworzyły dziur
		self.rect=pygame.Rect(0,0,settings.width_grid*1.1,
		settings.height_grid*1.1)
		self.color=color
		#Dodanie atrybutów, które będą zawierały informację o wzglednym
		#położeniu elementu w stosunku do środka rysunku
		self.position_x=None
		self.postion_y=None
	def draw_part(self):
		"""Wyświetlenie elementu rysunku"""
		pygame.draw.rect(self.screen,self.color,self.rect)
class Pawn(Sprite):
	"""Tworzenie pionka"""
	def __init__(self,piece_type,screen,settings):
		super().__init__()
		self.type=piece_type
		self.picture=Group()
		self.screen=screen
		self.settings=settings
		self.piece_name="pawn"
		self.type=piece_type
		#Upewnienie się, że ruch o dwa pola będzie mozliwy tylko
		#raz
		self.first_move=True
		#Atrybut zawierający położenie w jakim obecnie znajduje się 
		#figura
		self.vertical=None
		self.horizontal=None
		#Tworzenie rysunku figury z pliku
		load_picture(screen,settings,piece_type,self.piece_name,
		self.picture)
		#Określenie względnej pozycji każego elementu rysunku
		set_position(self.picture)
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
	def check_move(self,chess_board):
		"""Sprawdzanie pól dostępnych w danym ruchu"""
		avialable_fields=[]
		#Ruch dla pionów białych
		if self.type=="white":
			if self.first_move==True:
				#W pierwszym ruchu mozna poruszyć się pionem o jedno lub
				#dwa pola do przodu
				for chess_field in chess_board:
					#Znalezienie pól na szachownicy, które mają takie 
					#samo położenie poziome co obecnie zajmowane i jedno
					#lub dwa pola wyższe
					if (chess_field.vertical==self.vertical+1 and 
					chess_field.horizontal==self.horizontal):
						avialable_fields.append(chess_field.name)
					elif (chess_field.vertical==self.vertical+2 and 
					chess_field.horizontal==self.horizontal):
						avialable_fields.append(chess_field.name)
					#Zapamiętanie, że figura wykonała już pierwszy ruch
					self.first_move=False
			else:
				#W drugim ruchu można poruszyć się o jedno wolne pole do
				#przodu albo zbić przeciwną figurę po skosie
				for chess_field in chess_board:
					if (chess_field.vertical==self.vertical+1 and 
					chess_field.horizontal==self.horizontal and 
					chess_field.occupied==None):
						avialable_fields.append(chess_field.name)
					elif (chess_field.vertical==self.vertical+1 and 
					chess_field.horizontal==self.horizontal+1 and 
					chess_field.occupied!=None and 
					chess_field.occupied.type!=self.type):
						avialable_fields.append(chess_field.name)
					elif (chess_field.vertical==self.vertical+1 and 
					chess_field.horizontal==self.horizontal-1 and 
					chess_field.occupied!=None and 
					chess_field.occupied.type!=self.type):
						avialable_fields.append(chess_field.name)
		#Ruch dla pionów czarnych
		if self.type=="black":
			if self.first_move==True:
				#W pierwszym ruchu mozna poruszyć się pionem o jedno lub
				#dwa pola do przodu
				for chess_field in chess_board:
					#Znalezienie pól na szachownicy, które mają takie 
					#samo położenie poziome co obecnie zajmowane i jedno
					#lub dwa pola niższe
					if (chess_field.vertical==self.vertical-1 and 
					chess_field.horizontal==self.horizontal):
						avialable_fields.append(chess_field.name)
					elif (chess_field.vertical==self.vertical-2 and 
					chess_field.horizontal==self.horizontal):
						avialable_fields.append(chess_field.name)
					self.first_move=False
			else:
				#W drugim ruchu można poruszyć się o jedno wolne pole do
				#przodu albo zbić przeciwną figurę po skosie
				for chess_field in chess_board:
					if (chess_field.vertical==self.vertical-1 and 
					chess_field.horizontal==self.horizontal and 
					chess_field.occupied==None):
						avialable_fields.append(chess_field.name)
					elif (chess_field.vertical==self.vertical-1 and 
					chess_field.horizontal==self.horizontal+1 and 
					chess_field.occupied!=None and 
					chess_field.occupied.type!=self.type):
						avialable_fields.append(chess_field.name)
					elif (chess_field.vertical==self.vertical-1 and 
					chess_field.horizontal==self.horizontal-1 and 
					chess_field.occupied!=None and 
					chess_field.occupied.type!=self.type):
						avialable_fields.append(chess_field.name)	
		return avialable_fields
		
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
	def check_move(self,chess_board):
		"""Sprawdzanie pól dostępnych w danym ruchu"""
		avialable_fields=[]
		#Dodanie zmiennych, które zawierają informację, czy pole w 
		#rzędzie jest zablokowane i czy nie można przesunąć się dalej
		field_up_obstacle_found=False
		field_down_obstacle_found=False
		field_left_obstacle_found=False
		field_right_obstacle_found=False
		#Sprawdzenie dostępnych pól w rzędzie w górę
		for next_field_up in range(1,8):
			#Zaprzestanie szukania w danym rzędzie, jeżeli natafiło się
			#już na inną figurę
			if field_up_obstacle_found==True:
				break
			#Szukanie pól, które mają kolejne pozycje w danym rzedzie
			for chess_field in chess_board:
				if (chess_field.vertical==self.vertical+next_field_up 
				and chess_field.horizontal==self.horizontal):
					if chess_field.occupied:
						#Jeżeli pole jest zajęte przez figurę innego
						#koloru, będzie możliwe stanie na tym polu, ale 
						#nie dalej
						if chess_field.occupied.type!=self.type:
							avialable_fields.append(chess_field.name)
							field_up_obstacle_found=True
							break
						#Jezeli pole jest zajęte przez figurę tego
						#samego koloru, nie będzie mozna zając tego
						#pola ani żadnego dalszego
						elif chess_field.occupied.type==self.type:
							field_up_obstacle_found=True
							break
					#Pozostałe wolne pola są dodane do puli możliwych
					#ruchów
					else:
						avialable_fields.append(chess_field.name)
		#Sprawdzenie dostępnych pól w rzędzie w dół
		for next_field_down in range(1,8):
			#Zaprzestanie szukania w danym rzędzie, jeżeli natafiło się
			#już na inną figurę
			if field_down_obstacle_found==True:
				break
			#Szukanie pól, które mają kolejne pozycje w danym rzedzie
			for chess_field in chess_board:
				if (chess_field.vertical==self.vertical-next_field_down 
				and chess_field.horizontal==self.horizontal):
					if chess_field.occupied:
						#Jeżeli pole jest zajęte przez figurę innego
						#koloru, będzie możliwe stanie na tym polu, ale 
						#nie dalej
						if chess_field.occupied.type!=self.type:
							avialable_fields.append(chess_field.name)
							field_down_obstacle_found=True
							break
						#Jezeli pole jest zajęte przez figurę tego
						#samego koloru, nie będzie mozna zając tego
						#pola ani żadnego dalszego
						elif chess_field.occupied.type==self.type:
							field_down_obstacle_found=True
							break
					#Pozostałe wolne pola są dodane do puli możliwych
					#ruchów
					else:
						avialable_fields.append(chess_field.name)
		#Sprawdzenie dostępnych pól w rzędzie w lewo
		for next_field_left in range(1,8):
			#Zaprzestanie szukania w danym rzędzie, jeżeli natafiło się
			#już na inną figurę
			if field_left_obstacle_found==True:
				break
			#Szukanie pól, które mają kolejne pozycje w danym rzedzie
			for chess_field in chess_board:
				if (
				chess_field.horizontal==self.horizontal-next_field_left 
				and chess_field.vertical==self.vertical):
					if chess_field.occupied:
						#Jeżeli pole jest zajęte przez figurę innego
						#koloru, będzie możliwe stanie na tym polu, ale 
						#nie dalej
						if chess_field.occupied.type!=self.type:
							avialable_fields.append(chess_field.name)
							field_left_obstacle_found=True
							break
						#Jezeli pole jest zajęte przez figurę tego
						#samego koloru, nie będzie mozna zając tego
						#pola ani żadnego dalszego
						elif chess_field.occupied.type==self.type:
							field_left_obstacle_found=True
							break
					#Pozostałe wolne pola są dodane do puli możliwych
					#ruchów
					else:
						avialable_fields.append(chess_field.name)
		#Sprawdzenie dostępnych pól w rzędzie w prawo
		for next_field_right in range(1,8):
			#Zaprzestanie szukania w danym rzędzie, jeżeli natafiło się
			#już na inną figurę
			if field_right_obstacle_found==True:
				break
			#Szukanie pól, które mają kolejne pozycje w danym rzedzie
			for chess_field in chess_board:
				if (
				chess_field.horizontal==self.horizontal+next_field_right 
				and chess_field.vertical==self.vertical):
					if chess_field.occupied:
						#Jeżeli pole jest zajęte przez figurę innego
						#koloru, będzie możliwe stanie na tym polu, ale 
						#nie dalej
						if chess_field.occupied.type!=self.type:
							avialable_fields.append(chess_field.name)
							field_right_obstacle_found=True
							break
						#Jezeli pole jest zajęte przez figurę tego
						#samego koloru, nie będzie mozna zając tego
						#pola ani żadnego dalszego
						elif chess_field.occupied.type==self.type:
							field_right_obstacle_found=True
							break
					#Pozostałe wolne pola są dodane do puli możliwych
					#ruchów
					else:
						avialable_fields.append(chess_field.name)
		return avialable_fields
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
