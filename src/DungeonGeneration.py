# Importing libraries

from random import randint
from time import time
import json
#import numpy as np
#import matplotlib.pyplot as plt

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Global definition

tilemap,roomlist,tilevalue = [],[],{'floor':0,'wall':1,'outerwall':2,'roomfloor':3,'roomwall':4}
floors, walls = ['floor','roomfloor'],['wall','outerwall','roomwall']

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Size and start location definition

size = 100
start = size//2
start += 1 if start % 2 == 1 else 0  # start position needs to be even

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Class definition

class tile:  # containing every thing tile related such as tunnel and identify
	def __init__(self, outerwall,y,x):
		self.block = 'outerwall' if outerwall else 'wall'
		self.coor = [y,x]
		self.done = False
		self.Nflag, self.Wflag, self.Sflag, self.Eflag= False, False, False, False
		self.Treasure, self.Mob = False, False

		self.id = 0

		self.Nflag = True if size - self.coor[0] >= size - 2 else False
		self.Wflag = True if size - self.coor[1] >= size - 2 else False
		self.Sflag = True if size - self.coor[0] <= 2 else False
		self.Eflag = True if size - self.coor[1] <= 2 else False

	def preload(self):  # fetch the neighbours
		try:  # only possible with a try since else it will just straight up crash and its easier than checking for the max length of the map
			self.Ntile = tilemap[self.coor[0]-1][self.coor[1]]
		except:
			self.Ntile = None
		try:
			self.Wtile = tilemap[self.coor[0]][self.coor[1]-1]
		except:
			self.Wtile = None
		try:
			self.Stile = tilemap[self.coor[0]+1][self.coor[1]]
		except:
			self.Stile = None
		try:
			self.Etile = tilemap[self.coor[0]][self.coor[1]+1]
		except:
			self.Etile = None

	def tunnel(self):  # responsible for tunneling through the map
		if randint(0,2) == 1:
			return
		directions = [0,1,2,3]  # N, W, S, E. Below conditions can be changed to influence map tunneling
		if self.Nflag or self.Ntile.Ntile.block != 'wall':  # N
			directions.remove(0)
		if self.Wflag or self.Wtile.Wtile.block != 'wall':  # W
			directions.remove(1)
		if self.Sflag or self.Stile.Stile.block != 'wall':  # S
			directions.remove(2)
		if self.Eflag or self.Etile.Etile.block != 'wall':  # E
			directions.remove(3)

		if len(directions) == 0:
			return

		choice = directions[randint(0,len(directions) - 1)]
		if choice == 0:
			self.Ntile.Ntile.block, self.Ntile.block = 'floor','floor'  # N
			foundtile = self.Ntile.Ntile
		elif choice == 1:
			self.Wtile.Wtile.block, self.Wtile.block = 'floor','floor'  # W
			foundtile = self.Wtile.Wtile
		elif choice == 2:
			self.Stile.Stile.block, self.Stile.block = 'floor','floor'  # S
			foundtile = self.Stile.Stile
		elif choice == 3:
			self.Etile.Etile.block, self.Etile.block = 'floor','floor'  # E
			foundtile = self.Etile.Etile

		if len(directions) == 2:
			self.done = True

		if randint(0,9) == 0:
			self.Treasure, self.Mob = True, True

		return foundtile

	def deadend(self):  # responsible for removing deadends
		surroundings = [self.Ntile.block, self.Wtile.block, self.Stile.block, self.Etile.block]
		floortiles = surroundings.count('floor') + surroundings.count('roomfloor')
		if floortiles <= 1:  # if there is only 1 floor tile surrounding this tile then this tile is a deadend
			self.block = 'wall'

	def identify(self):  # responsible for defining tile.id
		if self.id != 0:
			pass
		elif self.block == 'wall' or self.block == 'outerwall' or self.block == 'roomwall':
			self.id = 0
		elif self.block == 'floor':  # self.id starts at None
			surroundings, cornerid = [self.Ntile.block, self.Wtile.block, self.Stile.block, self.Etile.block], {0:5,1:6,2:3,3:4}
			if self.Ntile.block == 'floor' and self.Stile.block == 'floor':  # check vertical alingment
				if self.Etile.block == 'floor' and self.Wtile.block == 'floor':  # found a cross
					self.id = 11  # a cross
				elif self.Etile.block == 'floor':  # right split
					self.id = 10
				elif self.Wtile.block == 'floor':  # left split
					self.id = 8
				else:  # vertical corridor
					self.id = 2
			elif (self.Ntile.block == 'floor' or self.Stile.block == 'floor') and 'roomfloor' in surroundings:
				self.id = 2  # in case we are going into a room
			elif self.Wtile.block == 'floor' and self.Etile.block == 'floor':  # check horizontal alignment
				if self.Ntile.block == 'floor':
					self.id = 7  # top split
				elif self.Stile.block == 'floor':
					self.id = 9  # bottom split
				else:
					self.id = 1
			elif (self.Wtile.block == 'floor' or self.Etile.block == 'floor') and 'roomfloor' in surroundings:
				self.id = 1
			else:
				for i in range(4):
					if surroundings[i] == 'floor' and surroundings[(i+1)%4] == 'floor' and surroundings[(i+2)%4] in walls and surroundings[(i+3)%4] in walls:  # mod for to loop back and check for corners
						self.id = cornerid[i]
						break
		else:
			self.id = 24

class room:  # containing rooms, location and entrance function
	def __init__(self,y,x,size):
		self.coor = [y,x]  # representing the top left corner of the room
		self.size = size
		self.middle, self.middletile = [int(y+size//2),int(x+size//2)], tilemap[int(y+size//2)][int(x+size//2)]
		self.tiles = []
		self.Nentflag, self.Nserflag, self.Wentflag, self.Wserflag, self.Sentflag, self.Sserflag, self.Eentflag, self.Eserflag = False, True, False, True, False, True, False, True  # used to see where we can make an entrance, followed by what direction we can search. to make sure we don't crash with big search widths.
		# Northentranceflag and Northsearchflag

	def entrance(self):  # responsible for creating an entrance to a room
		searchwidth = (self.size//2) - 1
		while searchwidth < 5: # so it doesnt go through other rooms since they require atleast 5 plus aesthetics
			#print(f'current searchwidth: {searchwidth}, middle is positioned at [y,x]: {self.middle}')  # could still search outside of the map which is an issue that not always shows.
			if self.Nserflag and tilemap[self.middle[0] - searchwidth][self.middle[1]].Nflag:
				self.Nserflag = False
			if self.Wserflag and tilemap[self.middle[0]][self.middle[1] - searchwidth].Wflag:
				self.Wserflag = False
			if self.Sserflag and tilemap[self.middle[0] + searchwidth][self.middle[1]].Sflag:
				self.Sserflag = False
			if self.Eserflag and tilemap[self.middle[0]][self.middle[1] + searchwidth].Eflag:
				self.Eserflag = False

			if self.Nserflag and tilemap[self.middle[0] - searchwidth][self.middle[1]].block == 'floor':
				self.Nentflag = True

			if self.Wserflag and tilemap[self.middle[0]][self.middle[1] - searchwidth].block == 'floor':
				self.Wentflag = True

			if self.Sserflag and tilemap[self.middle[0] + searchwidth][self.middle[1]].block == 'floor':
				self.Sentflag = True

			if self.Eserflag and tilemap[self.middle[0]][self.middle[1] + searchwidth].block == 'floor':
				self.Eentflag = True

			if self.Nentflag or self.Wentflag or self.Sentflag or self.Eentflag:
				break
			searchwidth += 1

		while sum([self.Nentflag,self.Wentflag,self.Sentflag,self.Eentflag]) > 2:
			counter = randint(0,3)
			if counter == 0:
				self.Nentflag = False
			elif counter == 1:
				self.Wentflag = False
			elif counter == 2:
				self.Sentflag = False
			else:
				self.Eentflag = False

		vrangevar,hrangevar = searchwidth * (self.Nentflag or self.Sentflag), searchwidth * (self.Wentflag or self.Eentflag)  # doing some weird stuff and calculating coords with zero bools
		#print(f'room at {self.middle} found v:{vrangevar} and h:{hrangevar}')

		for addedindex in range(vrangevar * (-1 if self.Nentflag else 0),max(vrangevar * (1 if self.Sentflag else 0),0)):  # the negative will make it go north
			tilemap[self.middle[0]+addedindex][self.middle[1]].block = 'floor' if 'wall' in tilemap[self.middle[0]+addedindex][self.middle[1]].block else tilemap[self.middle[0]+addedindex][self.middle[1]].block
			#print(f'should have created floor at {self.middle[0]+addedindex}, and {self.middle[1]}')

		for addedindex in range(hrangevar * (-1 if self.Wentflag else 0),hrangevar * (1 if self.Eentflag else 0)):
			tilemap[self.middle[0]][self.middle[1]+addedindex].block = 'floor' if 'wall' in tilemap[self.middle[0]][self.middle[1]+addedindex].block else tilemap[self.middle[0]][self.middle[1]+addedindex].block

		if self.Nentflag:  # is going wrong for some reason
			self.middletile.Ntile.id = 20
		if self.Wentflag:
			self.middletile.Wtile.id = 21
		if self.Sentflag:
			self.middletile.Stile.id = 22
		if self.Eentflag:
			self.middletile.Etile.id = 23

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function definition

def rooms(tries,roomsize):  # responsible for creating rooms in valid locations
	forbidden,stopflag = ['roomfloor','roomwall','outerwall','floor'], False
	for _ in range(tries):
		stopflag = False
		tly,tlx = randint(0, (size - roomsize) // 2) * 2, randint(0, (size - roomsize) // 2) * 2  # top-left y and x
		for y in range(tly, tly + roomsize):  # check these variables for inclusiveness
			for x in range(tlx, tlx + roomsize):
				if tilemap[y][x].block in forbidden:
					#print(f'found {tilemap[y][x].block} at [{y},{x}]')
					stopflag = True  # continueing an outer loop using function definition could be used to remove the flag.

		if stopflag:
			#print(f'failed at [{tly},{tlx}]')
			continue

		roomlist.append(room(tly,tlx,roomsize))
		roomwallid = [16,12,19,   13,24,15,   17,14,18]
		counter = 0
		for y in range(tly, tly + roomsize):  # check these variables for inclusiveness
			row = []
			for x in range(tlx, tlx + roomsize):
				tilemap[y][x].block = 'roomwall' if y == tly or x == tlx or y == tly + roomsize - 1 or x == tlx + roomsize - 1 else 'roomfloor'
				if tilemap[y][x].block == 'roomfloor':
					tilemap[y][x].Mob = True if randint(0,3) == 0 else False
					tilemap[y][x].Treasure = True if randint(0,8) == 0 else False
					tilemap[y][x].id = roomwallid[counter]
					counter += 1
				row.append(tilemap[y][x])
			roomlist[-1].tiles.append(row)

def tunnelmap(tries):  		# responsible for calling tunnel to every object
	#t0 = time()
	upfortunnel = []  # preload the floor tiles into the upfortunnel list, could definitely be integrated with the __init__ or something like it
	for row in tilemap:
		for tile in row:
			tile.preload()
			if not tile.done and tile.block == 'floor' and tile.coor[0]%2 == 0 and tile.coor[1]%2 == 0:
				upfortunnel.append(tile)
	#print(f'map was created in {time() - t0}')

	#t0 = time()
	for _ in range(tries):
		newtunnel = []
		for tile in upfortunnel[::-1]:
			newtile = tile.tunnel()
			if newtile != None:
				newtunnel.append(newtile)
			if not tile.done:
				newtunnel.append(tile)
		upfortunnel = newtunnel
	#print(f'map was tunneled in {time() - t0}')

def export(name):  				# responsible for exporting the map in a json
	ExportMap = []
	for row in tilemap:
		tiles = []
		for tile in row:
			tiles.append([tile.id, tile.Treasure, tile.Mob])
		ExportMap.append(tiles)

	#print('Map has been saved')

	with open(f'../saves/{name}.json','w',encoding = 'utf-8') as F:
		json.dump(ExportMap,F)

def removedeadend(tries):  	# responsible for calling tile.deadend
	for _ in range(tries):
		for row in tilemap:
			for tile in row:
				if tile.block == 'floor':
					tile.deadend()

def identify():  			# responsible for calling tile.identify
	for row in tilemap:
		for tile in row:
			tile.identify()

def visualize():  			# responsible for visualizing every tile.id
	safetymap = []
	for row in tilemap:  # matplot visualisation
		tiles = []
		for tile in row:
			tiles.append(tile.id)
		safetymap.append(tiles)
	H = np.array(safetymap)
	plt.imshow(H)
	plt.show()

def humanvis():  			# responsible for visualizing a regular map
	safetymap = []
	for row in tilemap:  # matplot visualisation
		tiles = []
		for tile in row:
			tiles.append(tilevalue[tile.block])
		safetymap.append(tiles)
	H = np.array(safetymap)
	plt.imshow(H)
	plt.show()

def entrance():  			# responsible for calling entrance to every room
	for rooM in roomlist:   # used a weird naming to make sure we do not interfere with class room
		rooM.entrance()

def mapcreation():  		# responsible for creating a 2d-array
	d2array = []
	for y in range(size):
		row = []
		for x in range(size):
			row.append(tile(True if y == 0 or y == size-1 or x == 0 or x == size-1 else False,y,x))
		d2array.append(row)
	return d2array

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main events

def new_map(name):  # creating a map
	# Map creation
	global tilemap
	tilemap = mapcreation()

	# Set the first block to floor for the generating system.
	tilemap[start][start].block = 'floor'  # starting position could be anywhere as long as the coords are even.
	#print('map has been created')

	# Map creating systems
	rooms(200,5)  		# create all the rooms
	tunnelmap(1000)		# tunnel from the start start
	entrance()			# create all the entrances
	removedeadend(100)	# remove all the dead ends, try based
	identify()			# call tile.id for everything
	#visualize()			# visualize the map
	#humanvis()			# visualize the map a second time.
	export(name)		# export the map