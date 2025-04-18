import math

class Selector:
    def __init__(self, canvas, x1, y1, x2, y2):
        self.outline = "hotpink"
        self.canvas = canvas
        self.rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline=self.outline, width=2)
        # x1 and y1 are min values
        # x2 and y2 are max values
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.angle = 0

    def get_center(self):
        return (self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2
    
    def get_angle(self):
        return self.angle

    def set_angle(self, angle):
        self.angle = angle

    # function to move the selector around the canvas
    def move(self, dx, dy):
        self.canvas.move(self.rect, dx, dy)
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def update_position(self, x1, y1, x2, y2):
        self.canvas.coords(self.rect, x1, y1, x2, y2)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    # rotate the selector by angle in degrees
    def rotate(self, angle):
        self.angle += angle  # update total rotation
        cx, cy = self.get_center()
        
        # get four corners of rectangle
        corners = [
            (self.x1, self.y1),
            (self.x2, self.y1),
            (self.x2, self.y2),
            (self.x1, self.y2),
        ]

        # rotate all corners
        rotated_corners = self.rotate_points(corners, angle, (cx, cy))

        self.canvas.delete(self.rect)
        self.rect = self.canvas.create_polygon(rotated_corners, outline=self.outline, fill="", width=2)

    # aux function to rotate points around a origin
    def rotate_points(self, points, angle, origin):
        angle_rad = math.radians(angle)
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)

        ox, oy = origin
        rotated = []
        for x, y in points:
            new_x = ox + cos_angle * (x - ox) - sin_angle * (y - oy)
            new_y = oy + sin_angle * (x - ox) + cos_angle * (y - oy)
            rotated.append((new_x, new_y))
        return rotated
