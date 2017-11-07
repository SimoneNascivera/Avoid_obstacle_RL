import avoidobstacle

game = avoidobstacle.AvoidObstacle()
frame = game.getPresentFrame()
while 1:
	reward_t, frame = game.getNextFrame([0,0,1], [1,1, 1, 1])
