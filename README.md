# Python-MazeGame
This is a simple game made whit python for a university project.

## About The Project
The original concept for this project was to have a game that worked similarly to the game "Pac-Man" where the playing field was in the form of a maze and the player character had to collect specific objects while there were enemies that were an obstacle to the player. The project was made for a python class in my second year of university. The project itself is a pretty simple version of what can be made using "Pac-Man" as an inspiration.

### Built With
This project uses Pygame.

## Prerequisites and Installation

### Prerequisites
* Download and install python 3.9 or newer from the official website 
* Install Pygame \
  For Windows:
  ```sh
  py -m pip install -U pygame --user
  ```
  For Mac:
  ```sh
  python3 -m pip install -U pygame --user
  ```
  For Linux(Ubuntu):
   ```sh
  sudo apt-get install python3-pygame
  ```
  
  ### Installation
  
  Clone the repo and open it with an IDE that supports python.
   ```sh
  git clone https://github.com/RosenStefanov/Python-MazeGame.git
  ```
  
  ## Usage
  
  ### On Start
  
  After running the project in a python IDE the start screen will open that explains the objective of the game, the controls and gives 3 options for difficulty. By pressing 1, 2 or 3 the game will start the respective difficulty and by pressing ESC the game closes.
  
![startscreen](https://user-images.githubusercontent.com/95367525/180017385-2ed49ced-0cf4-47f9-8910-09b5dfb0d32d.PNG)


### The Running Game

  The player gets spawned in the maze together whit the enemies and a mushroom. The goal is to collect as many mushrooms as you can before you get git by an enemy.
  
  ![game](https://user-images.githubusercontent.com/95367525/180019306-f1191817-b8f6-4d76-bdaf-919a85574f94.PNG)

### Game Over Screen
After getting hit the user is given the game over screen that shows the score the user had before they colided with an enemy and the user is prompted to press any button to go back to the start screen. 


![end](https://user-images.githubusercontent.com/95367525/180020483-9eac06d8-9b44-4098-85a3-dc0f6a7569db.PNG)

### Changing the level layout

The user has the option to change the level layout by accessing the gameDifficulty.txt file in the levels folder in the project. Each of the 3 levels is labeled and the layout shown.  

![l](https://user-images.githubusercontent.com/95367525/180021915-8a5a1ca7-45ff-4faf-a5d0-5485f27cc2cf.PNG)

* Whit 'SSS' is labeled the location of the score counter
* The walls are represented by '#'
* The player starting position is represented by '@'
* The enemies starting positions are represented by 'X'

By changing these characters the user can customize their level layout.  
