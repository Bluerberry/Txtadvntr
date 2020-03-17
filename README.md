# TXTADVNTR

This project was a joint effort between two teams. Our end goal was to create a dungeon crawler text adventure game from scratch. Each team had their own task, the team consisting of Bram Kreulen and Nando Witte would focus on the shell script in which the game would be played. The team consisting of Maurits would focus on generating the map that would be played on.

## The Shell Script:

The Shell Script is the game itself. It uses a map generated by the Dungeon Generator. You, the user, can explore the map by typing simple commands such as “Go left”. In the dungeon you will encounter monsters, loot and rooms.

## The Dungeon Generation:

product: code capable of creating a 2d dungeon crawler map.
The map has to abide to certain rules and has been scripted to be rendered in a specific way. There are 3 by 3 rooms generated throughout the map. After this a road is tunneled through the entire map starting from the middle. All rooms try to connect to the road with one or two entranvces. Rooms have a higher chance of containing loot and monsters. This map is then forwarded to the Shell Script.

##  Installation

For this game you will need to be on a system that runs Windows. THIS IS VERY IMPORTANT. Secondly you will need to install Python. Lastly you need to install the library curses. You can do this by entering the command:

    pip install curses

Now just run the game and you can play it!