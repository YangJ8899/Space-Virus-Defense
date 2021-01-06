from pygame import *
import random


import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(0, 25) #Sets the  window to open in the top left corner
lastTime = time.get_ticks()
fps = time.Clock()

init()

SIZE = (1000, 700)
screen = display.set_mode(SIZE)
titles = font.SysFont('Razor', 100)     #Initializing the fonts
lives = font.SysFont('Comic Sans',25)
infoFont = font.SysFont('Comic Sans', 25)
mainText = font.SysFont('Razor', 50)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
ORANGE = (255,165,0)

KEY_LEFT = False
KEY_RIGHT = False   #Booleans for the keys
KEY_UP = False
KEY_DOWN = False

bonusLife = False

MASTER = 1

startx = 490  #Starting position for the plane
starty = 500 

backgroundy = 0

bonusx = random.randint(0,800)
bonusy = -200

virusx = random.randint(25,275)             #Starting positions for the 3 viruses
virusx1 = random.randint(750,925)
virusx2 = random.randint(400,650)
virusy = random.randint(-2000,-1500)
virusy1 = random.randint(-1000,-500)
virusy2 = random.randint(-100,-50)


mx = 0      #Empty variables that will be changed later
my = 0
button = 0
button1 = 0

score = 0
levelspeed = 0 

mainRect = [Rect(200,200,200,100),Rect(950,650,50,50),Rect(200,400,200,100)]  #Main rectangles for instructions, and PLAY GAME

life = 4            #Life count of the player
healthValue = [50,50,50]        #Health bar for the computers
virusHealth = [30,20,10]        #Health bar for viruses

player = image.load('assets/PlayerShip.png').convert_alpha()
player = transform.scale(player,(75,100))      #Loading in all the images
ship2 = transform.scale(image.load('assets/ship2.png').convert_alpha(),(75,100))
keys = image.load("assets/keys.png")
background = image.load('assets/background.jpg').convert()
bonusItem = image.load('assets/bonusItem.png').convert_alpha()
bonusItem = transform.scale(bonusItem,(50,50))
virus = transform.scale(image.load('assets/virus1.png').convert_alpha(),(75,75))
virus1 = transform.scale(image.load('assets/virus2.png').convert_alpha(),(75,75))
virus2 = transform.scale(image.load('assets/virus3.png').convert_alpha(),(75,75))
heart = transform.scale(image.load('assets/heart.png').convert_alpha(),(50,50))
heart1 = transform.scale(image.load('assets/heart.png').convert_alpha(),(50,50))
heart2 = transform.scale(image.load('assets/heart.png').convert_alpha(),(50,50))
menuBackground = image.load('assets/menuBackground.jpg').convert()
gameTitle = transform.scale(image.load('assets/Title.png').convert_alpha(),(900,50))
scoreKeep = transform.scale(image.load('assets/score.png').convert_alpha(),(100,25))
computer = transform.scale(image.load('assets/Computer.png').convert_alpha(),(250,150))   
gameOverPic = image.load('assets/gameOver.jpg').convert()
highscore = transform.scale(image.load('assets/highScore.png').convert_alpha(),(150,25))
gameOverTXT = transform.scale(image.load('assets/gameOverTXT.png').convert_alpha(),(500,100))
infoBG = image.load('assets/infoBackGround.jpg').convert()
power = transform.scale(image.load('assets/power.jpg').convert_alpha(),(50,50))
back = transform.scale(image.load('assets/back.png').convert_alpha(),(50,50))

heartList = [heart,heart1,heart2]
missileList = []        #Lists for the missiles
missileListx = []

def drawMenu(MASTER, mx, my, button):   #Function to draw the main menu
    if MASTER == 1:
        if MASTER >= 1:
            mixer.music.load("assets/spaceMusic.mp3")
            mixer.music.play(-1)        #Plays the music during main screen, game screen and info screen
            mixer.music.set_volume(0.3)                 
        screen.fill(WHITE)
        screen.blit(menuBackground,(0,0))
        screen.blit(gameTitle,(50,100))
        draw.rect(screen,GREEN,(mainRect[0]))
        draw.rect(screen,GREEN,(mainRect[2]))
        draw.rect(screen,GREEN,(mainRect[1]))        
        game = mainText.render("Play Game",1,RED)
        info = mainText.render("Controls",1,RED)
        screen.blit(game,(210,225))
        screen.blit(info,(210,425))
        screen.blit(power,(mainRect[1]))
        if mainRect[2].collidepoint(mx,my) == True:
            draw.rect(screen,BLUE,(mainRect[2]))
            screen.blit(info,(210,425))
            if button == 1:
                MASTER = 2
        if mainRect[1].collidepoint(mx,my) == True:
            if button == 1:
                MASTER = -1
        if mainRect[0].collidepoint(mx,my) == True:
            draw.rect(screen,BLUE,(mainRect[0]))
            screen.blit(game,(210,225))
            if button == 1:
                MASTER = 3
        
    return MASTER,mx,my,button
        
    
def info(MASTER, mx, my, button):    #Function to draw the instructions screen
    if MASTER == 2:
        screen.fill(WHITE)
        screen.blit(infoBG,(0,0))
        screen.blit(keys,(50,100))
        help = titles.render("How To Play/Controls",1,BLUE)
        screen.blit(help,(150,25))
        draw.rect(screen,GREEN,(mainRect[1]))           
        controls = infoFont.render("Use arrow keys to move",1,ORANGE)
        shoot = infoFont.render("Tap space to shoot, *Note, there is a cooldown on the missiles",1,ORANGE)
        screen.blit(controls,(300,200))
        screen.blit(shoot,(300,230))
        screen.blit(bonusItem,(50,300))
        bonusInfo = infoFont.render("Collect these if you get hit by a virus to regain health",1,ORANGE)
        screen.blit(bonusInfo,(120,325))
        screen.blit(computer,(50,400))
        compInfo = infoFont.render("Protect these from getting hit by the viruses",1,ORANGE)
        compInfo2 = infoFont.render("If all 3 of them get infected or you lose all 3 hearts, its game over",1,ORANGE)
        screen.blit(compInfo,(320,475))
        screen.blit(compInfo2,(320,510))
        virusInfo = infoFont.render("The purple virus is the slowest, but takes 3 hits to kill",1,ORANGE)
        virusInfo1 = infoFont.render("The blue virus is the middle man, takes 2 hits to kill",1,ORANGE)
        virusInfo2 = infoFont.render("The green virus is the fastest, but only takes 1 hit to kill",1,ORANGE)
        screen.blit(virus,(50,570))
        screen.blit(virus1,(130,570))
        screen.blit(virus2,(210,570))
        screen.blit(virusInfo,(295,580))
        screen.blit(virusInfo1,(295,615))
        screen.blit(virusInfo2,(295,650))
        screen.blit(back,(mainRect[1]))
        if mainRect[1].collidepoint(mx,my) == True:
            if button == 1:
                MASTER = 1
    return MASTER, mx, my, button

def gameOver(MASTER, mx, my, button):       #Function that draws the game over screen
    if MASTER == 0:
        screen.fill(WHITE)
        topScore = open('assets/scoreKeep.txt','r')    #Allows the highscore to be shown on the game over screen
        highScore = int(topScore.readline())
        topScore.close()        
        screen.blit(gameOverPic,(0,0))
        screen.blit(gameOverTXT,(200,200))
        draw.rect(screen,GREEN,(mainRect[1]))
        draw.rect(screen,GREEN,(mainRect[2]))
        retry = mainText.render('play again',1,RED)
        screen.blit(retry,(215,430))  
        screen.blit(highscore,(400,600))
        highscore_ = lives.render(str(highScore),1,WHITE)
        screen.blit(highscore_,(565,605))
        screen.blit(back,(mainRect[1]))
        if mainRect[1].collidepoint(mx,my) == True:
            if button == 1:
                MASTER = 1
        elif mainRect[2].collidepoint(mx,my) == True:
            draw.rect(screen,BLUE,(mainRect[2]))
            screen.blit(retry,(215,430))
            if button == 1:                               
                MASTER = 3

    return MASTER,mx,my,button    

def character(MASTER,mx,my,button,button1):
    if MASTER == 3:
        screen.fill(WHITE)
        screen.blit(background,(0,0))
        select = titles.render("Please select a ship",1,GREEN)
        screen.blit(select,(200,300))
        shiprect = [Rect(200,500,75,100),Rect(700,500,75,100)]
        screen.blit(player,(shiprect[0]))
        screen.blit(ship2,(shiprect[1]))
        if shiprect[0].collidepoint(mx,my) == True:
            if button == 1:
                button1 = 1
                MASTER = 4
        if shiprect[1].collidepoint(mx,my) == True:
            if button == 1:
                button1 = 2
                MASTER = 4
    
    return MASTER,mx,my,button,button1
    
   
def mainGame(MASTER,mx,my,button,button1,startx,starty,backgroundy,bonusx,bonusy,virusx,virusx1,virusx2,virusy,virusy1,virusy2,life,score,healthValue,virusHealth,levelspeed,bonusLife):   #Function for the main game
    if MASTER == 4:
        screen.fill(WHITE)   
        LIFE = lives.render("Lives: ",1,WHITE)
        score_ = lives.render(str(score),1,WHITE)
        if score >= 0 and score < 300:    #Beginning levelspeed of 0.5 when score is 100
            levelspeed = 0.5
        if score >= 300:    #Game starts speeding up once the user gets 300 points
            levelspeed += 0.0003
        
        topScore = open('assets/scoreKeep.txt','r')  
        highScore = int(topScore.readline())
        topScore.close()            
        if score > highScore:     
            saveScore = open('assets/scoreKeep.txt','w')   #Reading and writing to a file so I can save the high score
            saveScore.write(str(score))
            saveScore.close()
            
        for i in range(-900, 900, 150):      #Loop that allows the background to move
            screen.blit(background,(0,backgroundy+i))
        backgroundy += levelspeed
        if backgroundy <= 700:
            backgroundy += 1
        if backgroundy >= 700:
            backgroundy = 100
        if backgroundy <= 0:
            backgroundy = 100
        
            
        for i in range(-900, 900, 150):     #Loop that allows the viruses to move and the health bars
            screen.blit(virus,(virusx,virusy))
            screen.blit(virus1,(virusx1,virusy1))
            screen.blit(virus2,(virusx2,virusy2))
            draw.rect(screen,RED,(virusx + 10,virusy - 20,60,20))
            if virusHealth[0] > 0:
                draw.rect(screen, GREEN, (virusx + 10,virusy - 20,(60-(2*(30-virusHealth[0]))),20))
            draw.rect(screen,RED,(virusx1 + 20,virusy1 - 20,40,20))
            if virusHealth[1] > 0:
                draw.rect(screen, GREEN, (virusx1 + 20,virusy1 - 20,(40-(2*(20-virusHealth[1]))),20))
            draw.rect(screen,RED, (virusx2 + 30,virusy2 - 20,20,20))
            if virusHealth[2] > 0:
                draw.rect(screen, GREEN, (virusx2 + 30,virusy2 - 20,(20-(2*(10-virusHealth[2]))),20))
        
        if button1 == 1:
            screen.blit(player,(startx,starty))     #Blits the player on the screen
        else:
            screen.blit(ship2,(startx,starty))
                
        if bonusLife == True:   #Statement to see if the bonus item shoudl spawn
            for i in range(-900,900,150):
                screen.blit(bonusItem,(bonusx,bonusy))
            bonusy += 0.5 + levelspeed
            
        playerRect = Rect(startx,starty,75,100)
        bonusRect = Rect(bonusx,bonusy,50,50)
        virusRect = Rect(virusx,virusy,75,75)       #All the rectangles for the objects
        virus1Rect = Rect(virusx1,virusy1,75,75)  
        virus2Rect = Rect(virusx2,virusy2,75,75)
        compRect = [Rect(25,575,250,150),Rect(400,575,250,150),Rect(750,575,250,150)]
        
        screen.blit(computer,(25,575))
        screen.blit(computer,(400,575))
        screen.blit(computer,(750,575))
        
        draw.rect(screen,RED,(100,675,100,20))
        draw.rect(screen,RED,(450,675,100,20))
        draw.rect(screen,RED,(800,675,100,20))
        
        if healthValue[0] > 0:
            draw.rect(screen, GREEN, (100,675,(100-(2*(50-healthValue[0]))),20))        #Drawing the health bar for the computers
        if healthValue[1] > 0:
            draw.rect(screen, GREEN, (450,675,(100-(2*(50-healthValue[1]))),20))
        if healthValue[2] > 0:
            draw.rect(screen, GREEN, (800,675,(100-(2*(50-healthValue[2]))),20))
        
        if button1 == 1:
            screen.blit(player,(startx,starty))     #Blits the player on the screen
        else:
            screen.blit(ship2,(startx,starty))
        screen.blit(scoreKeep,(750,50))
            
        if virusRect.colliderect(compRect[0]) == True:      #Checking to see if the viruses touch the computers, and if they do, resetting the viruses back off the screen
            healthValue[0] -= 10                            #If the computer has 0 health, the virus would then spawn on another computer
            virusy = random.randint(-2000,-1500)
            virusHealth[0] = 30
            if healthValue[0] <= 0:
                virusx = random.randint(400,650)
                virusHealth[0] = 30
        if virusRect.colliderect(compRect[1]) == True:
            healthValue[1] -= 10
            virusy = random.randint(-2000,-1500)
            virusHealth[0] = 30
            if healthValue[1] <= 0:
                virusx = random.randint(750,925)
                virusHealth[0] = 30
        if virusRect.colliderect(compRect[2]) == True:
            healthValue[2] -= 10
            virusy = random.randint(-2000,-1500)
            virusHealth[0] = 30
        if virus1Rect.colliderect(compRect[2]) == True:
            healthValue[2] -= 10
            virusy1 = random.randint(-1000,-500)
            virusHealth[1] = 20
            if healthValue[2] <= 0:
                virusx1 = random.randint(400,650)
                virusHealth[1] = 20
        if virus1Rect.colliderect(compRect[1]) == True:
            healthValue[1] -= 10
            virusy1 = random.randint(-1000,-500)
            virusHealth[1] = 20
            if healthValue[1] <= 0:
                virusx1 = random.randint(25,275)
                virusHealth[1] = 20
        if virus1Rect.colliderect(compRect[0]) == True:
            healthValue[0] -= 10
            virusy1 = random.randint(-1000,-500)
            virusHealth[1] = 20
        if virus2Rect.colliderect(compRect[1]) == True:
            healthValue[1] -= 10
            virusy2 = random.randint(-500,-200)
            virusHealth[2] = 10
            if healthValue[1] <= 0:
                virusx2 = random.randint(25,275)
                virusHealth[2] = 10
        if virus2Rect.colliderect(compRect[0]) == True:
            healthValue[0] -= 10
            virusy2 = random.randint(-500,-200)
            virusHealth[2] = 10
                
        if healthValue[0] <= 0:     #If the computer has 0 health, lose 1 life
            life -= 1
            bonusLife = False
            if life <= 1:   #If the user has one life and a computer dies, game over
                button = 0
                startx = 490
                starty = 500
                virusy = random.randint(-1500,-1250)    #Resets all the coordinates back to the original positions
                virusy1 = random.randint(-1000,-500)
                virusx = random.randint(0,200)  
                virusx1 = random.randint(0,400)
                virusy2 = random.randint(-500,-200)
                virusx2 = random.randint(400,650)                
                healthValue = [50,50,50]
                virusHealth = [30,20,10] 
                life = 4
                score = 0
                levelspeed = 0 
                bonusLife = False
                MASTER = 0
                if score > highScore:
                    saveScore = open('assets/scoreKeep.txt','w')
                    saveScore.write(str(score))
                    saveScore.close()                                    
        elif healthValue[1] <= 0: #Checks it for computer 2
            life -= 1
            bonusLife = False
            if life <= 1:  
                button = 0
                startx = 490
                starty = 500
                virusy = random.randint(-1500,-1250)
                virusy1 = random.randint(-1000,-500)
                virusx = random.randint(0,200)  
                virusx1 = random.randint(0,400)
                virusy2 = random.randint(-500,-200)
                virusx2 = random.randint(400,650)                
                healthValue = [50,50,50]
                life = 4
                score = 0
                levelspeed = 0 
                bonusLife = False
                MASTER = 0
                virusHealth = [30,20,10] 
                if score > highScore:
                    saveScore = open('assets/scoreKeep.txt','w')
                    saveScore.write(str(score))
                    saveScore.close()                                
        elif healthValue[2] <= 0:   #Checks for computer 3
            life -= 1
            bonusLife = False
            if life <= 1:   
                button = 0
                startx = 490
                starty = 500
                virusy = random.randint(-1500,-1250)
                virusy1 = random.randint(-1000,-500)
                virusx = random.randint(0,200)  
                virusx1 = random.randint(0,400)
                virusy2 = random.randint(-500,-200)
                virusx2 = random.randint(400,650)                
                healthValue = [50,50,50]
                virusHealth = [30,20,10] 
                life = 4
                score = 0
                levelspeed = 0 
                bonusLife = False
                MASTER = 0
                if score > highScore:
                    saveScore = open('assets/scoreKeep.txt','w')
                    saveScore.write(str(score))
                    saveScore.close()                                
            
        drawMissile(missileList)
        for i in range(len(missileListx)):     #Draws the missiles and makes sure the rectangle for the missile follows it
            missileRect = Rect(missileListx[i-1],missileList[i-1],10,10)
            if missileRect.colliderect(virusRect) == True:  #Checks to see if the missile hits the virus
                virusHealth[0] -= 10
                missileListx.remove(missileListx[i-1])
                missileList.remove(missileList[i-1])
                if healthValue[0] > 0 and virusHealth[0] <= 0:  #If the health bar for the comptuers are at 0, the virus would spawn on another computer
                    score += 25                                 #The health of the virus also has to hit 0 before the virus reblits to the top of the screen
                    virusy = random.randint(-2000,-1500)
                    virusx = random.randint(25,275) 
                    virusHealth[0] = 30
                elif healthValue[0] < 0 and virusHealth[0] <= 0:
                    score += 25
                    virusx = random.randint(400,650)
                    virusy = random.randint(-2000,-1500)
                    virusHealth[0] = 30
                elif healthValue[0] <= 0 and healthValue[1] <= 0 and virusHealth[0] <= 0:
                    score += 25
                    virusy = random.randint(-2000,-1500)
                    virusx = random.randint(750,925)
                    virusHealth[0] = 30
            elif missileRect.colliderect(virus1Rect) == True:
                virusHealth[1] -= 10
                missileListx.remove(missileListx[i-1])
                missileList.remove(missileList[i-1]) 
                if healthValue[2] > 0 and virusHealth[1] <= 0:
                    score += 25
                    virusy1 = random.randint(-1000,-500)
                    virusx1 = random.randint(750,925)
                    virusHealth[1] = 20
                elif healthValue[2] <= 0 and virusHealth[1] <= 0:
                    score += 25
                    virusy1 = random.randint(-1000,-500)
                    virusx1 = random.randint(400,650)
                    virusHealth[1] = 20
            elif missileRect.colliderect(virus2Rect) == True:
                virusHealth[2] -= 10
                missileListx.remove(missileListx[i-1])
                missileList.remove(missileList[i-1]) 
                if healthValue[1] > 0 and virusHealth[2] <= 0:
                    score += 25
                    virusy2 = random.randint(-500,-200)
                    virusx2 = random.randint(400,650)
                    virusHealth[2] = 10
                elif healthValue[1] <= 0 and virusHealth[2] <= 0:
                    score += 25
                    virusy2 = random.randint(-500,-200)
                    virusx2 = random.randint(25,275)    
                    virusHealth[2] = 10
                    
        if life == 4:       #Draws the haerts on the top left
            screen.blit(heartList[0],(100,25))
            screen.blit(heartList[1],(150,25))
            screen.blit(heartList[2],(200,25)) 
        elif life == 3:
            screen.blit(heartList[0],(100,25))
            screen.blit(heartList[1],(150,25))
        else:
            screen.blit(heartList[0],(100,25))           
                  
        virusy += (0.1 + levelspeed) - 0.2    #Slowest virus    #How fast the virus will move down the screen
        virusy1 += (0.25 + levelspeed) - 0.15  #Middle speed
        virusy2 += (0.3 + levelspeed) - 0.1   #Fastest Virus

        
        screen.blit(LIFE,(50,50))
        screen.blit(score_,(860,50))
                       
        if playerRect.colliderect(virusRect) == True:   #Checks to see if the viruses hit the player
            life -= 1
            startx = 490    #If it does, player loses a life, the ship gets reset and so does the corresponding virus
            starty = 500
            virusy = random.randint(-2000,-1500)
            virusx = random.randint(25,275)  
            virusHealth[0] = 30
            if score >= 500:
                levelspeed -= 0.1   #If the score is above 500, and user gets hit, they get a grace period and the level slows down
            if life <= 2:           #Or the game would be too hard
                bonusLife = True                
                button = 0
                startx = 490
                starty = 500
                virusy = random.randint(-1500,-1250)
                virusy1 = random.randint(-1000,-500)
                virusx = random.randint(25,275)  
                virusx1 = random.randint(400,650)
                virusy2 = random.randint(-500,-200)
                virusx2 = random.randint(700,950)                
                healthValue = [50,50,50]
                virusHealth = [30,20,10] 
                life = 4
                score = 0
                levelspeed = 0 
                bonusLife = False
                MASTER = 0                
                if score > highScore:
                    saveScore = open('assets/scoreKeep.txt','w')
                    saveScore.write(str(score))
                    saveScore.close()                    
        if playerRect.colliderect(virus1Rect) == True:
            life -= 1
            startx = 490
            starty = 500            
            virusy1 = random.randint(-1000,-500)
            virusx1 = random.randint(700,950)
            virusHealth[1] = 20
            if score >= 500:
                levelspeed -= 0.1
            if life <= 2:
                bonusLife = True
            if life <= 1:
                button = 0
                startx = 490
                starty = 500
                virusy = random.randint(-1500,-1250)
                virusy1 = random.randint(-1000,-500)
                virusx = random.randint(25,275)  
                virusx1 = random.randint(400,650)
                virusy2 = random.randint(-500,-200)
                virusx2 = random.randint(700,950)                
                healthValue = [50,50,50]
                life = 4
                score = 0
                levelspeed = 0 
                bonusLife = False
                MASTER = 0
                if score > highScore:
                    saveScore = open('assets/scoreKeep.txt','w')
                    saveScore.write(str(score))
                    saveScore.close()                    
        if playerRect.colliderect(virus2Rect) == True:
            life -= 1
            startx = 490
            starty = 500            
            virusy2 = random.randint(-500,-200)
            virusx2 = random.randint(400,650)
            virusHealth[2] = 10
            if score >= 500:
                levelspeed -= 0.1  
            if life <= 2:
                bonusLife = True
            if life <= 1:
                button = 0
                startx = 490
                starty = 500
                virusy = random.randint(-1500,-1250)
                virusy1 = random.randint(-1000,-500)
                virusx = random.randint(25,275)  
                virusx1 = random.randint(700,900)
                virusy2 = random.randint(-500,-200)
                virusx2 = random.randint(400,650)                
                healthValue = [50,50,50]
                virusHealth = [30,20,10] 
                life = 4
                score = 0
                levelspeed = 0    
                bonusLife = False
                MASTER = 0
                if score > highScore:
                    saveScore = open('assets/scoreKeep.txt','w')
                    saveScore.write(str(score))
                    saveScore.close()                    
        if playerRect.colliderect(bonusRect) == True:   #If you have less than 3 hearts, then u can get another life
            if life < 4:
                life += 1
                bonusx = random.randint(0,800)
                bonusy = -400  
        if healthValue[0] <= 0 and healthValue[1] <= 0 and healthValue[2] <= 0:     #If all 3 computers are at 0 hp, game over
            button = 0
            startx = 490
            starty = 500
            virusy = random.randint(-500,-200)
            virusy1 = random.randint(-500,-200)
            virusx = random.randint(25,275)  
            virusx1 = random.randint(700,900)
            virusy2 = random.randint(-500,-200)
            virusx2 = random.randint(400,650)            
            life = 4
            healthValue = [50,50,50]
            virusHealth = [30,20,10] 
            score = 0
            levelspeed = 0
            MASTER = 0
            if score > highScore:
                saveScore = open('assets/scoreKeep.txt','w')
                saveScore.write(str(score))
                saveScore.close()                
        if startx > 1000 or startx < 0: #If the user goes off the screen, you lose one life
            life -= 1
            startx = 490
            starty = 500
            if life <= 2:
                bonusLife = True
            if life <= 1:
                button = 0
                startx = 490
                starty = 500
                virusy = random.randint(-500,-200)
                virusy1 = random.randint(-500,-200)
                virusx = random.randint(25,275)  
                virusx1 = random.randint(700,900)
                virusy2 = random.randint(-500,-200)
                virusx2 = random.randint(400,650)            
                life = 4
                healthValue = [50,50,50]
                virusHealth = [30,20,10] 
                score = 0
                levelspeed = 0
                MASTER = 0                
                
        elif starty > 700 or starty < 0:
            life -= 1
            startx = 490
            starty = 500
            if life <= 2:
                bonusLife = True
            if life <= 1:
                button = 0
                startx = 490
                starty = 500
                virusy = random.randint(-500,-200)
                virusy1 = random.randint(-500,-200)
                virusx = random.randint(25,275)  
                virusx1 = random.randint(700,900)
                virusy2 = random.randint(-500,-200)
                virusx2 = random.randint(400,650)            
                life = 4
                healthValue = [50,50,50]
                virusHealth = [30,20,10] 
                score = 0
                levelspeed = 0
                MASTER = 0                
        
    return MASTER,mx,my,button,button1,startx,starty,backgroundy,bonusx,bonusy,virusx,virusx1,virusx2,virusy,virusy1,virusy2,life,score,healthValue,virusHealth,levelspeed,bonusLife
        
def drawMissile(missiles):
    for i in range(len(missileListx)):
        missile = Rect(missileListx[i], missileList[i], 10, 10)
        draw.rect(screen, RED, missile)
        
def moveMissiles(missiles):
    for index in range(len(missiles) - 1, -1, -1):
        missiles[index] -= 2  # will move the missiles up 2
        if missiles[index] < 0: # if it has gone off the horizon, lets remove
            del(missiles[index])  
            del(missileListx[index])
    

running = True
while running: 
    moveMissiles(missileList)
    button = 0   #Sets it back to 0 everytime it is clicked
    for evnt in event.get():   # checks all events that happen
        if evnt.type == QUIT or MASTER == -1:
            running = False
        if evnt.type == MOUSEBUTTONDOWN:
            mx, my = evnt.pos          
            button = evnt.button  
        if evnt.type == MOUSEMOTION:
            mx, my = evnt.pos    
        
        if evnt.type == KEYDOWN:
            if evnt.key == K_LEFT:
                KEY_LEFT = True
            elif evnt.key == K_RIGHT:
                KEY_RIGHT = True
            elif evnt.key == K_UP:
                KEY_UP = True
            elif evnt.key == K_DOWN:
                KEY_DOWN = True 
            elif evnt.key == K_SPACE:
                newMissilex = startx + 33
                newMissile = starty # keeping track of the y value of the missile
                if time.get_ticks() - lastTime > 200:
                    missileList.append(newMissile)
                    missileListx.append(newMissilex)
                    lastTime = time.get_ticks()
                    
        if evnt.type == KEYUP:
            if evnt.key == K_LEFT:
                KEY_LEFT = False        #If no keyes are pressed, the keys will be false
            if evnt.key == K_RIGHT:
                KEY_RIGHT = False
            if evnt.key == K_UP:
                KEY_UP = False
            if evnt.key == K_DOWN:
                KEY_DOWN = False
    
    if KEY_LEFT == True:
        startx -= 4         #The amount the palyer moves by
    if KEY_RIGHT == True:
        startx += 4
    if KEY_UP == True:
        starty -= 4
    if KEY_DOWN == True:
        starty += 4

    
    MASTER,mx,my,button = drawMenu(MASTER,mx,my,button)
    MASTER,mx,my,button = info(MASTER,mx,my,button)         #Re globalizing the functions
    MASTER,mx,my,button = gameOver(MASTER,mx,my,button)
    MASTER,mx,my,button,button1 = character(MASTER,mx,my,button,button1)
    MASTER,mx,my,button,button1,startx,starty,backgroundy,bonusx,bonusy,virusx,virusx1,virusx2,virusy,virusy1,virusy2,life,score,healthValue,virusHealth,levelspeed,bonusLife = mainGame(MASTER,mx,my,button,button1,startx,starty,backgroundy,bonusx,bonusy,virusx,virusx1,virusx2,virusy,virusy1,virusy2,life,score,healthValue,virusHealth,levelspeed,bonusLife)
    display.update()
    fps.tick(240)
