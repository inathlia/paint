import tkinter as tk
from tkinter import ttk

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
        self.canvas.bind("<Button-3>", self.handle_button_3)
        self.canvas.bind("<B3-Motion>", self.handle_b3_motion)
        self.canvas.bind("<ButtonRelease-3>", self.handle_buttonrelease_3)

        # Initialize selector
        self.selector = None

    # Handle mouse events for dragging and selection
    def handle_button_1(self, event):
        if self.selector is None:  # Create a new point if no selector exists
            self.add_point(event)
        else:
            self.start_drag_selector(event)

    def handle_b1_motion(self, event):
        if self.selector:
            self.drag_selector(event)

    def handle_buttonrelease_1(self, event):
        if self.selector:
            self.update_center(event)

    def handle_button_3(self, event):
        self.start_select_area(event)

    def handle_b3_motion(self, event):
        self.update_select_area(event)

    def handle_buttonrelease_3(self, event):
        self.finalize_select_area(event)

    # Manage points
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
            self.canvas.create_rectangle(p.x, p.y, p.x + 1, p.y + 1, fill="black", outline="black")
        print("--------------- update ------------------")
        print(self.points)

    def merge_selected_points(self):
        """Merge the selected points back into the original points list."""
        self.points.extend(self.selected_points)
        self.selected_points.clear()

    # Manage selector for selection
    def start_select_area(self, event):
        """Store the start position when the user clicks to define the selector."""
        if self.selector:
            self.canvas.delete(self.selector.rect)  # Clear previous selector
        self.rect_start = (event.x, event.y)
        self.selector = Selector(self.canvas, event.x, event.y, event.x, event.y)

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

    # Buttons and canvas clearing
    def add_buttons(self):
        btn_translate = ttk.Button(self.toolbar, text="Translate", command=self.translate_btn)
        btn_translate.pack(side=tk.LEFT, padx=5, pady=5)

        btn_clear = ttk.Button(self.toolbar, text="Clear", command=self.clear_canvas)
        btn_clear.pack(side=tk.LEFT, padx=5, pady=5)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points.clear()
        self.selected_points.clear()

    def translate_btn(self):
        trans = Transformations(self.selected_points)

        dx = self.final_x - self.initial_x
        dy = self.final_y - self.initial_y

        self.selected_points = trans.translate(self.selected_points, dx, dy)

        print("--------------- after translation ------------------")
        print(self.selected_points)

        self.canvas.delete("all")
        self.rect_exists = False
        self.update()
