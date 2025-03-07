# 2D geometric transformations
import math

from point import Point

class Transformations:
    def __init__(self, p):
        if isinstance(p, list) and all(isinstance(item, Point) for item in p):
            self.points = p  # if p is an array
        elif isinstance(p, Point):
            self.points = [p]  # it it's a single point, wrap into an array
        else:
            self.points = []  # if none, create an empty array

    def translate(self, points, dx, dy):
        """Translates a set of points by (dx, dy)."""
        translated_points = []
        for p in points:
            new_point = Point(p.x + dx, p.y + dy)
            translated_points.append(new_point)
        return translated_points

    def rotate(self, points, angle, origin=(0, 0)):
        """Rotates a set of points by 'angle' degrees around the given 'origin'."""
        angle_rad = math.radians(angle)  # Convert angle to radians
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)
        
        rotated_points = []
        ox, oy = origin
        
        for x, y in points:
            # Apply rotation matrix formula
            new_x = ox + cos_angle * (x - ox) - sin_angle * (y - oy)
            new_y = oy + sin_angle * (x - ox) + cos_angle * (y - oy)
            rotated_points.append((new_x, new_y))
        return rotated_points

    def scale(self, points, sx, sy, origin=(0, 0)):
        """Scales a set of points by (sx, sy) relative to the given 'origin'."""
        scaled_points = []
        ox, oy = origin
        
        for x, y in points:
            # Apply scaling transformation
            new_x = ox + sx * (x - ox)
            new_y = oy + sy * (y - oy)
            scaled_points.append((new_x, new_y))
        return scaled_points

    def reflect(self, points, axis):
        """Reflects a set of points over the specified axis ('X', 'Y', or 'XY')."""
        reflected_points = []
        
        for x, y in points:
            if axis == 'X':  # Reflection over the X-axis
                reflected_points.append((x, -y))
            elif axis == 'Y':  # Reflection over the Y-axis
                reflected_points.append((-x, y))
            elif axis == 'XY':  # Reflection over both axes
                reflected_points.append((-x, -y))
            else:
                raise ValueError("Invalid axis! Choose 'X', 'Y', or 'XY'.")
        return reflected_points
