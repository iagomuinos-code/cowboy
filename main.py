import pygame
pygame.init()


width=900
height=500
screen = pygame.display.set_mode((width,height))

bg_img = pygame.image.load("images\desertbgnew.jpg")
# cowboyright_img = pygame.image.load("images\cowboyright.png")
# cowboyleft_img

#game variables
plyersize = (40,60)
playerspeed= 3
maxbullet = 2
bulletspeed = 8
bulletsize= (10,4)
hp = 100
isrunning = True

clock = pygame.time.Clock()
fps = 60

#slecting fonts
hpfont = pygame.font.SysFont("helvetica",20)
winnerfont = pygame.font.SysFont("timesnewroman",80)

divider = pygame.Rect(width//2-5,0,10,height)


#creating characters
class Player(pygame.sprite.Sprite):
    #creating properties/attributes
    def __init__(self,x,y,image_path,controls,side):
        #initialising the init function of parent class
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image,(40,60))
        #adding collider/hitbox around image
        self.rect = self.image.get_rect(topleft=(x,y)) # topleft?
        self.controls = controls
        self.side = side
        self.hp = hp
        self.bullets = pygame.sprite.Group()

    def move(self,keys):
        if keys[self.controls["left"]]:
            self.rect.x -= playerspeed
        if keys[self.controls["right"]]:
            self.rect.x += playerspeed
        if keys[self.controls["down"]]:
            self.rect.y += playerspeed
        if keys[self.controls["up"]]:
            self.rect.y -= playerspeed
        
        #screen boundaries
        self.rect.top= max(0,self.rect.top)
        self.rect.bottom= min(height,self.rect.bottom)
        if self.side == "left":
            self.rect.left= max(0,self.rect.left)
            self.rect.right= min(divider.left,self.rect.right)
        else:
            self.rect.left= max(divider.right, self.rect.left)
            self.rect.right= min(width, self.rect.right)

    def shoot(self):
        if len(self.bullets) >= maxbullet:
            return
        if self.side == "left":
            bullet = Bullet(self.rect.right,self.rect.centery,1)

        else :
            bullet = Bullet(self.rect.left, self.rect.centery, -1)

        #adding bullet to bullet group
        self.bullets.add(bullet)

    def update(self):
        self.bullets.update()
        
        



class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction ):
        super().__init__()
        self.image = pygame.Surface((6,4))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.direction = direction

    def update(self):
        self.rect.x += bulletspeed * self.direction
        if self.rect.right < 0 or self.rect.left > width :
            self.kill()


#creating player objects
plyrone = Player(
    100,
    200,
    "images\cowboyleft.png",
    {"left":pygame.K_a,
      "down":pygame.K_s, 
      "up":pygame.K_w, 
      "right":pygame.K_d},
    "left"
    )

plyrtwo = Player(
    600,
    200,
    "images\cowboyright.png",
    {"left":pygame.K_LEFT,
      "down":pygame.K_DOWN, 
      "up":pygame.K_UP, 
      "right":pygame.K_RIGHT},
    "right"
    )

#creating players' group
players = pygame.sprite.Group()
players.add(plyrone, plyrtwo)





def draw():
    screen.blit(bg_img,(0,0)) #blit means displaying bg
    #display divide
    pygame.draw.rect(screen,"black", divider)
    players.draw(screen) # drawing both playes(group) onto screen
    #display bullets for both the players 
    plyrone.bullets.draw(screen)
    plyrtwo.bullets.draw(screen)

    #displaying health text
    lefttext = hpfont.render(f"Health: {plyrone.hp}",True,"black")
    screen.blit(lefttext, (50,30))
    righttext = hpfont.render(f"Health: {plyrtwo.hp}",True,"black")
    screen.blit(righttext, (width/2 + 50,30))

    pygame.display.update()


def check_shot():
    for bullet in plyrone.bullets:
        if bullet.rect.colliderect(plyrtwo.rect):
            plyrtwo.hp -= 15
            bullet.kill()
    for bullet in plyrtwo.bullets:
        if bullet.rect.colliderect(plyrone.rect):
            plyrone.hp -= 15
            bullet.kill()

def show_win(x):
    winnertext = winnerfont.render(x,True,"black")
    screen.blit(winnertext, (width//2-winnertext.get_width()//2,height//2-winnertext.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)







def main():
    isrunning = True
    while isrunning: 
        clock.tick(fps)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isrunning = False
                pygame.quit()
                exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    plyrone.shoot()
                if event.key == pygame.K_RSHIFT:
                    plyrtwo.shoot()
        #getting all the keys that are pressed 
        keys = pygame.key.get_pressed()

        plyrone.move(keys)
        plyrtwo.move(keys)

        #updating bullet groups for players
        players.update()

        check_shot()
        #ending condition is checking the health of both the players 
        if plyrone.hp <= 0 :
            show_win("Player2 wins")
            break
        if plyrtwo.hp <= 0:
            show_win("Player1 wins")
            break

        
    

        draw()

main()

        










