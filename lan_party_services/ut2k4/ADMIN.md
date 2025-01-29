Server admin commands:

```text
Statistics

Mem stat Show Windows memory usage
Stat all Displays all stats
Stat audio Shows audio stats
Stat fps Shows average and current frames per second
Stat game Displays game stats
Stat hardware Shows hardware stats
Stat net Displays net stats (ping etc)
Stat none Removes stat displays
Stat render Displays rendering stats

Player Commands / Bot Controls

Add bots (number) Add X number of bots
Behindview 1 Switches to 3rd person view
Behindview 0 Switches to 1st person view
Disconnect Disconnects from server
Reconnect Reconnects to last server
Quit Quits game
Exit Closes UT2003
Killbots Eliminates bots
Switchlevel (mapname) Changes to level named
Open (mapname) Opens named map
Switchteam Changes players team
Suicide Kills player
Teamsay (text) Talk to team-mates only
Playersonly Freezes bots
Say (text) Message to all players
Setname (name) Changes name

Misc. Commands

Demorec (demoname) Records a demo (n/a until patch)
Demoplay (demoname) Plays a demo (n/a until patch)
Stopdemo Stops playing a demo (n/a until patch)
Showhud Shows the HUD toggled on/off - added by Dudeguy
Brightness (number) Increases/Decreases brightness based on number
Contrast (number) Increases/Decreases contrast based on number - added by MacNiel
Gamma (number) Changes gamma level to certain number - added by MacNiel
Cdtrack (number) Plays named CD track number
Confighash Shows configuration information
Contrast (number) Increases/Decreases contrast based on number
Debug crash Test crash the game with an error
Debug eatmem Tests memory allocation until filled
Debug GPF Produces a general protection fault error
Debug recurse Test crash via infinite recursion
Exec (filename) Runs a file in the UT2003/system directory
Flush Cleans all caches and relights
FOV (number) Changes field of view to certain number
Dumpcache Clears memory cache contents
Getcolodepths Displays maximum colour depth supported by hardware
Getcurrentcolordepths Displays current colour depth
Getcurrentres Displays current resolution
Getcurrenttickrate Displays current tick rate
Getmaxtickrate Displays maximum tick rate
Musicorder (number) Changes to certain track in the song (0=ambient 1=action 2=suspense)
Netspeed (number) Set net speed (default=10000)
Obj classes Displays a list of object classes
Obj garbage Collects and purges objects not in use
Obj hash Displays object hashing stats
Obj linkers Displays list of active linkers
Pausesounds Pauses all sounds
Unpausesounds Un pauses all sounds
Preferences Opens advanced settings (Disabled in Retail Game)
Relaunch Copies report of current game to clipboard
Set (class variable value) Sets specified class and variable with named value
Setsensitivity (number) Sets mouse sensitivity to X
Setres (WidthxHeightxColordepth) Sets screen resolution to specific width/height/colour depth
Slomo 1 Sets game speed to normal
Slomo 2 Sets game speed to double - Increase number to go faster
Slomo .5 Sets game speed to half - Decrease number to go slower
Sockets Displays the list of in use sockets
Togglefullscreen Changes full screen mode (in Windows hit ALT + ENTER as well)
Type (text) Displays specified text in console

Cheat Codes

God Toggle God Mode
Amphibious Underwater Breathing
Fly Fly Mode
Ghost Walk through walls
Walk Return walking to normal
Invisible Turn invisibility on or off (true / false)
Teleport Teleport to where your crosshair is pointing
AllAmmo Full ammo on all possessed weapons
Allweapons Give all weapons
Loaded Give all weapons and full ammo on them (combo of allammo and allweapons
SkipMatch Win the current match and advance on the ladder
JumpMatch Jump to a specific match on the ladder, where is a number. For example 43 for ladder 4, rung 3
ChangeSize Change the player size by factor # (i.e. 0.25 or 2.0)
LockCamera Toggle locking the camera in its current position
FreeCamera D-link the camera rotation from the actor
ViewSelf Reset the camera to view the player (true to be quiet, false to have sound)
ViewBot Cycle the camera through the viewable bots
ViewFlag View the actor current carrying the flag
ViewPlayer Change the camera view to the given player
ViewActor Change the camera view to the given actor
ViewClass Change the camera view to the given class
KillViewedActor Kill the actor the camera is currently viewing. Do NOT kill yourself! (Game will get stuck)
Avatar Possess a pawn of the given class
Summon Summon the given object
SetCameraDist Set the distance the camera has from its target
SetGravity Change gravitational pull
SetJumpZ Change Jump height
SetSpeed Multiply the Player water and ground speed with the given value
ListDynamicActors Output all dynamic actors to the log file
FreezeFrame Pause the game for the given duration
SetFogR Set red colour component of fog
SetFogG Set green colour component of fog
SetFogB Set blue colour component of fog
SetFlash Set the duration a screen flash takes to fade away
CauseEvent Trigger the given event
LogSciptedSequences Toggle logging for all scripted sequences
KillPawns Kill all actor pawns except the player
KillAll Kill everything of the given class, i.e. KillAll Pawn
KillAllPawns Kill all pawns of the given class
PlayersOnly Toggle the level to a players only level
CheatView Toggle to view to the given actor
WriteToLog Write the string 'NOW!' to the game log
ReviewJumpSpots Test jumping, the parameter can be 'Transloc', 'Jump', 'Combo' or 'LowGrav'

And here´s some more (applies originally to UT2K3, but most of them also work with UT2K4) :

Player / Bot Commands

ADDBOTS [number] - Adds the specified number of bots
BEHINDVIEW 1 - Changes to third person view
BEHINDVIEW 0 - Changes to first person view
DISCONNECT - Disconnect from current server
EXIT - Quits the game
KILLBOTS - Gets rid of all bots
OPEN [IP address] - Connect to a specific server IP
OPEN [mapname] - Opens specified map
QUIT - Quits the game
RECONNECT - Reconnect to the current server
SWITCHLEVEL [mapname] - Switches to the specified level
SWITCHTEAM - Switch your player's team
SUICIDE - Kills yourself
TEAMSAY [text] - Displays your message in team chat
PLAYERSONLY - Freezes \ pauses the bots
SAY [text] - Displays your message in global chat
SETNAME [playername] - Changes your player name


Statistics

MEMSTAT - Displays Windows memory usage
STAT ALL - Shows all stats
STAT AUDIO - Shows audio stats
STAT FPS - Displays your frames per second
STAT GAME - Displays game stats
STAT HARDWARE - Shows hardware stats
STAT NET - Shows network game play stats
STAT NONE - Turns off all stats
STAT RENDER - Displays rendering statistics


Demo Commands

DEMOPLAY [demoname] - Plays the specified demo
DEMOREC [demoname] - Records a demo using the demoname you type
STOPDEMO - Stop recording a demo


Admin Commands

ADMIN SWITCHLEVEL [mapname?game=gametype?mutator=mutator] - Changes the current level to the specified level, game type and mutators
ADMIN [command] - Performs the specified command
ADMINLOGIN [password] - Logs the admininstrator onto the server using the specified password
ADMINLOGOUT - Logs the administrator off the server
ADMIN SET UWeb.Webserver bEnabled True - Enables the remote admin webserver (after level change)
ADMIN SET UWeb.Webserver bEnabled False - Disables the remote admin webserver (after level change)
KICK [playername] - Kicks the specified player from the server
KICKBAN [playername] - Kicks and bans the specified player from the server using their IP address. To unban the player, edit the server.ini or use the web admin interface


Other Commands

BRIGHTNESS [number] - Changes the brightness level to the specified number
CDTRACK [number] - Plays the specified CD track number
CONFIGHASH - Displays configuration info
CONTRAST [number] - Changes the contrast level to the specified number
DEBUG CRASH - Test crashes the game with an error
DEBUG EATMEM - Tests memory allocation until full
DEBUG GPF - Test crashes the game with a general protection fault error
DEBUG RECURSE - Test crashes the game by infinite recursion
DUMPCACHE - Displays the memory gcache contents
EXEC [filename] - Executes a file in the UT2003 /system/ directory by default
FLUSH - Flushes all caches and relights
FOV [number] - Changes the field of view to the specified number
GAMMA [number] - Changes the gamma level to the specified number
GETCOLORDEPTHS - Displays the maximum color depth supported by your hardware
GETCURRENTCOLORDEPTHS - Displays your current color depth
GETCURRENTRES - Displays your current resolution
GETCURRENTTICKRATE - Displays your current tick rate
GETMAXTICKRATE - Displays the maximum allowed tick rate
MUSICORDER [number] - Change to a certain track in the song (0=ambient, 1=action, 2=suspense)
NETSPEED [number] - Sets the net speed, default is 10000
OBJ CLASSES - Displays a list of object classes
OBJ GARBAGE - Collects and purges objects no longer in use
OBJ HASH - Displays object hashing statistics
OBJ LINKERS - Displays a list of active linkers
PAUSESOUNDS - Pauses all sounds
PREFERENCES - Opens advanced settings
RELAUNCH - Relaunches the engine
REPORT - Copies a report of the current game to clipboard
SET [class variable value] - Sets a specified class and specified variable with the specified value
SETSENSITIVITY [number] - Sets the mouse sensitivity to the specified number
SETRES [WxHxD] - Sets your screen resolution to the specified width, height, and color depth
SLOMO 1 - Sets the speed of the game back to normal real time speed
SLOMO 2 - Sets speed to double. Increase number to go faster
SLOMO .5 - Sets speed to half. Decrease number to go slower
SOCKETS - Displays a list of sockets in use
TOGGLEFULLSCREEN - Toggles fullscreen mode
TYPE [text] - Displays the specified text on the console
UNPAUSESOUNDS - Un-pauses all sounds
```
