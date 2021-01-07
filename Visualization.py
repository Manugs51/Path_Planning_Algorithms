import pygame, sys, time
import pygame.event as EVENTS
import pygame.locals as LOCALS
from enum import Enum
import cv2
import PathPlanning


bg_color = (255,255,255)
border_color = (255,0,0)
start_color = (128,128,0)
goal_color = (0,255,0)
line_color = (0,0,255)


class Algorithm(Enum):
    HOME = 0
    BUG1 = 1
    BUG2 = 2
    VALUE_ITERATION = 3


class Visualization:

    def __init__(self, map):
        pygame.init()
        self.font = pygame.font.SysFont("Comic Sans MS", 30)
        self.window_w = 900
        self.window_h = 900
        self.window = pygame.display.set_mode((self.window_w, self.window_h))
        pygame.display.set_caption("Path planning")
        self.state = Algorithm.HOME
        self.start = (0,0)
        self.goal = (0,0)
        self.map = []
        for i in range(self.window_h):
            row = []
            for j in range(self.window_w):
                # Center map
                if i >= ((self.window_h - len(map))//2) and i < ((self.window_h - len(map))//2 + len(map)) and \
                j >= ((self.window_w - len(map[0]))//2) and j < ((self.window_w - len(map[0]))//2 + len(map[0])):
                    row.append(map[i - ((self.window_h - len(map))//2)][j - ((self.window_w - len(map[0]))//2)])
                else:
                    row.append(255)
            self.map.append(row)


    def __display_buttons(self, button_x, button_width, button_height, button_separation, buttons):
        for i in range(1, len(Algorithm)):
            buttons.append(pygame.draw.rect(self.window, border_color, (button_x, i*button_separation, button_width, button_height), 1))
            button_text = self.font.render(Algorithm(i).name, False, border_color)
            self.window.blit(button_text, (button_x,i*button_separation))


    def __push_buttons(self, buttons, button_separation):
        for e in EVENTS.get():
            if e.type == LOCALS.QUIT:
                self.quit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.collidepoint(e.pos):
                        self.state = Algorithm(button.y/button_separation)


    def __home(self):
        button_x = 300
        button_width = 300
        button_height = 50
        button_separation = 60
        buttons = []
        
        self.__display_buttons(button_x, button_width, button_height, button_separation, buttons)
        
        self.__push_buttons(buttons, button_separation)


    def __paint_map(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == 0:
                    self.window.set_at((j, i), border_color)
    
        pygame.display.update()
    
    
    def __choose_start_point(self):
        start_selected = False
        while not start_selected:
            for e in EVENTS.get():
                if e.type == LOCALS.QUIT:
                    self.quit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self.start = e.pos
                    start_selected = True
                    pygame.draw.circle(self.window, start_color, self.start, 5, 0)
                    pygame.display.update()
    
    
    def __choose_goal(self):
        goal_selected = False
        while not goal_selected:
            for e in EVENTS.get():
                if e.type == LOCALS.QUIT:
                    self.quit()
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self.goal = e.pos
                    goal_selected = True
                    pygame.draw.circle(self.window, goal_color, self.goal, 5, 0)
                    pygame.display.update()
    
    
    def __paint_distances(self, map):
        for elem in map.keys():
            intensity = map[elem]
            self.window.set_at(elem, (intensity, intensity, intensity))
        pygame.draw.circle(self.window, start_color, self.start, 5, 0)
        pygame.draw.circle(self.window, goal_color, self.goal, 5, 0)
        pygame.display.update()

    
    def __execute_algorithm(self):
        if self.state == Algorithm.BUG1:
            algorithm = PathPlanning.Bug1(self.start, self.goal, self.map)
        if self.state == Algorithm.BUG2:
            algorithm = PathPlanning.Bug2(self.start, self.goal, self.map)
        if self.state == Algorithm.VALUE_ITERATION:
            algorithm = PathPlanning.ValueIteration(self.start, self.goal, self.map)
            self.__paint_distances(algorithm.distance_map())
        current_pos = self.start
        while current_pos != self.goal:
            current_pos = algorithm.next_step()
            self.window.set_at((current_pos[0], current_pos[1]), line_color)
            pygame.display.update()
        pygame.image.save(self.window, "result.png")
        time.sleep(4)


    def main_loop(self):
        while True:                
            self.window.fill(bg_color)
        
            if self.state == Algorithm.HOME:
                self.__home()
            else:
                self.__paint_map()
                self.__choose_start_point()
                self.__choose_goal()
                self.__execute_algorithm()

            pygame.display.update()


    #Close the screen
    def quit(self):
        pygame.quit()
        sys.exit()

# --------------------------------------------------------------------------

if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print('A file name for the map is needed as an argument')
        sys.exit()
    
    image = cv2.imread(sys.argv[1])
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (thresh, b_w_image) = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
    
    #cv2.imshow('Black and white image', b_w_image)
    vis = Visualization(b_w_image)
    vis.main_loop()
    