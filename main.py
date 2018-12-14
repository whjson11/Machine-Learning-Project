#An object oriented program which recreates the classic game of Tetris in a text based interface.
#SSAD and Project Assignment 1
#Anubhab Sen 201501114
import tensorflow as tf
import numpy as np
import time
import numpy as np
import random
from PIL import ImageGrab
from random import randrange as rand
from Board import Board
from Block import Block
import os
import pygame
import math
import sys


from constants import *

GAMMA = 0.98
ACTIONS=4
REPLAY_MEMORY = 10000
OBSERVE = 2000
MINIBATCH_SIZE = 250
INITIAL_EPSILON = 0.99
FINAL_EPSILON = 0.0001

def weight_variable(shape):
	return tf.Variable(tf.truncated_normal(shape,stddev=0.01))

def bias_variable(shape):
	return tf.constant(0.1, shape=shape)

def CreateNetwork():
	W_conv1 = weight_variable([8, 8, 1, 16])
	b_conv1 = bias_variable([16])
	W_conv2 = weight_variable([4, 4, 16, 32])
	b_conv2 = bias_variable([32])
	W_conv3 = weight_variable([3, 3, 32, 64])
	b_conv3 = bias_variable([64])
   
	state = tf.placeholder(tf.float32,[None,760,800,1])
	state_dsample = tf.nn.max_pool(state,ksize=[1,4,4,1],strides=[1,4,4,1],padding='SAME')
   
	h_conv1=tf.nn.relu(tf.nn.conv2d(state_dsample,W_conv1,strides=[1,4,4,1],padding='SAME'))
	h_pool1=tf.nn.max_pool(h_conv1,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
   
	h_conv2=tf.nn.relu(tf.nn.conv2d(h_pool1,W_conv2,strides=[1,2,2,1],padding='SAME'))
   
	h_conv3=tf.nn.relu(tf.nn.conv2d(h_conv2,W_conv3,strides=[1,2,2,1],padding='SAME'))
       
	h_conv3_flat=tf.reshape(h_conv3,[-1,2688])
   
	W_fc1 = weight_variable([2688,200])
	b_fc1 = bias_variable([200])
   
	W_fc2 = weight_variable([200,ACTIONS])
	b_fc2 = bias_variable([ACTIONS])
                           
	h_fc1 = tf.nn.relu(tf.matmul(h_conv3_flat,W_fc1) + b_fc1)
                           
	read_out = tf.matmul(h_fc1,W_fc2) + b_fc2
                           
	return state, read_out

class Gameplay(Block, Board):
	reward_t = 0


	def game_frame(self):
		self.img = ImageGrab.grab(bbox = (0,34,760,834))
		return np.reshape(self.img.convert('L'),(760,800,1))

	def take_action(self,action):        
		key = action.index(1)
		if key == 1:
			self.reward_t += self.fallBottom()
		elif key == 0:
			self.moveLeft()
		elif key == 2:
			self.moveRight()
		else:
			self.rotate()
                                  
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
		linescores = [0, 1, 2, 3, 4]
		self.lines = self.lines + n
		self.updateScore(linescores[n])
		self.reward_t = 0
		for i in range (0,n):
			self.reward_t += (1.2)**n

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
		sess=tf.InteractiveSession()
		state, read_out = CreateNetwork()
		actions = tf.placeholder(tf.float32, [None,ACTIONS])                        
		targetQ = tf.placeholder(tf.float32, [None])
		read_out_action=tf.reduce_sum(tf.multiply(read_out,actions),1)
		cost = tf.reduce_mean(tf.square(targetQ - read_out_action))
		train_step = tf.train.AdamOptimizer(1e-6).minimize(cost)
		keyBindings = {
			'r': lambda:self.initialiseGame(),
			'ESCAPE': lambda:self.quit(),
			'p': lambda:self.switchPause(),
			'RETURN': lambda:self.beginAdventure(),
			'SPACE': lambda:self.fallBottom()
		}
		self.gameover = False
		self.paused = False
		episode = 0
		t = 1
		#게임 처음 상황 로드
		sess.run(tf.global_variables_initializer())
		terminal = 0
		epsilon = INITIAL_EPSILON
		Batch = []
		if(self.gameover == True or self.paused == True):
			sys.exit(15)
		self.screen.fill((0, 0, 0))
		pygame.draw.line(self.screen, colourfav, (self.limit + 1, 0), (self.limit + 1, self.height - 1))
		self.dispMsg("\nNext block:", (self.limit + cellSize, 2))
		self.dispMsg("Score: %d\n\nLevel: %d" % (self.score, self.level), (self.limit + cellSize, cellSize * 5))
		self.renderMatrix(self.bground_grid, (0, trial - 12))
		self.renderMatrix(self.board, (0, trial /2 - 6))
		emptyness = self.checkRowEmpty(5, self.board)
		self.renderMatrix(self.block, (self.blockX, self.blockY))
		self.renderMatrix(self.nextBlock, (columns + 1, 2))
		pygame.display.update()
		time.sleep(10)
		state_t = self.game_frame()
		while trial:
			self.reward_t = 0            
			action_t = [0,0,0,0]
			read_out_t = read_out.eval(feed_dict={state : np.reshape(state_t,(1,760,800,1))})[0]
			chosen_action = np.argmax(read_out_t)    
			if random.random() < epsilon:
				while True :
					random_action = random.randrange(ACTIONS)
					if random_action != chosen_action:
						action_index = random_action
						action_t[action_index] = 1
						break
			else:
					action_index =chosen_action
					action_t[action_index] = 1
			self.take_action(action_t)
			if t % 3 ==0:
				self.drop()
			self.screen.fill((0, 0, 0))
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
			for event in pygame.event.get():
				if event.type == pygame.USEREVENT + 1:
					funTime = True
				elif event.type == pygame.QUIT:
					self.quit()
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if(self.score >= 0 and self.level >= 0):
						for key in keyBindings:
							if event.key == eval("pygame.K_"+key):
								keyBindings[key]()
			state_t_next = self.game_frame() # 다음 프레임 로드
			if self.gameover:
				terminal = 1
				episode += 1
				for i in range(0,t):
					if Batch[-i][4] == 0:
						Batch[-i][2] -=0.95**i
					else:
						break
				self.reward_t = -10
				self.beginAdventure()               
			else:
				terminal = 0
        
			if epsilon > FINAL_EPSILON and t % (OBSERVE/5) == 0:
				epsilon -= (INITIAL_EPSILON-FINAL_EPSILON)/ (OBSERVE/5)
        
			Batch.append([state_t,action_t,self.reward_t,state_t_next,terminal])
        
			if t > REPLAY_MEMORY:
				Batch.pop(0)
        
			if t % OBSERVE==0:
				print("-----Training-----")
				minibatch = random.sample(Batch,MINIBATCH_SIZE)
				state_t_batch = [i[0] for i in minibatch]
				action_t_batch = [i[1] for i in minibatch]
				reward_t_batch = [i[2] for i in minibatch]
				state_t_next_batch = [i[3] for i in minibatch]
            
				Q_t_batch = []
				read_out_t_next_batch = read_out.eval(feed_dict = {state : state_t_next_batch})
            
				for i in range(0,MINIBATCH_SIZE):
					terminal = minibatch[i][4]
					if terminal:
						Q_t_batch.append(reward_t_batch[i])
					else:
						Q_t_batch.append(reward_t_batch[i] + GAMMA * np.max(read_out_t_next_batch[i]))
            
				train_step.run(feed_dict = {state : state_t_batch, targetQ : Q_t_batch, actions : action_t_batch})
				print("-----Traing Done----")
			state_t = state_t_next
			t += 1
			print("Episode: ",episode,"   Trial: ",t,"   Rewards:",self.reward_t,"   Epsilon:",epsilon,"    ",action_index)
            

if __name__ == '__main__':
	App = Gameplay()
	App.run()