from point import Point
from rasterization.line import Line

# cohen region codes
INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000
class Cutting:
    def __init__(self, objects, pmin, pmax):
        if isinstance(pmin, Point) and isinstance(pmax, Point):
            self.objects = objects
            self.pmin = pmin
            self.pmax = pmax
        else:
            raise TypeError("pmin and pmax must be Point type")

    # gets an array of objects and return an array of cutted objects
    def cohen(self):
        new_objects = []
        for o in self.objects:
            if isinstance(o, Line):
                new_line = self.run_cohen(o.p1, o.p2)
                new_objects.append(new_line)
            else:
                # nothing happens
                new_objects.append(o)
        return new_objects

    # gets an array of objects and return an array of cutted objects
    def liang(self):
        new_objects = []
        for o in self.objects:
            if isinstance(o, Line):
                new_line = self.run_liang(o.p1, o.p2)
                new_objects.append(new_line)
            else:
                # nothing happens
                new_objects.append(o)
        return new_objects

    # Cohen --------------------------------------------------------------------------------------------------
    def get_code(self, p):
        code = INSIDE
        if p.x < self.pmin.x:
            code |= LEFT
        elif p.x > self.pmax.x:
            code |= RIGHT
        if p.y < self.pmin.y:
            code |= BOTTOM
        elif p.y > self.pmax.y:
            code |= TOP
        return code
    
    def bit(self, position, value):
        return (value >> position) & 1

    def run_cohen(self, p1, p2):
        done = False
        accept = False
        line = []

        while not done:
            cod1 = self.get_code(p1)
            cod2 = self.get_code(p2)

            if cod1 == INSIDE and cod2 == INSIDE: # inside
                done = True
                accept = True
            elif cod1 & cod2 != INSIDE: # out
                done = True
            else: # calc
                cod = cod1 if cod1 != 0 else cod2

                if self.bit(0, cod): # left
                    xint = self.pmin.x
                    yint = p1.y + (p2.y - p1.y) * (self.pmin.x - p1.x) / (p2.x - p1.x)
                elif self.bit(1, cod): # right
                    xint = self.pmax.x
                    yint = p1.y + (p2.y - p1.y) * (self.pmax.x - p1.x) / (p2.x - p1.x)
                elif self.bit(2, cod): # bottom
                    yint = self.pmin.y
                    xint = p1.x + (p2.x - p1.x) * (self.pmin.y - p1.y) / (p2.y - p1.y)
                elif self.bit(3, cod): # top
                    yint = self.pmax.y
                    xint = p1.x + (p2.x - p1.x) * (self.pmax.y - p1.y) / (p2.y - p1.y)

                if cod == cod1:
                    p1.x, p1.y = xint, yint
                else:
                    p2.x, p2.y = xint, yint
        
        if accept:
            # return line object
            line = Line(p1, p2)
            return line
        
    # Liang --------------------------------------------------------------------------------------------------
    def clip_test(self, p, q):
        result = True

        if p < 0: # out-in
            r = q/p
            if r > self.u2:
                result = False
            elif r > self.u1:
                self.u1 = r
        elif p > 0: # in-out
            r = q/p
            if r < self.u1:
                result = False
            elif r < self.u2:
                self.u2 = r
        return result

    def run_liang(self, p1, p2):
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        self.u1 = 0
        self.u2 = 1

        if self.clip_test(-dx, p1.x - self.pmin.x): # left
            if self.clip_test(dx, self.pmax.x - p1.x): # right
                if self.clip_test(-dy, p1.y - self.pmin.y): # bottom
                    if self.clip_test(dy, self.pmax.y - p1.y): # top
                        if self.u2 < 1:
                            p2.x = p1.x + dx * self.u2
                            p2.y = p1.y + dy * self.u2
                        if self.u1 > 0:
                            p1.x = p1.x + dx * self.u1
                            p1.y = p1.y + dy * self.u1
                        # return line object
                        line = Line(p1, p2)
                        return line