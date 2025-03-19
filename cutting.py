from point import Point
from rasterization.line import Line

# cohen region codes
INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000
class Cutting:
    def __init__(self, p1, p2, pmin, pmax):
        if isinstance(p1, Point) and isinstance(p2, Point) and isinstance(pmin, Point) and isinstance(pmax, Point):
            self.p1 = p1
            self.p2 = p2
            self.pmin = pmin
            self.pmax = pmax

    def get_code(p, pmin, pmax):
        code = INSIDE
        if p.x < pmin.x:
            code |= LEFT
        elif p.x > pmax.x:
            code |= RIGHT
        if p.y < pmin.y:
            code |= BOTTOM
        elif p.y > pmax.y:
            code |= TOP
        return code
    
    def bit(position, value):
        return (value >> position) & 1

    def cohen(self):
        done = False
        accept = True
        line = []

        while not done:
            cod1 = self.getCode(self.p1, self.pmin, self.pmax)
            cod2 = self.getCode(self.p2, self.pmin, self.pmax)

            if cod1 == INSIDE and cod2 == INSIDE: # inside
                done = True
                accept = True
            elif cod1 and cod2 != INSIDE: # out
                done = True
            else: # calc
                cod = cod1 if cod1 != 0 else cod2

                if self.bit(0, cod): # left
                    xint = self.pmin.x
                    yint = self.p1.y + (self.p2.y - self.p1.y) * (self.pmin.x - self.p1.x) / (self.p2.x - self.p1.x)
                elif self.bit(1, cod): # right
                    xint = self.pmax.x
                    yint = self.p1.y + (self.p2.y - self.p1.y) * (self.pmax.x - self.p1.x) / (self.p2.x - self.p1.x)
                elif self.bit(2, cod): # bottom
                    yint = self.pmin.y
                    xint = self.p1.x + (self.p2.x - self.p1.x) * (self.pmin.y - self.p1.y) / (self.p2.y - self.p1.y)
                elif self.bit(3, cod): # top
                    yint = self.pmax.y
                    xint = self.p1.x + (self.p2.x - self.p1.x) * (self.pmax.y - self.p1.y) / (self.p2.y - self.p1.y)

                if cod == cod1:
                    self.p1.x, self.p1.y = xint, yint
                else:
                    self.p2.x, self.p2.y = xint, yint
        
        if accept:
            # call dda function to add pixels on array
            line = Line(self.p1, self.p2).dda()
            return line
        
    # STILL HAVE TO ADAPT THE USE OF POINTER OF U1 AND U2!!!!!!!!!!!!!!!!
    def clip_test(p, q, u1, u2):
        result = True

        if p == 0 and q < 0:
            result = False
        elif p < 0:
            r = q/p
            if r > u2:
                result = False
            elif r > u1:
                u1 = r
        elif p > 0:
            r = q/p
            if r < u1:
                result = False
            elif r > u2:
                u2 = r
        return result 

    def liang(self):
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y
        u1 = 0
        u2 = 1

        if self.clip_test(-dx, self.p1.x - self.pmin.x, u1, u2): # left
            if self.clip_test(dx, self.pmax.x - self.p1.x, u1, u2): # right
                if self.clip_test(-dy, self.p1.y - self.pmin.y, u1, u2): # bottom
                    if self.clip_test(dy, self.pmax.y - self.p1.y, u1, u2): # top
                        if u2 < 1:
                            self.p2.x = self.p1.x + dx * u2
                            self.p2.y = self.p1.y + dy * u2
                        if u1 > 0:
                            self.p1.x = self.p1.x + dx * u1
                            self.p1.y = self.p1.y + dy * u1
                        line = Line(self.p1, self.p2).dda()
                        return line