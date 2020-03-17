# DND in a CLI - Text adventure shell
The shell supporting the text adventure. Contains menu screen, utility functions and gameloops.

### Must have
**- Gameloop** ✔
      
      A continuous loop that updates game objects, checks contitions and generally functions as the main 'engine' driving the game. Is nessicary for proper game functionality.
      
**- Error handling** ✔
      
      Curses, our supporting dependency, changes several properties of CMD, making it unusable outside of the programmed environment. Therefore, any and all unexpected program terminations should be caught in order for curses to return CMD to it's original state.
      
**- Supporting structure for dungeon generation** ✔
     
      Another group is building a python program that generates dungeons. We have agreed to join forces and implement their application into our Text adventure. In order for us to do so properly we need a supporting structure including several functions and code snippits. This supporting structure will act as a bridge between both programs.
      
**- Typewriting effect w/ skip function** ✔
     
      This is a classical effect used in text adventures. When printing, it appears as if someone is typing the words real-time instead of appearing instantly. On the other hand, if the player is feeling lazy, he can press any key to skip the typewriting effect and vieuw the whole message at once.

**- Exploration** ✔
     
      Allows for the player to explore the generated dungeon via typed commands. Because this is a text adventure and not a command line interface, we need to not conclusively define commands. Therefore, commands need to be interpreted to find the underlying purpose of a command.
      
**- Combat** ✔
    
      Scattered around the dungeon monsters can be found. Upon encountering them, a combat sequence should be initiated. Combat is a timed competition of moves and counter moves, where each succesfull attack or dodge results in advantages or damage.
 
### Should have
**- Scene visualisation** ✔
     
      Although this is a text adventure, we thought it'd be fun if you could actually see a representation of the room you are in. in order for us to do this, it is necissary to make ascii art for each type of room, and building support structure for choosing and displaying the correct room.
       
**- Music and sfx** ✔
     
      Add music that loops in the background. can be adjusted for volume within the settings tab. This will improve ambiance and enjoyment. We plan to use the song: Emulate the Past by Sky Marshall.
      
**- Menu screen** ✔
    
      Adds a menu system with intro sequence, New game tab, Load game tab, settings tab and exit tab.

**- Saved games** WIP
     
      Adds a system to load and save game progress within the load game tab

### Could have
**- Coloured textures**

**- Smooth room animations**

### Won't have
**- Flickery screens** sometimes

**- 3D engine** ✔

**- Disfunctioning code?** ✔