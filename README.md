# Content-Adaptation

## Research

To view the conclusion of the project, open up **ContentAdaptationReport.pdf**. All resources I used in my research are included in the __write-up__ folder. This includes papers I read, previous iterations of code as well as earlier research drafts.

## Code

###### Game State

Game state is stored as the heights of the ten columns on the tetris board, the block being dropped(S = 0, L = 3 etc.), the blocks orientation(0, 1, 2, 3), the blocks x and y co-ordinates and then the current player score. 

At each tick of the game clock; the current board state, the action the player took and the resultant game board space is stored as an entry.

> Eg: 0/0/0/0/0/0/0/0/0/0 0 1 3 1 0,Right,0/0/0/0/0/0/0/0/0/0 0 1 4 1 0


###### Using the code

**adaptive.py** is the game containing the MDP look-up and user inference. It also changes the pieces and game speed presented to you depending on your infered skill level. MDPS for each corresponding player types were stored in the following files:
- **MDPbadai.txt**
- **MDPgoodai.txt**
- **MDPhumanai.txt**

**backup/badai** is tetris played by a terrible ai.

**backup/goodai** is tetris played by a moderate ai.

**tetrishuman.py** is a normal tetris game. However, it collects data and stores it in a file called __human.txt__.

**MDP.py** takes a given data text file and converts it into a Markov Decision Process




