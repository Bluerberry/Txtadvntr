home = [ # homescreen ascii art
	'           ▒██████▒██ ▒██▒██████          ',
	'             ▒██  ▒██ ▒██  ▒██            ',
	'             ▒██    ▒██    ▒██            ',
	'             ▒██  ▒██ ▒██  ▒██            ',
	'             ▒██  ▒██ ▒██  ▒██            ',
	'',
	' ▒████ ▒█████ ▒██ ▒██▒█████ ▒██████▒█████ ',
	'▒██ ▒██▒██ ▒██▒██ ▒██▒██ ▒██  ▒██  ▒██ ▒██',
	'▒██████▒██ ▒██▒██ ▒██▒██ ▒██  ▒██  ▒█████ ',
	'▒██ ▒██▒██ ▒██ ▒█ ▒█ ▒██ ▒██  ▒██  ▒██ ▒██',
	'▒██ ▒██▒█████   ▒██  ▒██ ▒██  ▒██  ▒██ ▒██',
	'',
	'',
	'',
	'',
	'',
	'                > New Game',
	'                > Load Game',
	'                > Settings',
	'                > Exit'
]
newgame = [ # newgamescreen ascii art
	'         ▒█████ ▒██████▒██  ▒██           ',
	'         ▒██ ▒██▒██    ▒██  ▒██           ',
	'         ▒██ ▒██▒██████▒██  ▒██           ',
	'         ▒██ ▒██▒██    ▒██▒█▒██           ',
	'         ▒██ ▒██▒██████ ▒██▒██            ',
	'',
	'      ▒██████ ▒████ ▒██  ▒██▒█████        ',
	'      ▒██    ▒██ ▒██▒███▒███▒██           ',
	'      ▒██▒███▒██████▒██▒█▒██▒█████        ',
	'      ▒██ ▒██▒██ ▒██▒██  ▒██▒██           ',
	'      ▒██████▒██ ▒██▒██  ▒██▒█████        '
]
loadgame = [ # loadgamescreen ascii art
	'      ▒██    ▒██████ ▒████ ▒█████        ',
	'      ▒██    ▒██ ▒██▒██ ▒██▒██ ▒██       ',
	'      ▒██    ▒██ ▒██▒██████▒██ ▒██       ',
	'      ▒██    ▒██ ▒██▒██ ▒██▒██ ▒██       ',
	'      ▒██████▒██████▒██ ▒██▒█████        ',
	'',
	'      ▒██████ ▒████ ▒██  ▒██▒█████        ',
	'      ▒██    ▒██ ▒██▒███▒███▒██           ',
	'      ▒██▒███▒██████▒██▒█▒██▒█████        ',
	'      ▒██ ▒██▒██ ▒██▒██  ▒██▒██           ',
	'      ▒██████▒██ ▒██▒██  ▒██▒█████        ',
	'',
	'',
	'',
	'',
	''
]
settings = [ # settingsscreen ascii art
	'',
	'',
	'',
	'▒██████▒██████▒██████▒█████ ▒██████▒██████',
	'▒██      ▒██    ▒██  ▒██ ▒██▒██    ▒██    ',
	'▒██████  ▒██    ▒██  ▒██ ▒██▒██▒███▒██████',
	'    ▒██  ▒██    ▒██  ▒██ ▒██▒██ ▒██    ▒██',
	'▒██████  ▒██    ▒██  ▒██ ▒██▒██████▒██████',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'',
	'        > Master volume  ',
	'        > Music volume   ',
	'        > Sound effects  ',
	'        > Return'
]
tiles = [
	[ #0  wall
		'██████████',
		'██████████',
		'██████████',
		'██████████',
		'██████████'],
	[ #1  horizontal path
		'██████████',
		'          ',
		'          ',
		'          ',
		'██████████'],
	[ #2  vertical path
		'██      ██',
		'██      ██',
		'██      ██',
		'██      ██',
		'██      ██'],
	[ #3  top-left corner path
		'██████████',
		'██        ',
		'██        ',
		'██        ',
		'██      ██'],
	[ #4  bottom-left corner path
		'██      ██',
		'██        ',
		'██        ',
		'██        ',
		'██████████'],
	[ #5  bottom-right corner path
		'██      ██',
		'        ██',
		'        ██',
		'        ██',
		'██████████'],
	[ #6  top-right corner path
		'██████████',
		'        ██',
		'        ██',
		'        ██',
		'██      ██'],
	[ #7  top split path
		'██      ██',
		'          ',
		'          ',
		'          ',
		'██████████'],
	[ #8  left split path
		'██      ██',
		'        ██',
		'        ██',
		'        ██',
		'██      ██'],
	[ #9  bottom split path
		'██████████',
		'          ',
		'          ',
		'          ',
		'██      ██'],
	[ #10 right split path
		'██      ██',
		'██        ',
		'██        ',
		'██        ',
		'██      ██'],
	[ #11 cross path
		'██      ██',
		'          ',
		'          ',
		'          ',
		'██      ██'],
	[ #12 top wall
		'██████████',
		'          ',
		'          ',
		'          ',
		'          '],
	[ #13 left wall
		'██        ',
		'██        ',
		'██        ',
		'██        ',
		'██        '],
	[ #14 bottom wall
		'          ',
		'          ',
		'          ',
		'          ',
		'██████████'],
	[ #15 right wall
		'        ██',
		'        ██',
		'        ██',
		'        ██',
		'        ██'],
	[ #16 top-left corner wall
		'██████████',
		'██        ',
		'██        ',
		'██        ',
		'██        '],
	[ #17 bottom-left corner wall
		'██        ',
		'██        ',
		'██        ',
		'██        ',
		'██████████'],
	[ #18 bottom-right corner wall
		'        ██',
		'        ██',
		'        ██',
		'        ██',
		'██████████'],
	[ #19 top-right corner wall
		'██████████',
		'        ██',
		'        ██',
		'        ██',
		'        ██'],
	[ #20 top exit
		'██      ██',
		'          ',
		'          ',
		'          ',
		'          '],
	[ #21 left exit
		'██        ',
		'          ',
		'          ',
		'          ',
		'██        '],
	[ #22 bottom exit
		'          ',
		'          ',
		'          ',
		'          ',
		'██      ██'],
	[ #23 right exit
		'        ██',
		'          ',
		'          ',
		'          ',
		'        ██'],
	[ #24 floor
		'          ',
		'          ',
		'          ',
		'          ',
		'          ']
]