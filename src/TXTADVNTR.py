#-----------------------------------------------------> Axiums
# The game screen is 22 x 42 pixels wide
# The display is 15 x 30 (0 t/m 14 and 6 t/m 36)
# The cli is 6 x 42 (16 t/m 21 and 0 t/m 41)

# 0 = wall
# 1 = horizontal path
# 2 = vertical path
# 3 = top-left corner path
# 4 = bottom-left corner path
# 5 = bottom-right corner path
# 6 = top-right corner path
# 7 = top split path
# 8 = left split path
# 9 = bottom split path
# 10 = right split path
# 11 = crossroads
# 12 = top wall
# 13 = left wall
# 14 = bottom wall
# 15 = right wall
# 16 = top-left wall
# 17 = bottom-left wall
# 18 = bottom-right wall
# 19 = top-right wall
# 20 = top exit
# 21 = left exit
# 22 = bottom exit
# 23 = right exit
# 24 = floor

#-----------------------------------------------------> Dependencies

from random import randint
from time import sleep
from os import (system, listdir)
from sprites import *
from json import load
import DungeonGeneration
import winsound
try:
	import curses
except ModuleNotFoundError: # whether you fucking like it or not
	system('pip install windows-curses')
	import curses

#-----------------------------------------------------> Functions

# Takes a string, a threshold and a maximum amount of wraps
# Returns an array where each entry contains a string no longer than threshold without splitting words
def wrap(msg, threshold, maxwrap):
	if len(msg) > maxwrap*42: # raisers wrapping error if maxwrap is exceeded
		raise maxwrapError
	msg = msg.split(' ') # seperate each word
	wrappedmsg = [] # init variables
	temp = ''
	for word in msg: # for each word
		if len(temp + word) <= threshold: # check for threshold
			temp += word + ' ' # append word
		else:
			wrappedmsg.append(temp) # start newline
			temp = word + ' '
	return wrappedmsg + [temp]

# Takes a string and coordinates
# Allows wrapping and delays before continuing
# Prints a string, beginning at coordinates
def write(x, y, msg, threshold=None, maxwrap=21, wait=False):
	msg = wrap(msg, threshold, maxwrap) if threshold else [msg] # wrap msg
	for l in range(len(msg)): # for each line
		scr.addstr(y+l+2, x+4, msg[l]) # print string
	scr.refresh()
	if wait:
		scr.getch() # blocks until input

# Takes a string and coordinates
# Allows wrapping, delays before continuing, skipping features and custom keypress delays
# Prints a string, beginning at coordinates. Simulates live keypresses
def typewrite(x, y, msg, threshold=None, maxwrap=21, wait=False, enableSkip=True, delay=0.04, delayOffset=1):
	scr.nodelay(True) # sets input to non-blocking
	curses.flushinp() # clear stdin
	msg = wrap(msg, threshold, maxwrap) if threshold else [msg] # wrap msg
	skip = False
	for l in range(len(msg)): # for each line
		for c in range(len(msg[l])): # for each char
			if (scr.getch() != -1 or skip) and enableSkip: # if skipped
				write(x+c, y+l, msg[l][c:]) # display remaining message
				scr.refresh()
				skip = True
				break
			write(x+c, y+l, msg[l][c]) # display character
			scr.refresh()
			sleep(delay + randint(-delayOffset, delayOffset) / 100) # sleep for keypress delay
	scr.nodelay(False) # sets input to blocking
	if wait:
		scr.getch() # blocks until input

# Takes maximum value and progress
# Allows for bar length declaration
# Returns string containing ASCII art progressbar of constant length
def progressbar(complete, progress, length=10):
	div = complete / length # find bar scale
	bar = '█' * int(progress // div) + '▌' * int(progress % div // (div / 2)) # generate progressbar
	return bar + ' ' * (length - len(bar)) # fill whitespace

# Takes a user command and an actionset
# Returns most probable action from actionset, determined by keyword occurances
def interpret_command(cmd, actionset):
	best = [[-1]] #init scoreboard
	for action in actionset: #determine score for each action
		score = 0
		for key in action[0]: #increase score for each key occurance in command
			score += 1 if key in cmd else 0
		if score > best[0][0]: #replace best if new highscore
			best = [[score, action[1]]]
		elif score == best[0][0]: #append to best if new highscore
			best.append([score, action[1]])
	if len(best) > 1 or best[0][0] < 2: #if instructions unclear, return err
		return err
	else:  #else return action
		return best[0][1]

# Takes a time, possible actionset and a predetermined message
# Prints given message followed by a timer. During this time the player can type a command
# Returns interpreted command
def timedInput(time, actionset, msg):
	cmd = '' # set variables
	timer = time
	scr.clear() # display inputfield
	write_scene()
	typewrite(0, 16, msg, 42, 4, enableSkip=False) # displays message
	typewrite(0, 20, f'██████████| {round(timer, 2)}', enableSkip=False)
	typewrite(0, 21, f'> {cmd}', enableSkip=False)
	scr.nodelay(True) # sets input to non-blocking
	curses.flushinp() # clears stdin
	while timer > 0: # query keyboard and handle kbhit
		if (key := scr.getch()) == 10: # if enter is pressed
			break # exit loop
		elif key == 8: # if backspace is pressed
			cmd = cmd[:-1] # pop last char
		elif len(cmd) < 40 and key != -1: # else, if within charlimit
			cmd += chr(key) # append kbhit
		scr.clear() # display timed inputfield
		write_scene()
		write(0, 16, msg, 42, 4)
		write(0, 20, f'{progressbar(time, timer)}| {round(timer, 2)}')
		write(0, 21, f'> {cmd}')
		sleep(0.02)
		timer -= 0.02 # countdown time TODO find appropriate value
	scr.nodelay(False)
	return interpret_command(cmd, actionset) # return interpreted command

# Takes an actionset
# Allows for a  message to be displayed
# Returns interpreted command
def untimedInput(actionset, msg='', newgamemenu=False):
	cmd = '' # init vars
	scr.clear()
	if newgamemenu:
		for i in range(11):
			write(0, i, newgame[i])
	else:
		write_scene()
	typewrite(0, 16, msg, 42, 4, enableSkip=False) # displays message
	typewrite(0, 21, '> ', enableSkip=False) # displays inputfield
	curses.flushinp() # clear stdin
	while True: # query keyboard and handle kbhit
		if (key := scr.getch()) == 10: # if enter is pressed
			break # exit loop
		elif key == 8: # if backspace is pressed
			cmd = cmd[:-1] # pop last char
		elif len(cmd) < 40: # else, if within charlimit
			cmd += chr(key) # append kbhit
		scr.clear() # display inputfield
		if newgamemenu:
			for i in range(11):
				write(0, i, newgame[i])
		else:
			write_scene()
		write(0, 16, msg, 42, 4)
		write(0, 21, f'> {cmd}')
	return cmd if newgamemenu else interpret_command(cmd, actionset) # return interpreted command

# Takes a monster
# Allows for sneakattacks
# Inintiates a combat loop wich prosess actions and counteractions until on or both parties die
def init_combat(playersneakattack=False, monstersneakattack=False):
	global in_combat
	player.aggressor = True if (playersneakattack or player.speed > monster.speed) and not monstersneakattack else False # determine player aggression
	in_combat = True
	scr.clear()
	write_scene()
	typewrite(0, 16, f'As you turn the corner, your eye falls upon a giant monster, {monster.name}\'s fangs are still covered with fresh blood from it\'s last kill.', 42, 4, wait=True)
	while monster.health > 0:
		if player.aggressor:
			action = timedInput(max(player.speed-monster.speed, 2), offenceActions, 'You see an opportunity within which you can attack!') # finds player action
			counteraction = defenceActions[randint(0, 2)][1] # finds monster action
		else:
			action = offenceActions[(r := randint(0, 2))][1] # finds monster action
			counteraction = timedInput(max(player.speed-monster.speed, 0) + 2, defenceActions, action(monster)) # finds player action
		msg = action(monster, counteraction) # finds result
		scr.clear() # display inputfield
		write_scene()
		typewrite(0, 16, msg, 42, 4, enableSkip=False)
		if player.health < 1: #exit if player died
			raise exitGame
	scr.clear()
	write_scene()
	typewrite(0, 16, f'You slash deep into the {monster.name}\'s flesh, and with a loud thump, it falls to the ground.', 42, 4, wait=True)
	in_combat = False
	player.xp += monster.xp
	player.health += 10
	while player.xp >= player.lvl * 5:
		player.xp -= player.lvl * 5
		player.lvl += 1
	maze[player.y][player.x][2] = False
	maze[player.y][player.x][1] = True

# Generates a 3x3 tile scene
def write_scene():
	scene = []
	for m in range(-1, 2):
		for i in range(5):
			temp = tiles[maze[player.y+m][player.x-1][0]][i]
			temp += tiles[maze[player.y+m][player.x+0][0]][i]
			temp += tiles[maze[player.y+m][player.x+1][0]][i]
			scene.append(temp)
	for y in range(15):
		write(0, y, scene[y])
	write(33, 0, f'HP  {progressbar(100, player.health, 5)}')
	write(33, 1, f'LVL {player.lvl}')
	write(33, 2, f'XP  {player.xp}')
	write(33, 3, f'SLD {player.shielding}')
	write(33, 4, f'SPD {player.speed}')
	if in_combat:
		write(33, 6, monster.name)
		write(33, 7, f'HP  {progressbar(monster_starting_health, monster.health, 5)}')
		write(33, 8, f'XP  {monster.xp}')
		write(33, 9, f'SHD {monster.shielding}')
		write(33, 10, f'SPD {monster.speed}')

# Takes a savefile
# Runs the entire game
def gameloop(savefile):
	global maze, monster, monster_starting_health
	with open(savefile) as f:
		maze = load(f)
	maze[50][50][2] = False
	scr.clear()
	typewrite(0, 0, 'You do not know who you are...', threshold=42, wait=True)
	scr.clear()
	typewrite(0, 0, 'You do not know where you are...', threshold=42, wait=True)
	scr.clear()
	typewrite(0, 0, 'All you know, is to kill!', threshold=42, wait=True)
	while True:
		actionset = [[['stop', 'exit', 'leave', 'quit'], stop], [['interact', 'open', 'inspect', 'search', 'loot', 'look', 'room', 'area'], eit]]
		if maze[player.y][player.x][2]:
			monster = monsterTemplate()
			monster_starting_health = monster.health
			init_combat()
		if (tileID := maze[player.y][player.x][0]) in [2, 4, 5, 7, 8, 10, 11, 13, 14, 15, 17, 18, 20, 21, 22, 23, 24]:
			actionset.append([['up', 'top', 'north', 'move', 'go', 'move', 'walk'], emt])
		if tileID in [1, 5, 6, 7, 8, 9, 11, 12, 14, 15, 18, 19, 20, 21, 22, 23, 24]:
			actionset.append([['left', 'east', 'move', 'go', 'move', 'walk'], eml])
		if tileID in [2, 3, 6, 8, 9, 10, 11, 12, 13, 15, 16, 19, 20, 21, 22, 23, 24]:
			actionset.append([['down', 'bottom', 'south', 'move', 'go', 'move', 'walk'], emb])
		if tileID in [1, 3, 4, 7, 9, 10, 11, 12, 13, 14, 16, 17, 20, 21, 22, 23, 24]:
			actionset.append([['right', 'west' 'move', 'go', 'move', 'walk'], emr])
		untimedInput(actionset, 'What do you want to do?')()

def startup_home(startup=False):
	cursor = 0 # set cursor
	scr.clear() # clears screen
	if startup: # intro sequence
		write(4, 10, 'Please use speakers, headphones or')
		write(3, 11, 'earbuds to fully experience this game')
		sleep(5)
		scr.clear()
		write(13, 11, 'Launch in 9 seconds...')
		for i in reversed(range(9)):
			sleep(1)
			write(23, 11, str(i))
		scr.clear()
		winsound.PlaySound("../resources/main.wav", winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)
		typewrite(0, 0, 'WARNING: INCOMING MESSAGE', enableSkip=False, delay=0.06, delayOffset=0)
		typewrite(25, 0, '...', enableSkip=False, delay=1.75, delayOffset=0)
		scr.clear()
		typewrite(0, 0, 'This one is for all of those people who still want more of all the great tunes sung by the commodore, and feel the world is moving just a tad too fast.', threshold=42, enableSkip=False, delay=0.079, delayOffset=0)
		sleep(2.025)
		scr.clear()
		typewrite(0, 0, 'SYNCHRONISING', enableSkip=False, delay=0.1, delayOffset=0)
		typewrite(13, 0, '...', enableSkip=False, delay=0.25, delayOffset=0)
		scr.clear()
		typewrite(0, 0, 'We feel nostalgic about these songs because it remind us of a time that we have lost, and now we\'re keeping it alive while having a blast...', threshold=42, enableSkip=False, delay=0.085, delayOffset=0)
		sleep(0.75)
		typewrite(0, 4, 'Emulating the past.', enableSkip=False, delay=0.08, delayOffset=0)
		sleep(2.1)
		scr.clear()
		for i in range(20): # typewrite home
			typewrite(0, i, home[i].replace('>', ' ') if i != 16 else home[i], enableSkip=False, delay=0.0165, delayOffset=0) # typewrite rows w/ cursor on 0
	else:
		for i in range(20): # write home
			write(0, i, home[i].replace('>', ' ') if i != 16 else home[i]) # write rows w/ cursor on 0
	curses.flushinp() # Clear stdin
	while True:
		if (key := scr.getch()) == 261 or key == 10: # if enter or right arrow is pressed
			break # break menu screen
		cursor += -1 if cursor > 0 and key == 259 else 1 if cursor < 3 and key == 258 else 0 # shift cursor
		for i in range(16, 20):
			write(0, i, home[i].replace('>', ' ') if i - 16 != cursor else home[i]) # print rows w/ cursor on selected item
	if cursor == 0: # select new game
		startup_newgame()
	elif cursor == 1: # select load game
		startup_loadgame()
	elif cursor == 2: # select settings
		startup_settings()
	else: # select exit
		raise exitGame
	startup_home()

def startup_newgame():
	name = untimedInput([], 'How will you name this world?', newgamemenu=True)
	DungeonGeneration.new_map(name)
	gameloop(f'../saves/{name}.json')

def startup_loadgame():
	if listdir('../saves/'):
		for save in listdir('../saves/'):
			loadgame.append(f'                > {save[:-5]}')
		cursor = 0
		scr.clear()
		curses.flushinp()
		for i in range(len(loadgame)):
				write(0, i, loadgame[i].replace('>', ' ') if i - 16 != cursor else loadgame[i]) # print rows w/ cursor on selected item
		scr.clear()
		curses.flushinp()
		for i in range(len(loadgame)):
				write(0, i, loadgame[i].replace('>', ' ') if i - 16 != cursor else loadgame[i]) # print rows w/ cursor on selected item
		while True:
			if (key := scr.getch()) == 261 or key == 10: # if enter or right arrow is pressed
				break # break menu screen
			cursor += -1 if cursor > 0 and key == 259 else 1 if cursor < len(listdir('../saves/'))-1 and key == 258 else 0 # shift cursor
			for i in range(16, len(loadgame)):
				write(0, i, loadgame[i].replace('>', ' ') if i - 16 != cursor else loadgame[i]) # print rows w/ cursor on selected item
		gameloop('../saves/' + listdir('../saves/')[cursor])

def startup_settings():
	global mastervolume, musicvolume, soundeffects
	cursor = 0 # set cursor
	scr.clear()
	curses.flushinp()
	for i in range(20):
		if i == 16: # print rows w/ cursor on 0 and progressbar
			write(0, i, f'{settings[i]}{progressbar(100, mastervolume)}|')
		elif i == 17: # print rows w/ progressbar
			write(0, i, f'{settings[i].replace(">", " ")}{progressbar(100, musicvolume)}|')
		elif i == 18: # print rows w/ progressbar
			write(0, i, f'{settings[i].replace(">", " ")}{progressbar(100, soundeffects)}|')
		else: # print other rows 
			write(0, i, f'{settings[i].replace(">", " ")}')
	while True:
		if (key := scr.getch()) == None or cursor == 0: # alter master volume
			mastervolume += 5 if mastervolume < 100 and key == 261 else -5 if mastervolume > 0 and key == 260 else 0
			curses.flushinp() # flush stdin to prevent overshooting
		elif cursor == 1: # alter music volume
			musicvolume += 5 if musicvolume < 100 and key == 261 else -5 if musicvolume > 0 and key == 260 else 0
		elif cursor == 2: # alster sound effect volume
			soundeffects += 5 if soundeffects < 100 and key == 261 else -5 if soundeffects > 0 and key == 260 else 0
		elif key == 261 or key == 10:
			break
		cursor +=  -1 if cursor > 0 and key == 259 else 1 if cursor < 3 and key == 258 else 0 # shift cursor
		scr.clear()
		for i in range(20):
			if i == 16: # print rows w/ cursor on selection and progressbar
				write(0, i, f'{settings[i].replace(">", " ") if i - 16 != cursor else settings[i]}{progressbar(100, mastervolume)}|')
			elif i == 17: # print rows w/ cursor on selection and progressbar
				write(0, i, f'{settings[i].replace(">", " ") if i - 16 != cursor else settings[i]}{progressbar(100, musicvolume)}|')
			elif i == 18: # print rows w/ cursor on selection and progressbar
				write(0, i, f'{settings[i].replace(">", " ") if i - 16 != cursor else settings[i]}{progressbar(100, soundeffects)}|')
			else: # print rows w/ cursor on selection
				write(0, i, f'{settings[i].replace(">", " ") if i - 16 != cursor else settings[i]}')

def shutdown():
	scr.clear() # resets all curses activity
	scr.nodelay(False)
	scr.keypad(False)
	curses.nocbreak()
	curses.echo()
	curses.endwin()
	print('Settings reset, ready for shutdown...')

#-----------------------------------------------------> Actions

def err(_0=None, _1=None):
	player.aggressor, player.advantage = False, False
	return [
		'You just stand there, doing nothing. A bit of spit drools from your mouth.',
		'Your mind loses focus for a while and you start thinking about doves.',
		'You experience a weird spasm rushing through your body, as if some idiot tried to make you do something stupid.',
		'You start to wonder who\'s smarter: you or your dog.',
		'All you hear is the wind blowing through your head.',
		'You just stand there like an idiot.',
		'A giant monster attacks you from behind! Jokes, your empty brain is halucinating again.'
	][randint(0, 6)]

def eml():
	player.x -= 1

def emr():
	player.x += 1

def emt():
	player.y -= 1

def emb():
	player.y += 1

def eit():
	item = [
		['You found a helmet, covered in dust! You gain some shielding.', 'player.shielding += 1'],
		['You found a chestplate underneath a loose floor tile! You gain shielding.', 'player.shielding += 2'],
		['You found a pair of leggings hanging overhead! You gain some shielding.', 'player.shielding += 1'],
		['You found a pair of shoes! You gain some shielding and lose some speed.', 'player.shielding, player.speed += -1, 1'],
		['You found a coin cache! You gain 15 xp.', 'player.xp += 15'],
		['You found a sick bagpipe-dubstep mixtape! You gain 10 hp.', 'player.health += 10'],
		['You find a strange rock. When you pick it up, you feel the blood rushing to your left nostril. You gain 10 levels.', 'player.lvl += 10'],
		['You find a strange white powder lying in the corner. Snort it. You gain speed.', 'player.speed += 2']
	][randint(0, 8)] if maze[player.y][player.x][1] else [
		['You found nothing but cobwebs...', ''],
		['You found nothing but some gravel...', ''],
		['You found nothing but the bones of your predecessors...', '']
	][randint(0, 2)]
	print('hey')
	exec(item[1])
	scr.clear()
	write_scene()
	typewrite(0, 16, item[0], 42, 4, wait=True)
	maze[player.y][player.x][1] = False

def ddl(monster, succesful):
	if player.aggressor:
		if succesful:
			player.aggressor = False if player.advantage == False else True
			player.advantage = None if player.advantage == True else False
			return f'the {monster.name} ducks to your left.'
		else:
			player.advantage = None if player.advantage == False else True
			return f'the {monster.name} tries to duck to your left.'
	else:
		if succesful:
			player.aggressor = True if player.advantage == True else False
			player.advantage = None if player.advantage == False else True
			return f'You dive to your left and succesfully evade the {monster.name}s attack.'
		else:
			player.advantage = None if player.advantage == True else False
			return f'You try to combat roll to your left but you roll straight into the {monster.name}s attack.'

def ddb(monster, succesful):
	if player.aggressor:
		if succesful:
			player.aggressor = False if player.advantage == False else True
			player.advantage = None if player.advantage == True else False
			return f'the {monster.name} leans backwards.'
		else:
			player.advantage = None if player.advantage == False else True
			return f'the {monster.name} tries to lean backwards.'
	else:
		if succesful:
			player.aggressor = True if player.advantage == True else False
			player.advantage = None if player.advantage == False else True
			return f'You quickly arch backwards and succesfully dodge the {monster.name}s attack.'
		else:
			player.advantage = None if player.advantage == True else False
			return 'You try to dodge backwards but to no avail.'

def ddr(monster, succesful):
	if player.aggressor:
		if succesful:
			player.aggressor = False if player.advantage == False else True
			player.advantage = None if player.advantage == True else False
			return f'the {monster.name} dodges to your right.'
		else:
			player.advantage = None if player.advantage == False else True
			return f'the {monster.name} tries to dodge to your right.'
	else:
		if succesful:
			player.aggressor = True if player.advantage == True else False
			player.advantage = None if player.advantage == False else True
			return f'You fling your body to the right and the {monster.name}s fist misses you by a hair.'
		else:
			player.advantage = None if player.advantage == True else False
			return f'You try to launch yourself to the right but the {monster.name}s fist sill strikes true.'

def opl(monster, counteraction=None):
	if counteraction == None:
		return f'The {monster.name} thrusts his fist to your left as a deafening roar leaves his jaws...'
	if player.aggressor:
		if counteraction.__name__[2] == 'r':
			return 'You throw a punch to your left, but ' + counteraction(monster, True) + (' You lose your advantage.' if player.advantage == None else ' You have a disadvantage.')
		else:
			dmg = max(randint(1, 4 if player.advantage else 2 if not player.advantage else 3) - monster.shielding + player.lvl, 0)
			monster.health -= dmg
			return 'You throw a punch to your left and ' + counteraction(monster, False) + f' You deal {dmg} to the {monster.name} and you ' + ('lose your disadvantage.' if player.advantage == None else 'have an advantage.')
	else:
		if counteraction != err and counteraction.__name__[2] == 'r':
			return counteraction(monster, True) + (' You lose your disadvantage.' if player.advantage == None else ' You have an advantage.')
		else:
			dmg = max(randint(3, 4 if player.advantage else 6 if not player.advantage else 5) - player.shielding + monster.xp // 10, 0)
			player.health -= dmg
			return counteraction(monster, False) + f' You lose {dmg} hp and ' + ('your advantage.' if player.advantage == None else 'you have a disadvantage.')

def opf(monster, counteraction=None):
	if counteraction == None:
		return f'The {monster.name} throws his arm towards your face. You see a strand of spit coming from between his lips...'
	if player.aggressor:
		if counteraction.__name__[2] == 'b':
			return 'You throw your arm forward but ' + counteraction(monster, True) + (' You lose your advantage.' if player.advantage == None else ' You have a disadvantage.')
		else:
			dmg = max(randint(1, 4 if player.advantage else 2 if not player.advantage else 3) - monster.shielding + player.lvl, 0)
			monster.health -= dmg
			return 'You throw your arm forward and ' + counteraction(monster, False) + f' You deal {dmg} to the {monster.name} and you ' + ('lose your disadvantage.' if player.advantage == None else 'have an advantage.')
	else:
		if counteraction.__name__[2] == 'b':
			return counteraction(monster, True) + (' You lose your disadvantage.' if player.advantage == None else ' You have an advantage.')
		else:
			dmg = max(randint(3, 4 if player.advantage else 6 if not player.advantage else 5) - player.shielding + monster.xp // 10, 0)
			player.health -= dmg
			return counteraction(monster, False) + f' You lose {dmg} hp and ' + ('your advantage' if player.advantage == None else 'you have a disadvantage')

def opr(monster, counteraction=None):
	if counteraction == None:
		return f'You see the {monster.name}\'s twisted eyes as a fist flashes to your right..'
	if player.aggressor:
		if counteraction.__name__[2] == 'l':
			return 'In a flash you blindly punch to your right, but ' + counteraction(monster, True) + (' You lose your advantage.' if player.advantage == None else ' You have a disadvantage.')
		else:
			dmg = max(randint(1, 4 if player.advantage else 2 if not player.advantage else 3) - monster.shielding + player.lvl, 0)
			monster.health -= dmg
			return 'In a flash you blindly punch to your right and ' + counteraction(monster, False) + f' You deal {dmg} to the {monster.name} and you ' + ('lose your disadvantage.' if player.advantage == None else 'have an advantage.')
	else:
		if counteraction.__name__[2] == 'l':
			return counteraction(monster, True) + (' You lose your disadvantage.' if player.advantage == None else ' You have an advantage.')
		else:
			dmg = max(randint(3, 4 if player.advantage else 6 if not player.advantage else 5) - player.shielding + monster.xp // 10, 0)
			player.health -= dmg
			return counteraction(monster, False) + f' You lose {dmg} hp and ' + ('your advantage' if player.advantage == None else 'you have a disadvantage')

def stop():
	if untimedInput([[['yes', 'ok', 'alright', 'true', 'yeah', 'yeet'], True], [['no', 'nope', 'false', 'nevermind', 'nah'], False]], 'Are you shure you want to exit?'):
		raise exitGame

#-----------------------------------------------------> Classes

class exitGame(Exception):
	pass

class maxwrapError(Exception):
	pass

class playerTemplate():
	def __init__(self):
		self.x = 50 # coords
		self.y = 50
		self.lvl = 1 # general stats
		self.xp = 0
		self.health = 100
		self.shielding = 0
		self.speed = 5
		self.aggressor = None # combat variables
		self.advantage = None

class monsterTemplate():
	def __init__(self):
		self.name = [
			'Poisonmouth',
			'Cthulu',
			'Smokecreep',
			'Vampcreep',
			'Quiet Babbler',
			'Malformation',
			'Bruised Shriek',
			'Nightmare Lyx',
			'Supreme Critl',
			'Barbed Doom',
			'Razorbeast',
			'Embermutant',
			'Blightcrackle',
			'Flamegolem',
			'Lonely Ooze',
			'Delerious Brat',
			'Hollow Hybrid',
			'Night Yak',
			'Tusked Tusk',
			'Screechor'
		][randint(0, 19)]
		self.health = player.lvl * randint(1, 10)
		self.shielding = randint(0, player.lvl)
		self.speed = randint(0, player.lvl)
		self.xp = self.health + self.shielding + self.speed

#-----------------------------------------------------> Variables

in_combat = False
player = playerTemplate()
mastervolume, musicvolume, soundeffects = 100, 100, 100
defenceActions = [
	[['dodge', 'left'], ddl],
	[['dodge', 'backward', 'back', 'duck', 'crouch', 'down'], ddb],
	[['dodge', 'right'], ddr]
]
offenceActions = [
	[['punch', 'attack', 'slash', 'hit', 'left'], opl],
	[['punch', 'attack', 'slash', 'hit', 'forward', 'infront', 'front'], opf],
	[['punch', 'attack', 'slash', 'hit', 'right'], opr]
]

#-----------------------------------------------------> Main code

try:
	system('title TXTADVNTR')
	system('mode con: cols=55 lines=30')
	system('cls')
	scr = curses.initscr() # init curses screen
	scr.keypad(True) # converts special keys to curses
	curses.noecho() # sets input to no-echo
	curses.cbreak() # sets input to always feed
	startup_home(startup=True) # start game
except exitGame:
	shutdown() # resets all curses activity
	sleep(5)
	print('See you soon!')
except Exception as e: # catches any error
	shutdown() # resets all curses activity
	print(e) # re-raise exception
	sleep(5)