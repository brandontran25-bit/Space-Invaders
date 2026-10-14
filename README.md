--Python Space Invaders--
A retro-style, two-level Space Invaders game written in Python using Pygame, with a title screen, wave and barrage events, deployable shield and power-ups.


*Requirements:
•	Python 3 installed on the computer.
•	Pygame installed in the same Python environment used to run the project.
•	The complete project folder, including Graphics, Sounds and Font folders.


*How Do I Start the Project?
1.	Download or clone the complete Space Invaders project folder.
2.	Open the project folder in Visual Studio Code.
3.	Open the VS Code terminal.
4.	Install Pygame if required by entering: pip install pygame
5.	Run the project by entering: python main.py
6.	The title screen appears first. Press SPACE to start. Use LEFT and RIGHT to move, SPACE to shoot and E to deploy the Level 2 shield. Press SPACE after Level 1 completion to enter Level 2; SPACE after GAME OVER restarts.


*Controls
Key & Action:
LEFT ARROW: Move left
RIGHT ARROW: Move right
SPACE: Start title screen / shoot during gameplay / proceed to Level 2 / restart after game over
E: Deploy Level 2 shield when available


*Project Files
File/Folder              Purpose
main.py                  Initialises Pygame, controls title/Level 1/Level 2 state transitions, processes events, updates the active game and draws the GUI.
title_screen.py          Draws the title logo, star field, alien formation and start prompt; updates title-screen animation state.
game.py                  Controls Level 1 aliens, obstacles, collisions, lives, score, high score, mystery ship and reset behaviour.
level2.py                Controls Level 2 wave progression, barrage events, shield/power-up state, collisions and Level 2 interface status.
spaceship.py             Controls the Level 1 player movement, shooting and laser recharge.
level2_spaceship.py      Provides the Level 2 player/spaceship behaviour.
alien.py                 Defines the normal alien sprites and mystery ship.
laser.py                 Defines laser movement and deletion outside the screen.
obstacle.py              Builds destructible Level 1 shields from small Block sprites.
shield.py                Defines the deployable Level 2 shield and its state/charges.
powerup.py               Defines the Level 2 power-ups and their movement/collection behaviour.
Graphics/                Contains player, alien and mystery-ship images.
Sounds/                  Contains the existing game music and sound effects.
Font/                    Contains the monogram pixel font used by the interface.
highscore.txt            Stores the highest score; if it is absent, the game starts the high score at 0.


Troubleshooting
•	If “No module named pygame” appears, install Pygame using the same Python interpreter selected in VS Code.
•	If an image, font or sound file cannot be found, check that the project is being run from the folder that contains main.py and the asset folders.
•	If the wrong Python version runs, use the VS Code “Select Interpreter” command and choose the intended Python 3 installation.
