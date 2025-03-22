from point import Point

class Line:
    def __init__(self, p1, p2, color="purple"):
        if isinstance(p1, Point) and isinstance(p2, Point):
            self.p1 = p1
            self.p2 = p2
            self.color = color
        else:
            raise TypeError("p1 and p2 must be Point type")
        
    def __repr__(self):
        return f"Line: P1({self.p1.x},{self.p1.y}), P2({self.p2.x},{self.p2.y}))"
    
    def get_pixels(self):
        return self.dda()

    # returns a Point array
    def dda(self):
        line = []

        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y

        dx = x2 - x1
        dy = y2 - y1

        steps = int(abs(dx)) if abs(dx) > abs(dy) else int(abs(dy))

        x_inc = dx / steps
        y_inc = dy / steps

        x, y = x1, y1
        line.append(Point(x,y)) 

        for _ in range(steps + 1):
            x += x_inc
            y += y_inc
            line.append(Point(x,y))
        return line 
    # returns a Point array
    def bresenham(self):
        line = []

        x1, y1 = int(self.p1.x), int(self.p1.y)
        x2, y2 = int(self.p2.x), int(self.p2.y)

        dx = x2 - x1
        dy = y2 - y1

        if dx >= 0:
            x_inc = 1
        else:
            x_inc = -1
            dx = -dx

        if dy >= 0:
            y_inc = 1
        else:
            y_inc = -1
            dy = -dy

        x, y = x1, y1
        line.append(Point(x,y))

        if dy < dx:
            p = 2 * dy - dx
            const1 = 2 * dy
            const2 = 2 * (dy - dx)

            for _ in range(dx):
                x += x_inc
                if p < 0:
                    p += const1
                else:
                    y += y_inc
                    p += const2
                line.append(Point(x,y))
        else:
            p = 2 * dx - dy
            const1 = 2 * dx
            const2 = 2 * (dx - dy)

            for _ in range(dy):
                y += y_inc
                if p < 0:
                    p += const1
                else:
                    x += x_inc
                    p += const2
                line.append(Point(x,y))
        return line