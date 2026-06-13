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
        self.bullets = pygame.sprite.Group

    def move(self,keys):
        if keys[self.controls["left"]]:
            self.rect.x -= playerspeed
        if keys[self.controls["right"]]:
            self.rect.x += playerspeed
        if keys[self.controls["down"]]:
            self.rect.y -= playerspeed
        if keys[self.controls["up"]]:
            self.rect.y += playerspeed
        
        #screen boundaries
        self.rect.top= max(0,self.rect.top)
        self.rect.bottom= min(height,self.rect.bottom)
        if self.side == "left":
            self.rect.left= max(0,self.rect.left)
            self.rect.right= min(divider.left,self.rect.right)
        else:
            self.rect.left= max(divider.right, self.rect.left)
            self.rect.right= min(width, self.rect.right)

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
    screen.blit(bg_img,(0,0))
    #display divide
    pygame.draw.rect(screen,"black", divider)
    players.draw(screen)
    pygame.display.update()



def main():
    isrunning = True
    while isrunning: 
        clock.tick(fps)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isrunning = False
                pygame.quit()
                exit(0)

        draw()

main()

        










