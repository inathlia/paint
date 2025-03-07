import tkinter as tk
from tkinter import ttk

from point import Point
from transformations import Transformations

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

        # Bind mouse click event
        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<Control-Button-1>", self.start_select_area)
        self.canvas.bind("<B1-Motion>", self.update_select_area)
        self.canvas.bind("<ButtonRelease-1>", self.finalize_select_area)

        # Store rectangle attributes
        self.rect_start = None
        self.rect = None


    # MANAGE ARRAYS ---------------------------------------------------------------------------------------
    def add_point(self, event):
        # store new point on array when user clicks
        x, y = event.x, event.y
        point = Point(x, y)
        self.points.append(point)
        self.update()

    def update(self):
        # update canvas with points
        self.merge_selected_points()

        for p in self.points:
            self.canvas.create_rectangle(p.x, p.y, p.x+1, p.y+1, fill="black", outline="black")

        print("--------------- update ------------------")
        print(self.points)

    def merge_selected_points(self):
        """Merge the selected points back into the original points list."""
        self.points.extend(self.selected_points)
        self.selected_points.clear()       


    # MANAGE RECTANGLE ------------------------------------------------------------------------------------
    def start_select_area(self, event):
        """Store the start position when the user clicks to define the rectangle."""
        self.rect_start = (event.x, event.y)
        if self.rect:
            self.canvas.delete(self.rect)  # Clear previous rectangle

    def update_select_area(self, event):
        """Update the rectangle as the user drags the mouse."""
        if self.rect_start:
            if self.rect:
                self.canvas.delete(self.rect)
            x1, y1 = self.rect_start
            x2, y2 = event.x, event.y
            self.rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="pink", width=2)

    def finalize_select_area(self, event):
        """Finalize the rectangle and store the points inside."""
        if self.rect_start:
            x1, y1 = self.rect_start
            x2, y2 = event.x, event.y

            # Normalize the rectangle coordinates
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)

            # Store selected points inside the rectangle
            self.selected_points = [
                p for p in self.points if x1 <= p.x <= x2 and y1 <= p.y <= y2
            ]
            # Remove selected points from the original points list
            self.points = [p for p in self.points if not (x1 <= p.x <= x2 and y1 <= p.y <= y2)]
            print(f"Selected Points: {self.selected_points}")
            print(f"Main Points: {self.points}")
            

    # MANAGE BUTTONS -------------------------------------------------------------------------------------
    def add_buttons(self):
        btn_translate = ttk.Button(self.toolbar, text="Translate", command=self.translate_btn)
        btn_translate.pack(side=tk.LEFT, padx=5, pady=5)

        # btn_rotate = ttk.Button(self.toolbar, text="Rotate", command=self.test_rotate)
        # btn_rotate.pack(side=tk.LEFT, padx=5, pady=5)

        # btn_scale = ttk.Button(self.toolbar, text="Scale", command=self.test_scale)
        # btn_scale.pack(side=tk.LEFT, padx=5, pady=5)

        btn_clear = ttk.Button(self.toolbar, text="Clear", command=self.clear_canvas)
        btn_clear.pack(side=tk.LEFT, padx=5, pady=5)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points.clear()
        self.selected_points.clear()

    def translate_btn(self):
        trans = Transformations(self.selected_points)
        self.selected_points = trans.translate(self.selected_points, dx=20, dy=40)

        print("--------------- after translation ------------------")
        print(self.selected_points)

        self.canvas.delete("all")
        self.update()
