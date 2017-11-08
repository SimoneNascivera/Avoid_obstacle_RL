# This code is based on https://github.com/wh33ler/QNet_Pong/blob/master/pong.py
# This code was by wh33ler. I changed it to be suitable for my scope and documented it.
 
import pygame # simple library to develop simple python games
import random # simple library to generate random numbers

#size of our window
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

#size of our OBSTACLE
OBSTACLE_WIDTH = 10
OBSTACLE_HEIGHT = 180
OBSTACLE_SPACE = 30
#size of our SHIP
SHIP_WIDTH = 10
SHIP_HEIGHT = 10
#distance from the edge of the window
SHIP_BUFFER = 10
SHIP_SPEED = 5

#RGB colors for our paddle and ball
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#initialize our screen using width and height vars
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#draw the pipe
def drawObstacle(center):
    obstacle = pygame.Rect(WINDOW_WIDTH/2,  center + OBSTACLE_SPACE, OBSTACLE_WIDTH, WINDOW_HEIGHT-center-OBSTACLE_SPACE)
    obstacle1 = pygame.Rect(WINDOW_WIDTH/2, 0, OBSTACLE_WIDTH, center-OBSTACLE_SPACE)
    pygame.draw.rect(screen, WHITE, obstacle)
    pygame.draw.rect(screen, WHITE, obstacle1)

#draw the little ship
def drawShip(shipYPos, shipXPos):
    #create it
    paddle1 = pygame.Rect(shipXPos, shipYPos, SHIP_WIDTH, SHIP_HEIGHT)
    #draw it
    pygame.draw.rect(screen, WHITE, paddle1)

def drawScore(score, neg):    
    font = pygame.font.Font(None, 28)    
    scorelabel = font.render("Score " + str(score), 1, WHITE)
    screen.blit(scorelabel, (30 , 10))
    font = pygame.font.Font(None, 28)    
    scorelabel = font.render("Failed " + str(neg), 1, WHITE)
    screen.blit(scorelabel, (30 , 50))
  
#draw infos on the top of the screen    
def drawInfos(infos, action):
    font = pygame.font.Font(None, 15)
    if(infos[3] != 'model only'):        
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
		
#update the paddle position
def updateShip(action, shipYPos, shipXPos, center):
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
    if((shipXPos >= WINDOW_WIDTH/2) and ((shipYPos> (center + OBSTACLE_SPACE-15)) or (shipYPos< (center -( OBSTACLE_SPACE-15))))):		
		center = random.randint(0, 370)
		shipXPos = 0
		shipYPos = WINDOW_HEIGHT / 2 - SHIP_HEIGHT / 2
		score = -1
    if((shipXPos >= WINDOW_WIDTH/2+50) and (shipYPos< (center + OBSTACLE_SPACE-15)) and (shipYPos> (center -( OBSTACLE_SPACE-15)))):
		center = random.randint(0, 370)
		shipXPos = 0
		shipYPos = WINDOW_HEIGHT / 2 - SHIP_HEIGHT / 2
		score = 1
    return shipYPos, shipXPos, center, score

#game class
class AvoidObstacle:
    def __init__(self):
        pygame.font.init()
        #random number for initial direction of ball
        num = random.randint(0,9)
        #keep score
        self.neg = 0
        self.tally = 0
        #initialie positions of paddle
        self.shipYPos = WINDOW_HEIGHT / 2 - SHIP_HEIGHT / 2
    # the initial frae
    def getPresentFrame(self):
        #for each frame, calls the event queue
        pygame.event.pump()
        #make the background black
        screen.fill(BLACK)
        #draw obstacles
        self.center = random.randint(0, 370)
        drawObstacle(self.center)
        #draw our ship
        self.shipXPos = SHIP_BUFFER
        drawShip(self.shipYPos, self.shipXPos)
        #draw our ball
        drawScore(self.tally, self.neg)  
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
        self.shipYPos, self.shipXPos, self.center, score = updateShip(action, self.shipYPos, self.shipXPos, self.center)
        if(score == -1):
			self.neg = self.neg + 1
        drawObstacle(self.center)
        if(self.shipXPos > WINDOW_WIDTH):
			self.shipXPos = SHIP_BUFFER
        drawShip(self.shipYPos, self.shipXPos)
        #get the surface data
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        drawScore(self.tally, self.neg)  
        drawInfos(infos, action)
        #update the window
        pygame.display.flip()
        #record the total score
        self.tally = self.tally + score     
        #return the score and the surface data
        return [score, image_data]
