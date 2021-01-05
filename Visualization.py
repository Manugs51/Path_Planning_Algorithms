import pygame, sys
import pygame.event as EVENTS
import pygame.locals as LOCALS
from enum import Enum


bg_color = (255,255,255)
border_color = (0,0,0)


class Algorithm(Enum):
    HOME = 0
    BUG1 = 1
    BUG2 = 2


class Visualization:

    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont("Comic Sans MS", 30)
        self.window_w = 900
        self.window_h = 900
        self.window = pygame.display.set_mode((self.window_w, self.window_h))
        pygame.display.set_caption("Path planning")
        self.state = Algorithm.HOME


    def home(self):
    
        button_x = 300
        button_width = 300
        button_height = 50
    
        for i in range(1, len(Algorithm)):
            pygame.draw.rect(self.window, border_color, (button_x, i*60, button_width, button_height), 1)
            button_text = self.font.render(Algorithm(i).name, False, border_color)
            self.window.blit(button_text, (button_x,i*60))
        


    def main_loop(self):
        while True:
            for e in EVENTS.get():
                if e.type == LOCALS.QUIT:
                    self.quit()
                
            self.window.fill(bg_color)
        
            if self.state == Algorithm.HOME:
                self.home()
            elif self.state == Algorithm.BUG1:
                self.bug1()

            pygame.display.update()
            


    #Close the screen
    def quit(self):
        pygame.quit()
        sys.exit()

# --------------------------------------------------------------------------

if __name__ == '__main__':
    vis = Visualization()
    vis.main_loop()