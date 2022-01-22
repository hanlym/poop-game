#P.O.O.P. - Perfectly Operational Offensives Program
#warning: it will very quickly become evident that i know nothing about game development or graphic design
import pygame
import os
from random import randint

#set up window
WIDTH, HEIGHT = 900, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("P.O.O.P.")

fps = 60

#counter to keep track of the current stage
stageCount = 0

#import and resize assets
playerImg = pygame.image.load(os.path.join("assets", "builder.png"))
playerImg = pygame.transform.scale(playerImg, (100, 120))

coinImg = pygame.image.load(os.path.join("assets", "money.png"))
coinImg = pygame.transform.scale(coinImg, (50, 50))

money = 0
#get amount of money
with open("data.txt", "r") as f:
    money = f.readlines()[0]

pygame.font.init()
font = pygame.font.SysFont(None, 30)
moneyAmount = font.render(money, True, (0, 0, 0))

#draw stuff
def drawBuilderWin():
    window.fill((135, 206, 235))
    pygame.draw.rect(window, (0, 255, 0), pygame.Rect(0, HEIGHT-(HEIGHT/4), WIDTH, HEIGHT/4))
    window.blit(playerImg, (WIDTH/8, HEIGHT-(HEIGHT/4)-120))
    window.blit(coinImg, (10, 10))
    window.blit(moneyAmount, (70, 25))

    #draw the buttons
    BUTTCOLOUR = (65, 65, 65) #haha butt funny
    pygame.draw.rect(window, BUTTCOLOUR, pygame.Rect(650, 75, 200, 75))
    pygame.draw.rect(window, BUTTCOLOUR, pygame.Rect(650, 175, 200, 75))
    pygame.draw.rect(window, BUTTCOLOUR, pygame.Rect(650, 275, 200, 75))

    #render text for button titles
    TEXTCOLOUR = (255, 255, 255) #white
    warheadButLab = font.render("Select warhead", True, TEXTCOLOUR)
    fuselageButLab = font.render("Select fuselage", True, TEXTCOLOUR)
    boosterButLab = font.render("Select booster", True, TEXTCOLOUR)

    #put text on the buttons
    window.blit(warheadButLab, (650, 75))
    window.blit(fuselageButLab, (650, 175))
    window.blit(boosterButLab, (650, 275))

    #render text for the selection part of the buttons
    one = font.render("1", True, TEXTCOLOUR)
    two = font.render("2", True, TEXTCOLOUR)
    three = font.render("3", True, TEXTCOLOUR)

    #put selection part on buttons (add 75 to top of butt)
    #warhead select
    window.blit(one, (650, 110))
    window.blit(two, (725, 110))
    window.blit(three, (800, 110))

    #fuselage select
    window.blit(one, (650, 210))
    window.blit(two, (725, 210))
    window.blit(three, (800, 210))

    #booster select
    window.blit(one, (650, 310))
    window.blit(two, (725, 310))
    window.blit(three, (800, 310))

    #draw launch button
    pygame.draw.rect(window, (255, 0, 0), pygame.Rect(700, 400, 200, 100))

    #place text on launch button
    launch = font.render("LAUNCH", True, (0, 0, 0))
    window.blit(launch, (750, 450))

def drawMissile(booster, fuselage, warhead):
    #load in the required assets
    warheadImg = pygame.image.load(os.path.join("assets", "rocket parts", f"warhead_{warhead}.png"))
    fuselageImg = pygame.image.load(os.path.join("assets", "rocket parts", f"fuselage_{fuselage}.png"))
    boosterImg = pygame.image.load(os.path.join("assets", "rocket parts", f"booster_{booster}.png"))
    
    #draw booster
    window.blit(boosterImg, (400, 300))

    #draw fuselage
    window.blit(fuselageImg, (433, 210))

    #draw warhead (bit more fiddly because the images are different sizes)
    if warhead != 1:
        window.blit(warheadImg, (433, 135))
    else:
        window.blit(warheadImg, (433, 160))
    
    #calculate and show cost
    global cost
    cost = (300 * warhead) + (200 * fuselage) + (300 * booster)
    costTxt = font.render(f"COST: {str(cost)}", True, (255, 255, 255))
    window.blit(costTxt, (750, 480))

def launch():
    if cost > int(money):
        bigFont = pygame.font.SysFont(None, 50)
        tooExpensive = bigFont.render("UR TOO POOR", True, (0, 0, 0))
        window.blit(tooExpensive, (175, 200))
    else:
        amountLeft = int(money) - cost
        with open("data.txt", "r+") as f:
            f.truncate(0)
            f.write(str(amountLeft))
        global stageCount
        stageCount += 1

#i started rushing here so please excuse me
def drawTravelWin():
    window.fill((0, 255, 0))

#main game loop
def main():
    clock = pygame.time.Clock()

    running = True
    
    warhead = 1
    fuselage = 1
    booster = 1

    missilePos = (10, 10)
    count = 0
    travelDist = randint(100, 300)
    explosionPow = randint(100, 300)
    while running:
        clock.tick(fps)
        
        #get amount of money
        with open("data.txt", "r") as f:
            money = f.readlines()[0]

        if stageCount == 0:
            drawBuilderWin()
        if stageCount == 1:
            drawTravelWin()
            missileIcon = pygame.image.load(os.path.join("assets", "radioactive.png"))
            if count < travelDist:
                window.blit(missileIcon, missilePos)
                missilePos = (missilePos[0]+1, missilePos[1]+1)
                count += 1
            elif count >= travelDist:
                explosion = pygame.image.load(os.path.join("assets", "explosion.png"))
                window.blit(explosion, missilePos)
                results = font.render(f"Exploded successfully - Explosion: {explosionPow} explosion units", True, (0, 0, 0))
                window.blit(results, (200, 200))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            #handle button clicking events
            if event.type == pygame.MOUSEBUTTONDOWN and stageCount == 0:
                x, y = pygame.mouse.get_pos()

                #warhead select
                if 650 <= x <= 675 and 110 <= y <= 125:
                    warhead = 1
                elif 725 <= x <= 750 and 110 <= y <= 125:
                    warhead = 2
                elif 800 <= x <= 825 and 110 <= y <= 125:
                    warhead = 3

                #fuselage select
                if 650 <= x <= 675 and 210 <= y <= 225:
                    fuselage = 1
                elif 725 <= x <= 750 and 210 <= y <= 225:
                    fuselage = 2
                elif 800 <= x <= 825 and 210 <= y <= 225:
                    fuselage = 3 
                
                #booster select
                if 650 <= x <= 675 and 310 <= y <= 325:
                    booster = 1
                elif 725 <= x <= 750 and 310 <= y <= 325:
                    booster = 2
                elif 800 <= x <= 825 and 310 <= y <= 325:
                    booster = 3

                #launch
                if 750 <= x <= 850 and 450 <= y <= 475:
                    launch()

        if stageCount == 0:
            drawMissile(booster, fuselage, warhead) 
        
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()