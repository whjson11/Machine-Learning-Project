from random import randrange as rand
import os
import pygame
import math
import sys
from constants import *

class Board(object):
	def checkCollision(self, board, shape, offset):
		for countY, row in enumerate(shape):
			for countX, cell in enumerate(row):
				try:
					if cell and board[countY + offset[1]][countX + offset[0]]:
						return True
				except IndexError:
					return True
		return False

	def newBoard(self):
		board = [[0 for x in range(columns)] for y in range(rows)]
		board += [[1 for x in range(columns)]]
		return board

	def removeRow(self, board, row):
		del	board[row]
		return [[0 for i in range(columns)]] + board

	def checkRowEmpty(self, row, board):
		for i in range(columns):
			if(board[row][i] != 0):
				return False
			else:
				continue
		return True
