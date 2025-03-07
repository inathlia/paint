import tkinter as tk
from tkinter import ttk

from point import Point

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

        # Bind mouse click event
        self.canvas.bind("<Button-1>", self.draw_pixel)

    def draw_pixel(self, event):
        # draw pixel on canvas and store it on array
        x, y = event.x, event.y
        point = Point(x, y)
        self.points.append(point)
        self.canvas.create_rectangle(x, y, x+1, y+1, fill="black", outline="black")

        # for p in self.points:
        #     print(p)

    def add_buttons(self):
        btn_translate = ttk.Button(self.toolbar, text="Translate", command=self.test_translate)
        btn_translate.pack(side=tk.LEFT, padx=5, pady=5)

        btn_rotate = ttk.Button(self.toolbar, text="Rotate", command=self.test_rotate)
        btn_rotate.pack(side=tk.LEFT, padx=5, pady=5)

        btn_scale = ttk.Button(self.toolbar, text="Scale", command=self.test_scale)
        btn_scale.pack(side=tk.LEFT, padx=5, pady=5)

        btn_clear = ttk.Button(self.toolbar, text="Clear", command=self.clear_canvas)
        btn_clear.pack(side=tk.LEFT, padx=5, pady=5)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points.clear()

