from random import choice
from random import randint
import pygame
import numpy as np
import os

###########################################################################################
#-----------------------------------------SETUP-------------------------------------------#
###########################################################################################

#colors
BACKGROUND = (255, 255, 255, 255)
BLACK = (185, 186, 185, 255)
WHITE = (251, 251, 216, 255)
RED = (245, 168, 144, 255)
GREEN = (156, 208, 169, 255)
BLUE = (168, 223, 247, 255)
GRAY = (203, 193, 190, 255)

#Define some constants
PI = 3.1415926536
WIDTH = 1200
HEIGHT = 700

OG_CARD_HEIGHT = 522
OG_CARD_WIDTH = 375

CARD_HEIGHT = int(OG_CARD_HEIGHT*.335)
CARD_WIDTH = int(OG_CARD_WIDTH*.333)
WRAP = 8
BUFFER = 2

SMALL_CARD_HEIGHT = int(OG_CARD_HEIGHT*.2)
SMALL_CARD_WIDTH = int(OG_CARD_WIDTH*.2)
SMALL_WRAP = 15
SMALL_BUFFER = 1

SORTED_CARD_HEIGHT = int(OG_CARD_HEIGHT*.265)
SORTED_CARD_WIDTH = int(OG_CARD_WIDTH*.265)
SORTED_WRAP = 12
SORTED_BUFFER = 1

N_COMMONS = 11
N_UNCOMMONS = 3
N_RARES = 1

#PyGame Setup
pygame.init()

# Set the width and height of the screen [width,height]
size = [WIDTH, HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Draft Sim")
clock = pygame.time.Clock()

#Fonts
FONT_1 = pygame.font.SysFont('Matrix Bold', 40)
FONT_2 = pygame.font.SysFont('MPlantin', 40)
		
###########################################################################################
#-----------------------------------------CLASSES-----------------------------------------#
###########################################################################################
class Card():
	def __init__(self, x, y, img, name, rarity):
		self.x = x
		self.y = y
		self.img = img
		self.scale_img = pygame.transform.scale(self.img, (CARD_WIDTH, CARD_HEIGHT))
		self.name = name
		self.rarity = rarity
		self.large = False
	
		c = self.img.get_at((374-38, 31))
		
		if pix_color(c) == None:
			print(self.img.get_at((374-38, 31)))
		elif pix_color(c) == "gray":
			self.color = "z_gray"
		else:
			self.color = pix_color(c)

		
		c2 = self.img.get_at((374-58, 31))
		
		if pix_color(c2) == None or pix_color(c2) == "gray":
			self.color2 = "aaa"
		else:
			self.color2 = pix_color(c2)
			
			
###########################################################################################
#----------------------------------------FUNCTIONS----------------------------------------#
###########################################################################################			
		
def adjust_pack(pack):
	for j, card in enumerate(pack):	
		card.x = int(j%WRAP)*(CARD_WIDTH+BUFFER)
		card.y = int(j/WRAP)*(CARD_HEIGHT+BUFFER)
	
def display_pack(pack):
	adjust_pack(pack)
	for card in pack:		
		if card.large ==False:
			rect = card.scale_img.get_rect()
			rect.x = card.x
			rect.y = card.y
			screen.blit(card.scale_img, rect)
	
	for card in pack:		
		if card.large ==True:
			rect = card.img.get_rect()
			rect.x = min(card.x, WIDTH-OG_CARD_WIDTH)
			rect.y = min(card.y, HEIGHT-OG_CARD_HEIGHT)
			screen.blit(card.img, rect)

def display_deck(deck):
	textsurface = FONT_1.render("Your Picks (Hover + Space to zoom):", False, (0, 0, 0))
	screen.blit(textsurface,(0, 2*CARD_HEIGHT+15))	
	
	for k, card in enumerate(deck):	
		if card.large == False:
			card.x = int(k%SMALL_WRAP)*(SMALL_CARD_WIDTH + SMALL_BUFFER)
			card.y = CARD_HEIGHT*2 + 40 + int(k/SMALL_WRAP)*(SMALL_CARD_HEIGHT+SMALL_BUFFER)
		
			#card.x = WIDTH - SMALL_CARD_WIDTH - 40 + (100 * int(k/25))
			#card.y = ((k%25)+1)*SMALL_BUFFER
		
			img = pygame.transform.scale(card.img, (SMALL_CARD_WIDTH, SMALL_CARD_HEIGHT))
			rect = img.get_rect()
			rect.x = card.x
			rect.y = card.y
			screen.blit(img, rect)
	
	for k, card in enumerate(deck):	
		if card.large == True:
			card.x = min(int(k%SMALL_WRAP)*(SMALL_CARD_WIDTH + SMALL_BUFFER), WIDTH-OG_CARD_WIDTH) 
			card.y = HEIGHT - OG_CARD_HEIGHT

			#card.x = WIDTH - SMALL_CARD_WIDTH - 40 + (100 * int(k/25))
			#card.y = ((k%25)+1)*SMALL_BUFFER
		
			img = card.img#pygame.transform.scale(card.img, (SMALL_CARD_WIDTH, SMALL_CARD_HEIGHT))
			rect = img.get_rect()
			rect.x = card.x
			rect.y = card.y
			screen.blit(img, rect)

def display_deck_sorted(deck, deck_number):
	#deck.sort(key=lambda c: c.name)
	deck.sort(key=lambda c: (c.color2, c.color, c.name))
	
	if deck_number == 0:
		textsurface = FONT_1.render("Your picks: (use L/R keys to see bot decks)", False, (0, 0, 0))
	else:
		textsurface = FONT_1.render("(use L/R keys) Bot # " + str(deck_number) + "'s picks:", False, (0, 0, 0))
	screen.blit(textsurface,((0,15)))	
	
	for k, card in enumerate(deck):	
		if card.large == False:
			card.x = int(k%SORTED_WRAP)*(SORTED_CARD_WIDTH + SORTED_BUFFER)
			card.y = 40 + int(k/SORTED_WRAP)*(SORTED_CARD_HEIGHT+SORTED_BUFFER)
		
			#card.x = WIDTH - SMALL_CARD_WIDTH - 40 + (100 * int(k/25))
			#card.y = ((k%25)+1)*SMALL_BUFFER
		
			img = pygame.transform.scale(card.img, (SORTED_CARD_WIDTH, SORTED_CARD_HEIGHT))
			rect = img.get_rect()
			rect.x = card.x
			rect.y = card.y
			screen.blit(img, rect)
	
	for k, card in enumerate(deck):	
		if card.large == True:
			card.x = min(int(k%SORTED_WRAP)*(SORTED_CARD_WIDTH + SORTED_BUFFER), WIDTH-OG_CARD_WIDTH) 
			card.y = min(40 + int(k/SORTED_WRAP)*(SORTED_CARD_HEIGHT+SORTED_BUFFER), HEIGHT - OG_CARD_HEIGHT)

			#card.x = WIDTH - SMALL_CARD_WIDTH - 40 + (100 * int(k/25))
			#card.y = ((k%25)+1)*SMALL_BUFFER
		
			img = card.img#pygame.transform.scale(card.img, (SMALL_CARD_WIDTH, SMALL_CARD_HEIGHT))
			rect = img.get_rect()
			rect.x = card.x
			rect.y = card.y
			screen.blit(img, rect)

def clicked_card_index(pos, current_pack):
	for index, card in enumerate(current_pack):	
		if pos[0] >= card.x and pos[0] <= card.x + CARD_WIDTH and pos[1] >= card.y and pos[1] <= card.y + CARD_HEIGHT:
			return index	
	return None

def clicked_small_card_index(pos, current_pack):
	for index, card in enumerate(current_pack):	
		if pos[0] >= card.x and pos[0] <= card.x + SMALL_CARD_WIDTH and pos[1] >= card.y and pos[1] <= card.y + SMALL_CARD_HEIGHT:
			return index	
	return None
	
def clicked_sorted_card_index(pos, current_pack):
	for index, card in enumerate(current_pack):	
		if pos[0] >= card.x and pos[0] <= card.x + SORTED_CARD_WIDTH and pos[1] >= card.y and pos[1] <= card.y + SORTED_CARD_HEIGHT:
			return index	
	return None

def bot_choice(bot_deck, bot_pack):
	
	#First pick the rare
	if len(bot_deck) == 0:
		return 0
		
	#If deck is less than 3 cards, rare draft
	elif len(bot_deck) < 5:		
		for i, card in enumerate(bot_pack):
			if card.rarity == "rare":
				return i
		
	#If there is no rare, or we are not just rare drafting, choose based on color
	colors_dict = {"black":0,  #BLACK
				   "white":0,  #WHITE
				   "red":0,  #RED
				   "green":0,  #GREEN
				   "blue":0} #GRAY	

	for card in bot_deck:
		c = card.img.get_at((374-38, 31))
		color = pix_color(c)
		
		if color == "black":
			colors_dict["black"] += 1		
		elif color == "white":
			colors_dict["white"] += 1		
		elif color == "red":
			colors_dict["red"] += 1		
		elif color == "green":
			colors_dict["green"] += 1		
		elif color == "blue":
			colors_dict["blue"] += 1	
		elif color == "gray":
			pass	
		else:
			print(card.name, str(card.img.get_at((374-38, 31))))
		
		c2 = card.img.get_at((374-58, 31))
		color2 = pix_color(c2)
		if color2 == "black":
			colors_dict["black"] += 1		
		elif color2 == "white":
			colors_dict["white"] += 1		
		elif color2 == "red":
			colors_dict["red"] += 1		
		elif color2 == "green":
			colors_dict["green"] += 1		
		elif color2 == "blue":
			colors_dict["blue"] += 1	
	
	color = max(colors_dict, key=colors_dict.get)
	colors_dict[color] = 1
	color2 = max(colors_dict, key=colors_dict.get)
	
	for i, card in enumerate(bot_pack):
		if card.color == color:
			return i
	for i, card in enumerate(bot_pack):
		if card.color == color2:
			return i
	for i, card in enumerate(bot_pack):
		if card.color == "gray":
			return i
	
	return 0

def pix_color(c):
		if c[0] in range(180,191) and c[1] in range(181, 191) and c[2] in range(180,191):
			return("black")	
		elif c[0] in range(246,257) and c[1] in range(246, 257) and c[2] in range(211,222):
			return "white"	
		elif c[0] in range(240,251) and c[1] in range(163, 174) and c[2] in range(139,150):
			return "red"
		elif c[0] in range(130,162) and c[1] in range(185, 220) and c[2] in range(150,180):
			return "green"	
		elif c[0] in range(163,174) and c[1] in range(218, 229) and c[2] in range(242,253):
			return "blue"	
		elif c[0] in range(198,209) and c[1] in range(188, 199) and c[2] in range(185,196):
			return "gray"	
		else:
			return None
			
##########################################################################################
#-----------------------------------------SETUP------------------------------------------#
##########################################################################################

#Create list of cards (by rarity). Each item is of the form (img, "name")
commons = [(pygame.image.load("images/commons/"+file), file[0:-4]) for file in os.listdir("images/commons")]
uncommons = [(pygame.image.load("images/uncommons/"+file), file[0:-4]) for file in os.listdir("images/uncommons")]
rares = [(pygame.image.load("images/rares/"+file), file[0:-4]) for file in os.listdir("images/rares")]

# 8 empty decks are created
decks = [[] for i in range(8)]

##########################################################################################
#--------------------------------------BEGIN DRAFT---------------------------------------#
##########################################################################################

current_deck = 0
for open_pack in range(3):

	# 8 Packs are randomly created
	packs = [[] for i in range(8)]

	for i in range(8):
		for j in range(N_RARES):
			ch = randint(0, len(rares)-1)
			packs[i].append(Card(None, None, rares[ch][0], rares[ch][1], "rare"))
		for j in range(N_UNCOMMONS):
			ch = randint(0, len(uncommons)-1)
			packs[i].append(Card(None, None, uncommons[ch][0], uncommons[ch][1], "uncommon"))
		for j in range(N_COMMONS):
			ch = randint(0, len(commons)-1)
			packs[i].append(Card(None, None, commons[ch][0], commons[ch][1], "common"))
	
	pick_num = 0
	current_pack = packs[pick_num]

	while len(current_pack) > 0:

		adjust_pack(current_pack)
		next = False
	
		while next == False:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
		
				elif event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					ind = clicked_card_index(pos, current_pack)
					if ind != None:
						decks[current_deck].append(current_pack.pop(ind))
				
						#Bots make their choice
						for i in range(1,8):
							bots_pack = packs[(i+pick_num)%8]
							selected = bot_choice(decks[i], bots_pack)
							decks[i].append(bots_pack.pop(selected))
						next = True

		
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						pos = pygame.mouse.get_pos()
						ind = clicked_card_index(pos, current_pack)
						if ind != None:
							current_pack[ind].large = True
						else:
							ind = clicked_small_card_index(pos, decks[current_deck])
							if ind != None:
								decks[current_deck][ind].large = True
						
					elif event.key == pygame.K_ESCAPE:
						pygame.quit()
				
				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_SPACE:
						for card in current_pack:
							card.large = False
						for card in decks[current_deck]:
							card.large = False

			#Draw
			screen.fill(BACKGROUND)
			
			display_deck_first = False
			for card in current_pack:
				if card.large == True:
					display_deck_first = True
			
			if display_deck_first == True:
				display_deck(decks[current_deck])
				display_pack(current_pack)
			else:
				display_pack(current_pack)
				display_deck(decks[current_deck])


			pygame.display.flip()
			clock.tick(60)

		pick_num += 1
		current_pack = packs[pick_num%8]

##########################################################################################
#-------------------------------------DECK BUILDING--------------------------------------#
##########################################################################################
done = False	
current_deck = 0
while done == False:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
			pygame.quit()
	
		elif event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			#ind = clicked_card_index(pos, current_pack)
			#if ind != None:
			#	decks[0].append(current_pack.pop(ind))
			
				#Bots make their choice
			#	for i in range(1,8):
			#		bots_pack = packs[(i+pick_num)%8]
			#		selected = bot_choice(decks[i], bots_pack)
			#		decks[i].append(bots_pack.pop(selected))
			#	next = True

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				pos = pygame.mouse.get_pos()
				ind = clicked_sorted_card_index(pos, decks[current_deck])
				if ind != None:
					decks[current_deck][ind].large = True
				
			elif event.key == pygame.K_RIGHT:
				current_deck += 1
				current_deck = current_deck % 8
		
			elif event.key == pygame.K_LEFT:
				if current_deck > 0:
					current_deck -= 1
				
				else:
					current_deck = 7
				
			elif event.key == pygame.K_ESCAPE:
				pygame.quit()
		
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				for card in decks[current_deck]:
					card.large = False

	#Draw
	screen.fill(BACKGROUND)
	display_deck_sorted(decks[current_deck], current_deck)
	
	pygame.display.flip()
	clock.tick(60)
		
pygame.quit()
exit()

	