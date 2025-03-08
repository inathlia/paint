# logic for selecting objects in the interface
class Selector:
    def __init__(self, canvas, x1, y1, x2, y2):
        self.canvas = canvas
        self.rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="pink", width=2)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.rect_exists = True
        
    def move(self, dx, dy):
        """Move the rectangle by dx and dy."""
        self.canvas.move(self.rect, dx, dy)
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def update_position(self, x1, y1, x2, y2):
        """Update the position of the rectangle."""
        self.canvas.coords(self.rect, x1, y1, x2, y2)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def get_center(self):
        """Get the center coordinates of the rectangle."""
        return (self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2
