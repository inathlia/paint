# 2D geometric transformations
import math

from point import Point

class Transformations:
    # self.points should always be Point type
    def __init__(self, p):
        if isinstance(p, list) and all(isinstance(point, Point) for point in p):
            self.points = p
        else:
            raise TypeError("Value must be a list of Point objects")

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
        
        for p in points:
            # Apply rotation matrix formula
            x = p.x
            y = p.y
            new_x = ox + cos_angle * (x - ox) - sin_angle * (y - oy)
            new_y = oy + sin_angle * (x - ox) + cos_angle * (y - oy)
            rotated_points.append(Point(new_x, new_y))
        return rotated_points

    def scale(self, points, sx, sy, origin=(0, 0)):
        """Scales a set of points by (sx, sy) relative to the given 'origin'."""
        scaled_points = []
        ox, oy = origin
        
        for p in points:
            # Apply scaling transformation
            x = p.x
            y = p.y
            new_x = ox + sx * (x - ox)
            new_y = oy + sy * (y - oy)
            scaled_points.append(Point(new_x, new_y))
        return scaled_points

    def reflect(self, points, axis, center):
        """Reflects a set of points over the specified axis ('X', 'Y', or 'XY') relative to the given center."""
        reflected_points = []
        
        # Get the center of the selector (used as the reflection center)
        cx, cy = center
        
        for p in points:
            x = p.x
            y = p.y
            
            if axis == 'X':  # Reflection over the X-axis (relative to the center)
                reflected_points.append(Point(x, 2*cy - y))
            elif axis == 'Y':  # Reflection over the Y-axis (relative to the center)
                reflected_points.append(Point(2*cx - x, y))
            elif axis == 'XY':  # Reflection over both axes (relative to the center)
                reflected_points.append(Point(2*cx - x, 2*cy - y))
            else:
                raise ValueError("Invalid axis! Choose 'X', 'Y', or 'XY'.")
        
        return reflected_points

