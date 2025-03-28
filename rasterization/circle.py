import math

from point import Point

class Circle:
    def __init__(self, p, r, color):
        if isinstance(p, Point) and isinstance(r, Point):
            self.p = p
            self.r_point = r
            self.r = math.sqrt(abs(p.x - r.x)**2 + abs(p.y - r.y)**2)
            self.color = color
            self.circ = []
        else:
            raise TypeError("p and r must be Point type")
        
    def __repr__(self):
        return f"Circle: P({self.p.x},{self.p.y}), R({self.r}), Color({self.color}))"

    def get_pixels(self):
        return self.bresenham()

    def bresenham(self):
        x, y = 0, self.r
        xc, yc = self.p.x, self.p.y
        p = 3 - 2 * self.r
        
        self.plot_simetric(x, y, xc, yc)
        
        while x < y:
            if p < 0:
                p += 4 * x + 6
            else:
                p += 4 * (x - y) + 10
                y-= 1
            x += 1
            self.plot_simetric(x, y, xc, yc)
        
        return self.circ
        
    def plot_simetric(self, x, y, xc, yc):
        points = [
            (xc + x, yc + y), (xc - x, yc + y),
            (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x),
            (xc + y, yc - x), (xc - y, yc - x)
        ]
        for px, py in points:
            self.circ.append(Point(px, py))