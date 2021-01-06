import math

class PathPlanning:

    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        self.current_pos = start
    
    
    def finished(self):
        return self.current_pos == self.goal
    
    
    def next_step(self):
        # Placeholder
        return self.current_pos
    
    
    def distance(self, p0, p1):
        return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
    
    
    def neighbors(self, p):
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
    
    def __init__(self, start, goal):
        super().__init__(start, goal)
    
    
    def next_step(self):
        self.current_pos = self.closest_neighbor(self.current_pos)
        return self.current_pos