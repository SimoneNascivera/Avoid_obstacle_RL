import pygame #helps us make GUI games in python
import random #help us define which direction the ball will start moving in

#DQN. CNN reads in pixel data. 
#reinforcement learning. trial and error.
#maximize action based on reward
#agent envrioment loop
#this is called Q Learning
#based on just game state. mapping of state to action is policy
#experience replay. learns from past policies


#size of our window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

#size of our OBSTACLE
OBSTACLE_WIDTH = 10
OBSTACLE_HEIGHT = 180

#size of our SHIP
SHIP_WIDTH = 10
SHIP_HEIGHT = 10
#distance from the edge of the window
SHIP_BUFFER = 0
SHIP_SPEED = 5

#RGB colors for our paddle and ball
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#initialize our screen using width and height vars
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

def drawObstacle():
    #small rectangle, create it
    obstacle = pygame.Rect(WINDOW_WIDTH/2, WINDOW_HEIGHT - 300, OBSTACLE_WIDTH, 300)
    obstacle1 = pygame.Rect(WINDOW_WIDTH/2, 0, OBSTACLE_WIDTH, 50)
    #draw it
    pygame.draw.rect(screen, WHITE, obstacle)
    pygame.draw.rect(screen, WHITE, obstacle1)


def drawShip(shipYPos, shipXPos):
    #create it
    ship = pygame.Rect(shipXPos, shipYPos, SHIP_WIDTH, SHIP_HEIGHT)
    #draw it
    pygame.draw.rect(screen, WHITE, ship)

def drawScore(score):    
    font = pygame.font.Font(None, 28)    
    scorelabel = font.render("Score " + str(score), 1, WHITE)
    screen.blit(scorelabel, (30 , 10))
    
def drawInfos(infos, action):
    font = pygame.font.Font(None, 15)        
    label = font.render("step " + str(infos[0]) + " ["+str(infos[3])+"]", 1, WHITE)
    screen.blit(label, (30 , 30))
    label = font.render("epsilon " + str(infos[2]), 1, WHITE)
    screen.blit(label, (30 , 45))
    label = font.render("q_max " + str(infos[1]), 1, WHITE)
    screen.blit(label, (30 , 60))
    actionText = "--"
    if (action[1] == 1):
        actionText = "Up"
    if (action[2] == 1):
        actionText = "Down"
    label = font.render("action " + actionText, 1, WHITE)
    screen.blit(label, (30 , 75))

#[score, shipYPos, paddle2YPos, ballXPos, ballYPos, ballXDirection, ballYDirection]

#update the paddle position
def updateShip(action, shipYPos, shipXPos):
    #if move up
    if (action[1] == 1):
        shipYPos = shipYPos - SHIP_SPEED
    #if move down
    if (action[2] == 1):
        shipYPos = shipYPos + SHIP_SPEED

    #don't let it move off the screen
    if (shipYPos < 0):
        shipYPos = 0
    if (shipYPos > WINDOW_HEIGHT - SHIP_HEIGHT):
		shipYPos = WINDOW_HEIGHT - SHIP_HEIGHT
    shipXPos = shipXPos + SHIP_SPEED
    score = 0 
    if((shipXPos >= WINDOW_WIDTH/2+100) and (shipYPos > 55 and shipYPos < WINDOW_HEIGHT - 305)):
		shipXPos = 0
		shipYPos = WINDOW_HEIGHT / 2 - SHIP_HEIGHT / 2
		score = 1
    if((shipXPos >= WINDOW_WIDTH/2) and (not(shipYPos > 55) or not(shipYPos < WINDOW_HEIGHT - 305))):
		shipXPos = 0
		shipYPos = WINDOW_HEIGHT / 2 - SHIP_HEIGHT / 2
		score = -1
    return shipYPos, shipXPos,  score

#game class
class AvoidObstacle:
    def __init__(self):
        pygame.font.init()
        #random number for initial direction of ball
        num = random.randint(0,9)
        #keep score
        self.tally = 0
        #initialie positions of paddle
        self.shipYPos = WINDOW_HEIGHT / 2 - SHIP_HEIGHT / 2
    #
    def getPresentFrame(self):
        #for each frame, calls the event queue, like if the main window needs to be repainted
        pygame.event.pump()
        #make the background black
        screen.fill(BLACK)
        #draw obstacles
        drawObstacle()
        #draw our paddles
        self.shipXPos = SHIP_BUFFER
        drawShip(self.shipYPos, self.shipXPos)
        #draw our ball
        drawScore(self.tally)  
        #copies the pixels from our surface to a 3D array. we'll use this for RL
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        #updates the window
        pygame.display.flip()
        
        #return our surface data
        return image_data

    #update our screen
    def getNextFrame(self, action, infos):
        pygame.event.pump()
        score = 0
        screen.fill(BLACK)
        #update our paddle
        self.shipYPos, self.shipXPos, score = updateShip(action, self.shipYPos, self.shipXPos)
        drawObstacle()
        if(self.shipXPos > WINDOW_WIDTH):
			self.shipXPos = SHIP_BUFFER
        drawShip(self.shipYPos, self.shipXPos)
        #get the surface data
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        drawScore(self.tally)  
        drawInfos(infos, action)
        #update the window
        pygame.display.flip()
        #record the total score
        self.tally = self.tally + score   
        #return the score and the surface data
        return [score, image_data]
