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

CARD_HEIGHT = 270
CARD_WIDTH = 193
BUFFER = 2

SMALL_CARD_HEIGHT = 240
SMALL_CARD_WIDTH = 172
SMALL_BUFFER = 25

N_COMMONS = 10
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
#----------------------------------CLASSES AND FUNCTIONS----------------------------------#
###########################################################################################
class Card():
	def __init__(self, x, y, img, name, rarity):
		self.x = x
		self.y = y
		self.img = img
		self.scale_img = pygame.transform.scale(self.img, (CARD_WIDTH, CARD_HEIGHT))
		self.name = name
		self.rarity = rarity
	
		c = self.img.get_at((374-38, 31))
		if c[0] in range(180,191) and c[1] in range(181, 191) and c[2] in range(180,191):
			self.color = "black"	
		elif c[0] in range(246,257) and c[1] in range(246, 257) and c[2] in range(211,222):
			self.color = "white"		
		elif c[0] in range(240,251) and c[1] in range(163, 174) and c[2] in range(139,150):
			self.color = "red"	
		elif c[0] in range(130,162) and c[1] in range(190, 220) and c[2] in range(155,180):
			self.color = "green"	
		elif c[0] in range(163,174) and c[1] in range(218, 229) and c[2] in range(242,253):
			self.color = "blue"		
		elif c[0] in range(198,209) and c[1] in range(188, 199) and c[2] in range(185,196):
			self.color = "gray"	
				
		
def adjust_pack(pack):
	for j, card in enumerate(pack):	
		card.x = int(j%5)*(CARD_WIDTH+BUFFER)
		card.y = int(j/5)*(CARD_HEIGHT+BUFFER)
	
def display_pack(pack):
	adjust_pack(pack)
	for card in pack:		
		rect = card.scale_img.get_rect()
		rect.x = card.x
		rect.y = card.y
		screen.blit(card.scale_img, rect)

def display_deck(deck):
	textsurface = FONT_1.render("Your Picks:", False, (0, 0, 0))
	screen.blit(textsurface,(WIDTH-SMALL_CARD_WIDTH-30, 0))	
	
	for k, card in enumerate(deck):	
		card.x = WIDTH - SMALL_CARD_WIDTH - 40 + (100 * int(k/25))
		card.y = ((k%25)+1)*SMALL_BUFFER
		
		img = pygame.transform.scale(card.img, (SMALL_CARD_WIDTH, SMALL_CARD_HEIGHT))
		rect = img.get_rect()
		rect.x = card.x
		rect.y = card.y
		screen.blit(img, rect)

def display_deck_alpha(deck):
	deck.sort(key=lambda c: c.name)
	for k, card in enumerate(deck):	
		card.x = (int(SMALL_CARD_WIDTH/2-12) * (k%15))
		card.y = int(k/15)*SMALL_CARD_HEIGHT
		
		img = pygame.transform.scale(card.img, (SMALL_CARD_WIDTH, SMALL_CARD_HEIGHT))
		rect = img.get_rect()
		rect.x = card.x
		rect.y = card.y
		screen.blit(img, rect)

def clicked_card_index(pos, current_pack):
	for index, card in enumerate(current_pack):	
		if pos[0] >= card.x and pos[0] <= card.x + CARD_WIDTH and pos[1] >= card.y and pos[1] <= card.y + CARD_HEIGHT:
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
				   "blue":0,  #BLUE
				   "gray":0 } #GRAY	

	for card in bot_deck:
		c = card.img.get_at((374-38, 31))
		if c[0] in range(180,191) and c[1] in range(181, 191) and c[2] in range(180,191):
			colors_dict["black"] += 1		
		elif c[0] in range(246,257) and c[1] in range(246, 257) and c[2] in range(211,222):
			colors_dict["white"] += 1		
		elif c[0] in range(240,251) and c[1] in range(163, 174) and c[2] in range(139,150):
			colors_dict["red"] += 1		
		elif c[0] in range(130,162) and c[1] in range(190, 220) and c[2] in range(155,180):
			colors_dict["green"] += 1		
		elif c[0] in range(163,174) and c[1] in range(218, 229) and c[2] in range(242,253):
			colors_dict["blue"] += 1		
		elif c[0] in range(198,209) and c[1] in range(188, 199) and c[2] in range(185,196):
			colors_dict["gray"] += 1	
		else:
			print(card.name, str(card.img.get_at((374-38, 31))))
	
	color = max(colors_dict, key=colors_dict.get)
	colors_dict[color] = 1
	color2 = max(colors_dict, key=colors_dict.get)
	
	for i, card in enumerate(bot_pack):
		if card.color == color:
			return i
	for i, card in enumerate(bot_pack):
		if card.color == color2:
			return i
	
	return 0
	#return randint(0,len(bots_pack)-1)
	
##########################################################################################
#----------------------------------------SET UP------------------------------------------#
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
						decks[0].append(current_pack.pop(ind))
				
						#Bots make their choice
						for i in range(1,8):
							bots_pack = packs[(i+pick_num)%8]
							selected = bot_choice(decks[i], bots_pack)
							decks[i].append(bots_pack.pop(selected))
						next = True
		
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()

			#Draw
			screen.fill(BACKGROUND)

			display_pack(current_pack)

			display_deck(decks[0])

			pygame.display.flip()
			clock.tick(60)

		pick_num += 1
		current_pack = packs[pick_num%8]

##########################################################################################
#-------------------------------------DECK BUILDING--------------------------------------#
##########################################################################################
done = False	
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
			if event.key == pygame.K_ESCAPE:
				done = True
				pygame.quit()

	#Draw
	screen.fill(BACKGROUND)

	display_deck_alpha(decks[0])
	
	pygame.display.flip()
	clock.tick(60)
		
pygame.quit()
exit()

	