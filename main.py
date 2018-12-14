#An object oriented program which recreates the classic game of Tetris in a text based interface.
#SSAD and Project Assignment 1
#Anubhab Sen 201501114

from random import randrange as rand
from Board import Board
from Block import Block
import os
import pygame
import math
import sys
import time
from constants import *

class Gameplay(Block, Board):
	def __init__(self):
		pygame.init()
		rowscounter = 0
		pygame.key.set_repeat(250, 25)
		self.rlim = cellSize * columns
		self.default_font =  pygame.font.Font(pygame.font.get_default_font(), 17)
		self.nextBlock = tetrisShapes[rand(len(tetrisShapes))]
		self.height = cellSize * rows
		self.bground_grid = [[0 for x in range(columns)]for y in range(rows)]
		for i in range(rows):
			for j in range(columns):
				if(i % 2 == j % 2):
					self.bground_grid[i][j] = 8
		self.width = cellSize * (columns + 8)
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.limit = self.rlim
		self.initialiseGame()

	def updateScore(self, increment):
		self.score += increment

	def initialiseGame(self):
		self.board = self.newBoard()
		self.newBlock()
		self.level = initLevel
		self.score = initScore
		self.lines = initLines
		if(self.level == 1):
			pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
		elif(self.level == 2):
			pygame.time.set_timer(pygame.USEREVENT + 1, 800)
		elif(self.level == 3):
			pygame.time.set_timer(pygame.USEREVENT + 1, 600)
		elif(self.level == 4):
			pygame.time.set_timer(pygame.USEREVENT + 1, 400)
		elif(self.level == 5):
			pygame.time.set_timer(pygame.USEREVENT + 1, 200)
		else:
			pygame.time.set_timer(pygame.USEREVENT + 1, 100)

	def centreMsg(self, msg):
		for i, line in enumerate(msg.splitlines()):
			self.default_font.render(line, False, (254, 254, 254), (1, 1, 1))
			msgim_center_x = self.default_font.render(line, False, (254, 254, 254), (1, 1, 1)).get_size()[0]
			msgim_center_y = self.default_font.render(line, False, (254, 254, 254), (1, 1, 1)).get_size()[1]
			msgim_center_x = (int) (msgim_center_x / 2)
			msgim_center_y = (int) (msgim_center_x / 2)
			self.screen.blit(self.default_font.render(line, False, (254, 254, 254), (1, 1, 1)), ((int)(self.width / 2) - msgim_center_x, (int)(self.height / (trial - 10)) - msgim_center_y + i * (trial + 10)))

	def dispMsg(self, msg, topleft):
		x = topleft[0]
		y = topleft[1]
		trial = 12
		for line in msg.splitlines():
			arg = False
			self.screen.blit(self.default_font.render(line, arg, (white, white, white), (1, 1, 1)), (x, y))
			y += 14

	def addClearedLines(self, n):
		linescores = [0, 100, 100, 100, 100]
		self.lines = self.lines + n
		self.updateScore(linescores[n] * self.level)
		if(self.lines >= self.level * lvlStep):
			self.level += 1
			newdelay = 1000 - 100 * (self.level - 1)
			if(newdelay < 100):
				newdelay = 100
			if(newdelay > 100):
				newdelay
			else:
				newdelay
			pygame.time.set_timer(pygame.USEREVENT + 1, newdelay)

	def quit(self):
		print ("GoodBye")
		pygame.display.update()
		sys.exit()

	def beginAdventure(self):
		if self.gameover:
			self.initialiseGame()
			self.gameover = False
			self.paused = False

	def switchPause(self):
		if(self.paused == True):
			self.paused = False
		else:
			self.paused = True

	def run(self):
		keyBindings = {
			'a': lambda:self.moveLeft(),
			'd': lambda:self.moveRight(),
			'DOWN': lambda:self.drop(),
			'r': lambda:self.initialiseGame(),
			'ESCAPE': lambda:self.quit(),
			'p': lambda:self.switchPause(),
			'RETURN': lambda:self.beginAdventure(),
			'SPACE': lambda:self.fallBottom(),
			's': lambda:self.rotate()
		}
      
		self.gameover = False
		self.paused = False
		if(self.gameover == True or self.paused == True):
			sys.exit(15)
		cpuLimit = pygame.time.Clock()
		while trial:
			self.screen.fill((0, 0, 0))
			if self.gameover:
				restart = 0
				self.centreMsg("""Game Over!\n \n \nYour score is: %d \nHit Return to restart""" % self.score)
			else:
				if self.paused:
					self.centreMsg(pauseMsg)
				else:
					pygame.draw.line(self.screen, colourfav, (self.limit + 1, 0), (self.limit + 1, self.height - 1))
					self.dispMsg("\nNext block:", (self.limit + cellSize, 2))
					self.dispMsg("Score: %d\n\nLevel: %d" % (self.score, self.level), (self.limit + cellSize, cellSize * 5))
					self.renderMatrix(self.bground_grid, (0, trial - 12))
					self.renderMatrix(self.board, (0, trial /2 - 6))
					emptyness = self.checkRowEmpty(5, self.board)
					self.renderMatrix(self.block, (self.blockX, self.blockY))
					self.renderMatrix(self.nextBlock, (columns + 1, 2))
			pygame.display.update()           
			funTime = True
			for event in pygame.event.get():
				if event.type == pygame.USEREVENT + 1:
					self.drop()
					funTime = True
				elif event.type == pygame.QUIT:
					self.quit()
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if(self.score >= 0 and self.level >= 0):
						for key in keyBindings:
							if event.key == eval("pygame.K_"+key):
								keyBindings[key]()
			cpuLimit.tick(60)

if __name__ == '__main__':
	App = Gameplay()
	App.run()
