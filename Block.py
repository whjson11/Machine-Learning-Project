from random import randrange as rand
import os
import pygame
import math
import sys
from constants import *

class Block(object):

	def joinMatrices(self, mat1, mat2, mat2Off):
		offX = mat2Off[0]
		offY = mat2Off[1]
		for countY, row in enumerate(mat2):
			for countX, val in enumerate(row):
				mat1[countY + offY + trial - 13][countX + offX] += val
		return mat1

	def moveLeft(self):
		if(self.gameover == False and self.paused == False):
			newX = self.blockX - 1
			if newX < 0:
				newX = 0
			if not self.checkCollision(self.board, self.block, (newX, self.blockY)):
				self.blockX = newX

	def moveRight(self):
		if(self.gameover == False and self.paused == False):
			newX = self.blockX + 1
			if newX > columns - len(self.block[0]):
				newX = columns - len(self.block[0])
			if not self.checkCollision(self.board, self.block, (newX, self.blockY)):
				self.blockX = newX

	def rotate(self):
		if(self.gameover == False and self.paused == False):
			newBlock = [[self.block[x][y] for x in range(len(self.block))] for y in range(len(self.block[0]) - 1, -1, -1)]
			if not self.checkCollision(self.board, newBlock, (self.blockX, self.blockY)):
				self.block = newBlock

	def fallBottom(self):
		if(self.gameover == False and self.paused == False):
			self.score += trial - 2
			while(not self.drop()):
				pass

	def drop(self):
		if(self.gameover == False and self.paused == False):
			self.blockY += 1
			if self.checkCollision(self.board, self.block, (self.blockX, self.blockY)):
				self.board = self.joinMatrices(self.board, self.block, (self.blockX, self.blockY))
				self.newBlock()
				clearedRows = 0
				clearedRows = self.checkRowFull(clearedRows)
				self.addClearedLines(clearedRows)
				return True
		return False

	def newBlock(self):
		self.block = self.nextBlock
		self.nextBlock = tetrisShapes[rand(len(tetrisShapes))]
		self.blockX = int(columns / 3 - len(self.block[0]) / 2 + trial - 7)
		self.blockY = initY
		if self.checkCollision(self.board, self.block, (self.blockX, self.blockY)):
			self.gameover = True
		else:
			False

	def renderMatrix(self, matrix, offset):
		for y, row in enumerate(matrix):
			for x, val in enumerate(row):
				if val:
					if(self.score >= 0 and self.level >= 0):
						pygame.draw.rect(self.screen, colours[val], pygame.Rect((offset[0] +x) * cellSize, (offset[1] + y) * cellSize, cellSize, cellSize), 0)

	def checkRowFull(self, clearedRows):
		while 1:
			for i, row in enumerate(self.board[:-1]):
				if 0 not in row:
					scores = self.score
					self.board = self.removeRow(self.board, i)
					clearedRows += 1
					break
			else:
				break
		return clearedRows
