
import pygame
import math
###
# Just a class to bunch up all the camera variables
class Camera:
    def __init__(self):
        self.x = 300
        self.y = 300
        self.z = 0
        self.angle = 0, 0
        self.anglex = self.angle[0]
        self.angley = self.angle[1]
        self.fieldofview = 60
        self.pos = (self.x, self.y, self.z)
    def refreshpos(self):
        self.pos = (self.x, self.y, self.z)

# Cube class for 3D objects
class Cuboid:
    def __init__(self, topfrontleft, width, height, depth):
        # Create a bunch of useful variables
        self.width = width
        self.height = height
        self.depth = depth
        self.x = topfrontleft[0]
        self.y = topfrontleft[1]
        self.z = topfrontleft[2]

        self.topfrontleft = topfrontleft
        self.topfrontright = (self.topfrontleft[0]+self.width, self.topfrontleft[1], self.topfrontleft[2])
        self.topbackleft = (self.topfrontleft[0], self.topfrontleft[1], self.topfrontleft[2]+self.depth)
        self.topbackright = (self.topfrontleft[0]+self.width, self.topfrontleft[1], self.topfrontleft[2]+self.depth)
        self.bottomfrontleft = (self.topfrontleft[0], self.topfrontleft[1]+self.height, self.topfrontleft[2])
        self.bottomfrontright = (self.topfrontleft[0]+self.width, self.topfrontleft[1]+self.height, self.topfrontleft[2])
        self.bottombackleft = (self.topfrontleft[0], self.topfrontleft[1]+self.height, self.topfrontleft[2]+self.depth)
        self.bottombackright = (self.topfrontleft[0]+self.width, self.topfrontleft[1]+self.height, self.topfrontleft[2]+self.depth)

        self.points = [self.topfrontleft, self.topfrontright, self.bottomfrontleft, self.bottomfrontright,
                    self.topbackleft, self.topbackright, self.bottombackleft, self.bottombackright]
    def refreshpoints(self):
        self.topfrontleft = (self.x, self.y, self.z)
        self.topfrontright = (self.topfrontleft[0]+self.width, self.topfrontleft[1], self.topfrontleft[2])
        self.topbackleft = (self.topfrontleft[0], self.topfrontleft[1], self.topfrontleft[2]+self.depth)
        self.topbackright = (self.topfrontleft[0]+self.width, self.topfrontleft[1], self.topfrontleft[2]+self.depth)
        self.bottomfrontleft = (self.topfrontleft[0], self.topfrontleft[1]+self.height, self.topfrontleft[2])
        self.bottomfrontright = (self.topfrontleft[0]+self.width, self.topfrontleft[1]+self.height, self.topfrontleft[2])
        self.bottombackleft = (self.topfrontleft[0], self.topfrontleft[1]+self.height, self.topfrontleft[2]+self.depth)
        self.bottombackright = (self.topfrontleft[0]+self.width, self.topfrontleft[1]+self.height, self.topfrontleft[2]+self.depth)

        self.points = [self.topfrontleft, self.topfrontright, self.bottomfrontleft, self.bottomfrontright,
                    self.topbackleft, self.topbackright, self.bottombackleft, self.bottombackright]
    # Turn a 3D set of points into a 2D set to display.
    def render(self, cam: Camera, H: int, W: int):
        #This is the hard bit
        Points2D = []
        for point in self.points:
            #X-angle
            opposite = point[0]-cam.x
            ajacent = point[2]-cam.z
            if ajacent > 0:
                #If it is in front of the camera
                try:
                    anglex = math.degrees(math.atan(opposite/ajacent))
                    anglex += cam.anglex
                except:
                    anglex = 90
                anglex += 90
            elif point[0]-cam.x > 0:
                #Send it into the ether
                anglex = 180
            elif point[0]-cam.x < 0:
                anglex = 0
            else:
                anglex = 90
            #Y-angle

            opposite = point[1]-cam.y
            ajacent = point[2]-cam.z

            if ajacent > 0:
                try:
                    angley = math.degrees(math.atan(opposite/ajacent))
                    angley += cam.angley
                except:
                    angley = 90
                angley += 90
            elif point[1]-cam.y > 0:
                #Send it into the ether
                angley = 180
            elif point[1]-cam.y < 0:
                angley = 0
            else:
                angley = 90
            
            fullviewW = W * 180/cam.fieldofview
            fullviewH = H * 180/cam.fieldofview
            xpos = (anglex/180 * fullviewW) - ((fullviewW-W)/2)
            ypos = (angley/180 * fullviewH) - ((fullviewH-H)/2)
            Points2D.append((xpos, ypos))

        return Points2D
    
    # Draw the shape onto the screen, utilizing the render function
    def draw(self, win: pygame.surface.Surface, cam: Camera, W: int, H: int, fill: tuple, outline=(0, 0, 0)):
        shape = self.render(cam, W, H)
        def drawy():
            if self.y+(self.height/2) > cam.y:
                pygame.draw.polygon(win, fill, (shape[0], shape[1], shape[5], shape[4]))
                pygame.draw.polygon(win, outline, (shape[0], shape[1], shape[5], shape[4]), 2)
            else:
                pygame.draw.polygon(win, fill, (shape[2], shape[3], shape[7], shape[6]))
                pygame.draw.polygon(win, outline, (shape[2], shape[3], shape[7], shape[6]), 2)
            
        def drawx():
            if self.x+(self.width/2) > cam.x:
                pygame.draw.polygon(win, fill, (shape[0], shape[2], shape[6], shape[4]))
                pygame.draw.polygon(win, outline, (shape[0], shape[2], shape[6], shape[4]), 2)
            
            else:
                pygame.draw.polygon(win, fill, (shape[1], shape[3], shape[7], shape[5]))
                pygame.draw.polygon(win, outline, (shape[1], shape[3], shape[7], shape[5]), 2)
        if self.y < cam.y < self.y+self.height:
            drawy()
            drawx()
        elif self.x < cam.x < self.x+self.width:
            drawx()
            drawy()
        else:
            drawx()
            drawy()
        pygame.draw.polygon(win, fill, (shape[0], shape[1], shape[3], shape[2]))
        pygame.draw.polygon(win, outline, (shape[0], shape[1], shape[3], shape[2]), 2)
    
    def get_dist(self, cam):
        avrg = 0
        for point in self.points:
            avrg += math.dist(point, cam.pos)
        avrg /= len(self.points)
        return avrg

#### END OF LIBRARY CODE
#### START OF TEST CODE
# Main loop
def main():
    Done = False
    W, H = 880, 880
    clock = pygame.time.Clock()
    FPS = 60
    win = pygame.display.set_mode((W, H))
    cam = Camera()
    player = Cuboid((200, 100, 1000), 200, 200, 200)
    shapes = [Cuboid((200, 300, -200), 1000, 1, 200)]
    for i in range(20):
        shapes.append(Cuboid((-200, 300, (i*200)+200), 1000, 1, 200))
    def sort(var):
        return var.z
    shapes.sort(reverse=True, key=sort)
    while not Done:
        #Regulate Framerate
        clock.tick(FPS)
        #Process inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Done = True
            elif event.type == pygame.KEYDOWN:
                pass
        event = pygame.key.get_pressed()
        if event[pygame.K_LEFT]:
            cam.x -= 8
        if event[pygame.K_RIGHT]:
            cam.x += 8
        if event[pygame.K_UP]:
            cam.z += 8
            player.z += 8
        if event[pygame.K_DOWN]:
            cam.z -= 8
            player.z -= 8
        if event[pygame.K_SPACE]:
            cam.y -= 8
        if event[pygame.K_LSHIFT]:
            cam.y += 8
        if event[pygame.K_a]:
            cam.anglex += 1
        if event[pygame.K_d]:
            cam.anglex -= 1
        if event[pygame.K_w]:
            cam.angley += 1
        if event[pygame.K_s]:
            cam.angley -= 1
        cam.refreshpos()
        if shapes[len(shapes)-1].z - cam.z < 4000:
            shapes.append(Cuboid((-200, 800, shapes[len(shapes)-1].z+200), 1000, 1, 200))
        #Render shape
        win.fill((125, 125, 200))
        for shape in shapes:
            if shape.y > 300:
                shape.y -= 6
                shape.draw(win, cam, H, W, (130, 20, 20), (100, 20, 20))
            shape.refreshpoints()
        
        for shape in shapes:
            if shape.y <= 300:
                shape.refreshpoints()
                shape.draw(win, cam, H, W, (130, 20, 20), (100, 20, 20))
        
        player.refreshpoints()
        player.draw(win, cam, W, H, (255, 255, 255))
        #Edit shape
        #Draw
        pygame.display.flip()

        

# Run the program
if __name__ == '__main__':
    main()
    print('Done.')