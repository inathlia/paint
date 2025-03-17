import tkinter as tk
from tkinter import ttk, simpledialog
import math

from point import Point
from transformations import Transformations
from selection import Selector

class GraphicsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("2D Graphics Application")

        # Create a frame for buttons
        self.toolbar = tk.Frame(root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Create buttons
        self.add_buttons()

        # Create a canvas for drawing
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Store points
        self.points = []

        # Store selected points inside the rectangular area
        self.selected_points = []

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.handle_button_1)
        self.canvas.bind("<B1-Motion>", self.handle_b1_motion)
        self.canvas.bind("<ButtonRelease-1>", self.handle_buttonrelease_1)
        self.canvas.bind("<Shift-Button-1>", self.handle_shift_b1)
        self.canvas.bind("<Button-3>", self.handle_button_3)
        self.canvas.bind("<B3-Motion>", self.handle_b3_motion)
        self.canvas.bind("<ButtonRelease-3>", self.handle_buttonrelease_3)

        # Initialize selector
        self.selector = None
        self.selector_exits = False
        self.is_rotating = False


    # Handle mouse events ---------------------------------------------------------------------------------------------------------
    def handle_button_1(self, event):
        if not self.selector_exits:  # Create a new point if no selector exists
            self.add_point(event)
        else:
            self.start_drag_selector(event)

    def handle_b1_motion(self, event):
        if self.selector and not self.is_rotating:
            self.drag_selector(event)
        else:
            self.rotate_rectangle(event)

    def handle_buttonrelease_1(self, event):
        if self.selector:
            self.update_center(event)
        if self.is_rotating:
            self.stop_rotation(event)

    def handle_shift_b1(self, event):
        self.start_rotation(event)
        print(self.is_rotating)

    def handle_button_3(self, event):
        self.start_select_area(event)

    def handle_b3_motion(self, event):
        self.update_select_area(event)

    def handle_buttonrelease_3(self, event):
        self.finalize_select_area(event)


    # Manage points ---------------------------------------------------------------------------------------------------------------
    def add_point(self, event):
        # store new point when user clicks
        x, y = event.x, event.y
        point = Point(x, y)
        self.points.append(point)
        self.update()

    def update(self):
        # update canvas with points
        self.merge_selected_points()
        for p in self.points:
            self.canvas.create_rectangle(round(p.x), round(p.y), round(p.x + 1), round(p.y + 1), fill="black", outline="black")
        print("--------------- update ------------------")
        print(self.points) # real value

    def merge_selected_points(self):
        """Merge the selected points back into the original points list."""
        self.points.extend(self.selected_points)
        self.selected_points.clear()


    # Manage selector for selection -----------------------------------------------------------------------------------------------
    # select area
    def start_select_area(self, event):
        """Store the start position when the user clicks to define the selector."""
        if self.selector:
            self.canvas.delete(self.selector.rect)  # Clear previous selector
        self.rect_start = (event.x, event.y)
        self.selector = Selector(self.canvas, event.x, event.y, event.x, event.y)
        self.selector_exits = True

    def update_select_area(self, event):
        """Update the selector as the user drags the mouse."""
        if self.selector:
            self.selector.update_position(self.rect_start[0], self.rect_start[1], event.x, event.y)

    def finalize_select_area(self, event):
        """Finalize the selector and store the points inside."""
        if self.selector:
            x1, y1, x2, y2 = self.selector.x1, self.selector.y1, event.x, event.y
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)

            # Store selected points inside the selector
            self.selected_points = [
                p for p in self.points if x1 <= p.x <= x2 and y1 <= p.y <= y2
            ]
            self.points = [p for p in self.points if not (x1 <= p.x <= x2 and y1 <= p.y <= y2)]
            print(f"Selected Points: {self.selected_points}")
            print(f"Main Points: {self.points}")
            self.selector.update_position(x1, y1, x2, y2)

    # dragging
    def start_drag_selector(self, event):
        """Start dragging the selector."""
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.initial_x, self.initial_y = self.selector.get_center()

    def drag_selector(self, event):
        """Move the selector as the mouse moves."""
        if self.selector:
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y
            self.selector.move(dx, dy)
            self.drag_start_x = event.x
            self.drag_start_y = event.y

    def update_center(self, event):
        """Update the center of the selector while dragging."""
        if self.selector:
            self.final_x, self.final_y = self.selector.get_center()
            print(f"selector center: ({self.final_x}, {self.final_y})")

    # rotation
    def start_rotation(self, event):
        """Start rotating the rectangle with a reference angle of 0."""
        if self.selector:
            self.is_rotating = True
            self.start_angle = 0  # Set initial angle to zero
            self.start_x, self.start_y = event.x, event.y  # Store initial mouse position

    def rotate_rectangle(self, event):
        """Rotate the rectangle based on mouse movement."""
        if self.is_rotating and self.selector:
            dx = event.x - self.start_x
            dy = event.y - self.start_y

            angle_diff = math.degrees(math.atan2(dy, dx))  # Compute new angle from initial position

            # Rotate the selector
            self.selector.rotate(angle_diff)
            self.selector.set_angle(angle_diff)

    def stop_rotation(self, event):
        """Stop rotating the rectangle when mouse button is released."""
        self.is_rotating = False


    # Buttons ---------------------------------------------------------------------------------------------------------------------
    def add_buttons(self):
        btn_translate = ttk.Button(self.toolbar, text="Translate", command=self.translate_btn)
        btn_translate.pack(side=tk.LEFT, padx=5, pady=5)

        btn_rotate = ttk.Button(self.toolbar, text="Rotate", command=self.rotate_btn)
        btn_rotate.pack(side=tk.LEFT, padx=5, pady=5)

        btn_clear = ttk.Button(self.toolbar, text="Clear", command=self.clear_btn)
        btn_clear.pack(side=tk.LEFT, padx=5, pady=5)

    def clear_btn(self):
        self.canvas.delete("all")
        self.points.clear()
        self.selected_points.clear()
        self.selector_exits = False

    def clear_after_operation(self):
        self.canvas.delete("all")
        self.selector_exits = False
        self.update()

    def translate_btn(self):
        trans = Transformations(self.selected_points)

        dx = self.final_x - self.initial_x
        dy = self.final_y - self.initial_y

        self.selected_points = trans.translate(self.selected_points, dx, dy)

        print("--------------- after translation ------------------")
        print(self.selected_points)

        self.clear_after_operation()

    def rotate_btn(self):
        """Handle rotation when the Rotate button is clicked."""
        if not self.selected_points:
            print("No points selected for rotation.")
            return

        # Get rotation angle from user
        angle = self.selector.get_angle()

        # Define rotation origin (center of selected points)
        ox = sum(p.x for p in self.selected_points) / len(self.selected_points)
        oy = sum(p.y for p in self.selected_points) / len(self.selected_points)

        trans = Transformations(self.selected_points)
        self.selected_points = trans.rotate(self.selected_points, angle, origin=(ox, oy))

        print(f"After rotation: {self.selected_points}")

        self.clear_after_operation()
