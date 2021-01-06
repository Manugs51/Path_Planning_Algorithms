import math
from bresenham import bresenham
from enum import Enum

class Direction(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3

class State(Enum):
    STRAIGHT_LINE = 0
    SURROUND = 1
    BEST_SURROUNDED = 2


class PathPlanning:

    def __init__(self, start, goal, map):
        self.start = start
        self.goal = goal
        self.current_pos = start
        self.map = map
    
    
    def finished(self):
        return self.current_pos == self.goal
    
    
    def next_step(self):
        # Placeholder
        return self.current_pos
    
    
    def distance(self, p0, p1):
        return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
    
    
    def neighbors(self, p):
        return [(p[0]-1, p[1]), (p[0]+1, p[1]), (p[0], p[1]-1), (p[0], p[1]+1)]
    
    
    def corner_neighbors(self, p):
        return [(p[0]-1, p[1]-1), (p[0]-1, p[1]+1), (p[0]+1, p[1]-1), (p[0]+1, p[1]+1)]
    
    
    def closest_neighbor(self, p):
        min_dist = math.inf
        closest_neighbor = None
        for n in self.neighbors(p):
            if self.distance(n, self.goal) < min_dist:
                min_dist = self.distance(n, self.goal)
                closest_neighbor = n
        return closest_neighbor


class Bug1(PathPlanning):
    
    def __init__(self, start, goal, map):
        super().__init__(start, goal, map)
        self.line = list(bresenham(start[0], start[1], goal[0], goal[1]))
        self.last_wall = Direction.RIGHT
        self.current_state = State.STRAIGHT_LINE
        self.hit_point = start
        self.times_hit = 4
        self.surroundings = {}
    
    
    def next_step(self):
        if self.current_state == State.STRAIGHT_LINE:
            if self.map[self.line[0][1]][self.line[0][0]] == 255:
                self.current_pos = self.line[0]
                self.line.pop(0)
            else:
                self.current_state = State.SURROUND
                if self.map[self.current_pos[1]][self.current_pos[0] + 1] == 0:
                    self.last_wall = Direction.RIGHT
                elif self.map[self.current_pos[1]][self.current_pos[0] - 1] == 0:
                    self.last_wall = Direction.LEFT
                elif self.map[self.current_pos[1] + 1][self.current_pos[0]] == 0:
                    self.last_wall = Direction.DOWN
                elif self.map[self.current_pos[1] - 1][self.current_pos[0]] == 0:
                    self.last_wall = Direction.UP
                else:
                    # It touched in a corner
                    if self.map[self.current_pos[1] + 1][self.current_pos[0] + 1] == 0:
                        self.current_pos = (self.current_pos[0] + 1, self.current_pos[1])
                        self.last_wall = Direction.DOWN
                    elif self.map[self.current_pos[1] + 1][self.current_pos[0] - 1] == 0:
                        self.current_pos = (self.current_pos[0], self.current_pos[1] + 1)
                        self.last_wall = Direction.LEFT
                    elif self.map[self.current_pos[1] - 1][self.current_pos[0] - 1] == 0:
                        self.current_pos = (self.current_pos[0] - 1, self.current_pos[1])
                        self.last_wall = Direction.UP
                    elif self.map[self.current_pos[1] - 1][self.current_pos[0] + 1] == 0:
                        self.current_pos = (self.current_pos[0], self.current_pos[1] - 1)
                        self.last_wall = Direction.RIGHT
                    else:
                        # This never happens
                        pass
                self.hit_point = self.current_pos
                # Worst case scenario: has to turn 3 times before being able to make first move
                self.times_hit = 4
        
        elif self.current_state == State.SURROUND:
            x, y = self.current_pos
            if self.last_wall == Direction.RIGHT:
                if self.map[y][x + 1] == 255:
                    self.current_pos = (x + 1, y)
                    self.last_wall = Direction.DOWN
                else:
                    self.last_wall = Direction.UP
            elif self.last_wall == Direction.UP:
                if self.map[y - 1][x] == 255:
                    self.current_pos = (x, y - 1)
                    self.last_wall = Direction.RIGHT
                else:
                    self.last_wall = Direction.LEFT
            elif self.last_wall == Direction.LEFT:
                if self.map[y][x - 1] == 255:
                    self.current_pos = (x - 1, y)
                    self.last_wall = Direction.UP
                else:
                    self.last_wall = Direction.DOWN
            elif self.last_wall == Direction.DOWN:
                if self.map[y + 1][x] == 255:
                    self.current_pos = (x, y + 1)
                    self.last_wall = Direction.LEFT
                else:
                    self.last_wall = Direction.RIGHT
            self.surroundings[self.current_pos] = self.distance(self.current_pos, self.goal)
            
            if self.current_pos == self.hit_point:
                self.times_hit -= 1
            
            if self.times_hit <= 0:
                self.current_state = State.BEST_SURROUNDED
        
        elif self.current_state == State.BEST_SURROUNDED:
            self.current_pos = min(self.surroundings, key=self.surroundings.get)
            self.current_state = State.STRAIGHT_LINE
            self.line = list(bresenham(self.current_pos[0], self.current_pos[1], self.goal[0], self.goal[1]))
            
        
        return self.current_pos


class Bug2(PathPlanning):
    
    def __init__(self, start, goal, map):
        super().__init__(start, goal, map)
        self.line = list(bresenham(start[0], start[1], goal[0], goal[1]))
        self.last_wall = Direction.RIGHT
        self.current_state = State.STRAIGHT_LINE
        self.left_hit = False
    
    
    def next_step(self):
        if self.current_state == State.STRAIGHT_LINE:
            if self.map[self.line[0][1]][self.line[0][0]] == 255:
                self.current_pos = self.line[0]
                self.line.pop(0)
            else:
                self.current_state = State.SURROUND
                if self.map[self.current_pos[1]][self.current_pos[0] + 1] == 0:
                    self.last_wall = Direction.RIGHT
                elif self.map[self.current_pos[1]][self.current_pos[0] - 1] == 0:
                    self.last_wall = Direction.LEFT
                elif self.map[self.current_pos[1] + 1][self.current_pos[0]] == 0:
                    self.last_wall = Direction.DOWN
                elif self.map[self.current_pos[1] - 1][self.current_pos[0]] == 0:
                    self.last_wall = Direction.UP
                else:
                    # It touched in a corner
                    if self.map[self.current_pos[1] + 1][self.current_pos[0] + 1] == 0:
                        self.current_pos = (self.current_pos[0] + 1, self.current_pos[1])
                        self.last_wall = Direction.DOWN
                    elif self.map[self.current_pos[1] + 1][self.current_pos[0] - 1] == 0:
                        self.current_pos = (self.current_pos[0], self.current_pos[1] + 1)
                        self.last_wall = Direction.LEFT
                    elif self.map[self.current_pos[1] - 1][self.current_pos[0] - 1] == 0:
                        self.current_pos = (self.current_pos[0] - 1, self.current_pos[1])
                        self.last_wall = Direction.UP
                    elif self.map[self.current_pos[1] - 1][self.current_pos[0] + 1] == 0:
                        self.current_pos = (self.current_pos[0], self.current_pos[1] - 1)
                        self.last_wall = Direction.RIGHT
                    else:
                        # This never happens
                        pass
        
        elif self.current_state == State.SURROUND:
            x, y = self.current_pos
            if self.last_wall == Direction.RIGHT:
                if self.map[y][x + 1] == 255:
                    self.current_pos = (x + 1, y)
                    self.last_wall = Direction.DOWN
                    self.left_hit = True
                else:
                    self.last_wall = Direction.UP
            elif self.last_wall == Direction.UP:
                if self.map[y - 1][x] == 255:
                    self.current_pos = (x, y - 1)
                    self.last_wall = Direction.RIGHT
                    self.left_hit = True
                else:
                    self.last_wall = Direction.LEFT
            elif self.last_wall == Direction.LEFT:
                if self.map[y][x - 1] == 255:
                    self.current_pos = (x - 1, y)
                    self.last_wall = Direction.UP
                    self.left_hit = True
                else:
                    self.last_wall = Direction.DOWN
            elif self.last_wall == Direction.DOWN:
                if self.map[y + 1][x] == 255:
                    self.current_pos = (x, y + 1)
                    self.last_wall = Direction.LEFT
                    self.left_hit = True
                else:
                    self.last_wall = Direction.RIGHT
            
            if (self.current_pos in self.line) and self.left_hit:
                print('x')
                while self.line[0] != self.current_pos:
                    self.line.pop(0)
                self.current_state = State.STRAIGHT_LINE
            else:
                print(self.left_hit)
        
        return self.current_pos
