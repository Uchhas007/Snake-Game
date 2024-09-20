'''
the blueprint of our snake game is
https://www.codewithharry.com/videos/python-game-development-8/
'''
import random
import time
import pygame

# Initialising pygame and setting up the clock
pygame.init()
clock = pygame.time.Clock() # using the clock module of pygame for better physics (ex: velocity) & graphics in game
font = pygame.font.SysFont(None, 55) # defining the font

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game") # Game Title
pygame.display.update()

# Colours for our display (RGB)
white = (255, 255, 255) # hence white colour have all colours
red = (255, 0, 0)
black = (0, 0, 0) # black is not a colour its a race
# c = (0, 255, 255) # combining RGB for new colour

def text_screen(text, color, x, y): # (text to be displayed, colour of text, position (x, y) of text on display)
    screen_text = font.render(text, True, color) # (text, resoloution management?, colour of text)
    gameWindow.blit(screen_text, [x,y]) # where to show.blit(saved text, [coordinate of display where text is to be displayed])

def plot_snake(gameWindow, color, snk_list, snake_size):
    # print(snk_list)
    for x,y in snk_list:
        # print(x, y)
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((black))
        text_screen("Welcome to Snake Game!", white, 200, 200)
        text_screen("Press Space To Play", white, 200, 300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()

        pygame.display.update()
        clock.tick(60)

# Game Loop: (Less functions = fast processing)
def gameloop():
    # Game specific variables
    exit_game = False # will be true if player wants to quit
    game_over = False # will be true if the snake crashes with wall or eats itself up

    # snake variables
    snake_x = 50 # initialising the x coordinate of the snake
    snake_y = 50 # initialising the y coordinate of the snake
    snake_size = 10 # initialising the size of the snake
    snk_list = [] # this will become a 2D list which will keep increasing in size evertime the snake eats a food
    snk_length = 1 # initial length of the snake

    # Motion Variables. defining the velocity of our snake. VVV Important for vector motions
    velocity_x = 0
    velocity_y = 0
    initial_velocity = 10 # better to use variable for code reusability
    fps = 60 # defining the frame rate of our game


    # defining a random position for the food where the food will appear randomly
    food_x = random.randint(0, int(screen_width/2)) # the food will be produced within the screen width
    food_y = random.randint(0, int(screen_height/2.5)) # dividing by 2 so that the food don't go to the edge of the screen

    # saving the scores of the player & displaying it
    score = 0
    c = 0

    while not exit_game:
        if game_over:
            gameWindow.fill(white)
            text_screen("Game Over! Press Enter To Continue", red, 100, 250)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = 10 # maintaining the vector
                        velocity_y = 0 # so that snake don't move diagonally

                    if event.key == pygame.K_LEFT:
                        velocity_x = - initial_velocity # code reusability
                        velocity_y = - 0

                    if event.key == pygame.K_UP:
                        velocity_y = - 10
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = initial_velocity
                        velocity_x = 0
                        # velocity_x = 10 # in this the snake will go horizontal i.e. resultant vector velocity
                    
                    # cheatcode
                    if event.key == pygame.K_s:
                        if c != 3:
                            score += 5
                        else:
                            continue
                        c+=1
                        print(c)

            # other variables that will change while we play the game
            
            # chnaging the postion of our snake & it'll keep happening on loop wheather we press keys or not
            snake_x = snake_x + velocity_x # using vector. velocity changes = direction changes
            snake_y = snake_y + velocity_y
            
            # defining our precision by matching the coordinate of the head of the snake with the food's coordinate
            if abs(snake_x - food_x)<6 and abs(snake_y - food_y)<6:
                score +=10 # if the difference of x & y coordinate of head & food decrease then it'll be a score
                snk_length += 5 # abh jaab khana kha hi liya tabh bara bhi toh hona parega na
                # hence it's a score, the food will be replaced in a different position
                food_x = random.randint(20, int(screen_width / 2))
                food_y = random.randint(20, int(screen_height / 2))

            gameWindow.fill(white) # this will be painted first. i.e. white colour will stay at the bottom. Important
            # displaying the text on screen
            text_screen("Score: " + str(score), red, 5, 5) # the function takes the fist arg as string with no commas allowed        

            # maintaining the size of the snake
            # we did this whole thing in the form of Linked List.
            head = [] # Initially head and tail are the same thing. So we'll just append the coordinate of the head of the snake here
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head) # snk_lst will now become a nested list
            
            if len(snk_list)>snk_length: # as the lenght of snake increase, we'll delete the head of the snake for better motion
                del snk_list[0] # deleting the element in the 0th index
            
            # Handle the collision of the snake with wall
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
            
            # handling auto canibalism
            '''
            Head is the last element of the snklist. So other than the last elemnt of the snklst if any coordinate matches with head then GG
            ''' 
            if head in snk_list[:-1]: 
                game_over = True

        
        # to draw anything in pygame dsiplay we'll say pygame.draw and then .rect i.e. what shape we want to draw
        # pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size]) # (where we want to draw, colour of our object, [x_pos, y_pos, length, breadth])
        pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
        plot_snake(gameWindow, black, snk_list, snake_size) # calling the plot_snake function
        
        pygame.display.update() # if we bring any cng in our display we must run this code to update our display
        clock.tick(fps) # to maintain the frame rate

    pygame.quit()
    quit()
welcome()