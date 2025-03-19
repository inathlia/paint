import tkinter as tk
from tkinter import ttk, Toplevel
import tkinter.messagebox as messagebox
import math

from point import Point
from transformations import Transformations
from selection import Selector
from rasterization.line import Line
from rasterization.circle import Circle

class GraphicsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Computer Graphics Application")

        # toolbar with buttons
        self.toolbar = tk.Frame(root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_buttons()

        # canvas
        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.points = []
        self.selected_points = []

        # bind mouse events
        self.canvas.bind("<Button-1>", self.handle_button_1)
        self.canvas.bind("<B1-Motion>", self.handle_b1_motion)
        self.canvas.bind("<ButtonRelease-1>", self.handle_buttonrelease_1)
        self.canvas.bind("<Shift-Button-1>", self.handle_shift_b1)
        self.canvas.bind("<Control-Button-1>", self.handle_ctrl_b1)
        self.canvas.bind("<Button-3>", self.handle_button_3)
        self.canvas.bind("<B3-Motion>", self.handle_b3_motion)
        self.canvas.bind("<ButtonRelease-3>", self.handle_buttonrelease_3)

        # initialize selector
        self.selector = None
        self.selector_exits = False
        self.is_rotating = False
        self.is_resizing = False
        self.sx = 1 # default value
        self.sy = 1 # default value
        self.selected_axis = 'X' # default value


    # Handle events --------------------------------------------------------------------------------------------------------------
    def handle_button_1(self, event):
        if not self.selector_exits:
            self.add_point(event)
        else:
            self.start_drag_selector(event)

    def handle_b1_motion(self, event):
        if self.selector_exits and not self.is_rotating and not self.is_resizing:
            self.drag_selector(event)
        elif self.selector_exits and self.is_rotating:
            self.rotate_rectangle(event)
        elif self.selector_exits and self.is_resizing:
            self.scale(event)

    def handle_buttonrelease_1(self, event):
        if self.selector:
            self.update_center(event)
        if self.is_rotating:
            self.stop_rotation(event)
        if self.is_resizing:
            self.end_scale()

    def handle_shift_b1(self, event):
        self.start_rotation(event)

    def handle_ctrl_b1(self, event):
        self.start_scale(event)

    def handle_button_3(self, event):
        self.start_select_area(event)

    def handle_b3_motion(self, event):
        self.update_select_area(event)

    def handle_buttonrelease_3(self, event):
        self.finalize_select_area(event)


    # Manage points ---------------------------------------------------------------------------------------------------------------
    # store new point when user clicks
    def add_point(self, event):
        x, y = event.x, event.y
        point = Point(x, y)
        self.points.append(point)
        self.update()

    # update canvas with points
    def update(self):
        self.merge_selected_points()
        for p in self.points:
            self.canvas.create_rectangle(round(p.x), round(p.y), round(p.x + 1), round(p.y + 1), fill="black", outline="black")

    # merge selected points into points list
    def merge_selected_points(self):
        self.points.extend(self.selected_points)
        self.selected_points.clear()

    def draw_points(self, points, color="purple"):
        self.canvas.delete(self.selector.rect)
        self.selector_exits = False
        for p in points:
            self.canvas.create_oval(p.x, p.y, p.x + 1, p.y + 1, fill=color, outline=color)
            self.points.append(p)
        self.merge_selected_points()

    # Manage selector for selection -----------------------------------------------------------------------------------------------
    # selector starts as the pixel where the user clicked
    def start_select_area(self, event):
        if self.selector:
            # delete if already exist a selector
            self.canvas.delete(self.selector.rect)
            self.merge_selected_points()
        self.rect_start = (event.x, event.y)
        self.selector = Selector(self.canvas, event.x, event.y, event.x, event.y)
        self.selector_exits = True

    def update_select_area(self, event):
        if self.selector:
            self.selector.update_position(self.rect_start[0], self.rect_start[1], event.x, event.y)

    # update the selector with last position and store pixels inside
    def finalize_select_area(self, event):
        if self.selector:
            x1, y1, x2, y2 = self.selector.x1, self.selector.y1, event.x, event.y
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)

            # divide points that are inside and outside the selector
            self.selected_points = [
                p for p in self.points if x1 <= p.x <= x2 and y1 <= p.y <= y2
            ]
            self.points = [p for p in self.points if not (x1 <= p.x <= x2 and y1 <= p.y <= y2)]

            self.selector.update_position(x1, y1, x2, y2)

            # print(f"Selected Points: {self.selected_points}")
            # print(f"Main Points: {self.points}")

    ## dragging
    def start_drag_selector(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.initial_x, self.initial_y = self.selector.get_center()

    def drag_selector(self, event):
        if self.selector:
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y

            self.selector.move(dx, dy)

            # updates the start for the next drag movement
            self.drag_start_x = event.x
            self.drag_start_y = event.y

    def update_center(self, event):
        if self.selector:
            self.final_x, self.final_y = self.selector.get_center()

    # rotation
    def start_rotation(self, event):
        if self.selector:
            self.is_rotating = True
            self.start_angle = 0  # set initial angle as zero
            self.start_x, self.start_y = event.x, event.y  # store initial mouse position

    def rotate_rectangle(self, event):
        if self.is_rotating and self.selector:
            dx = event.x - self.start_x
            dy = event.y - self.start_y

            angle_diff = math.degrees(math.atan2(dy, dx))  # calculate new angle from initial position

            self.selector.rotate(angle_diff)
            self.selector.set_angle(angle_diff)

    def stop_rotation(self, event):
        self.is_rotating = False

    ## scaling
    def start_scale(self, event):
        self.is_resizing = True
        # store x2 and y2 since these will be needed later
        self.orig_x2, self.orig_y2 = self.selector.x2, self.selector.y2
        self.start_x = event.x
        self.start_y = event.y

    def scale(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        new_x2 = self.orig_x2 + dx
        new_y2 = self.orig_y2 + dy
        
        self.selector.update_position(self.selector.x1, self.selector.y1, new_x2, new_y2)

    def end_scale(self):
        # calculate sx and sy based on new rectangle size
        new_width = self.selector.x2 - self.selector.x1
        new_height = self.selector.y2 - self.selector.y1
        
        self.sx = new_width / (self.orig_x2 - self.selector.x1)
        self.sy = new_height / (self.orig_y2 - self.selector.y1)
        

    # Buttons ---------------------------------------------------------------------------------------------------------------------
    ## base
    def add_buttons(self):
        btn_translate = ttk.Button(self.toolbar, text="Translate", command=self.translate_btn)
        btn_translate.pack(side=tk.LEFT, padx=5, pady=5)

        btn_rotate = ttk.Button(self.toolbar, text="Rotate", command=self.rotate_btn)
        btn_rotate.pack(side=tk.LEFT, padx=5, pady=5)

        btn_scale = ttk.Button(self.toolbar, text="Scale", command=self.scale_btn)
        btn_scale.pack(side=tk.LEFT, padx=5, pady=5)

        btn_scale = ttk.Button(self.toolbar, text="Reflect", command=self.reflect_btn)
        btn_scale.pack(side=tk.LEFT, padx=5, pady=5)

        btn_scale = ttk.Button(self.toolbar, text="Line", command=self.line_btn)
        btn_scale.pack(side=tk.LEFT, padx=5, pady=5)

        btn_scale = ttk.Button(self.toolbar, text="Circle", command=self.circle_btn)
        btn_scale.pack(side=tk.LEFT, padx=5, pady=5)

        btn_clear = ttk.Button(self.toolbar, text="Clear", command=self.clear_btn)
        btn_clear.pack(side=tk.LEFT, padx=5, pady=5)

    def clear_btn(self):
        self.canvas.delete("all")
        self.points.clear()
        self.selected_points.clear()
        self.selector = None
        self.selector_exits = False
        self.is_rotating = False
        self.is_resizing = False
        self.sx = 1
        self.sy = 1
        self.selected_axis = 'X'

    def clear_after_operation(self):
        self.canvas.delete("all")
        self.selector = None
        self.selector_exits = False
        self.is_rotating = False
        self.is_resizing = False
        self.sx = 1
        self.sy = 1
        self.selected_axis = 'X'
        self.update()

    # transformation
    def translate_btn(self):
        trans = Transformations(self.selected_points)

        if not self.selected_points:
            messagebox.showinfo("Error", "No points selected for translation.")
            return

        dx = self.final_x - self.initial_x
        dy = self.final_y - self.initial_y

        self.selected_points = trans.translate(self.selected_points, dx, dy)

        self.clear_after_operation()

    def rotate_btn(self):
        trans = Transformations(self.selected_points)

        if not self.selected_points:
            messagebox.showinfo("Error", "No points selected for rotation.")
            return

        angle = self.selector.get_angle()

        # takes object center as origin
        ox = sum(p.x for p in self.selected_points) / len(self.selected_points)
        oy = sum(p.y for p in self.selected_points) / len(self.selected_points)

        self.selected_points = trans.rotate(self.selected_points, angle, origin=(ox, oy))

        self.clear_after_operation()

    def scale_btn(self):
        trans = Transformations(self.selected_points)

        if not self.selected_points:
            messagebox.showinfo("Error", "No points selected for scale.")
            return
        
        # takes object center as origin
        ox = sum(p.x for p in self.selected_points) / len(self.selected_points)
        oy = sum(p.y for p in self.selected_points) / len(self.selected_points)

        self.selected_points = trans.scale(self.selected_points, self.sx, self.sy, (ox, oy))

        self.clear_after_operation()

    def reflect_btn(self):
        # pop-up for axis selection
        def show_radio_selector():
            popup = Toplevel(self.root)
            popup.title("Select Reflection Axis")

            select = tk.StringVar()
            select.set("X")  # default

            radio_x = tk.Radiobutton(popup, text="X", variable=select, value="X")
            radio_x.pack(anchor="w")

            radio_y = tk.Radiobutton(popup, text="Y", variable=select, value="Y")
            radio_y.pack(anchor="w")

            radio_xy = tk.Radiobutton(popup, text="XY", variable=select, value="XY")
            radio_xy.pack(anchor="w")

            ok_button = tk.Button(popup, text="OK", command=lambda: self.apply_reflection(select.get(), popup))
            ok_button.pack()

        if not self.selected_points:
            messagebox.showinfo("Error", "No points selected for reflection.")
            return

        show_radio_selector()
    def apply_reflection(self, select, popup):
        popup.destroy()

        trans = Transformations(self.selected_points)

        # takes object center as origin
        ox = sum(p.x for p in self.selected_points) / len(self.selected_points)
        oy = sum(p.y for p in self.selected_points) / len(self.selected_points)

        self.selected_points = trans.reflect(self.selected_points, select, (ox, oy))

        self.clear_after_operation()

    # rasterization
    def line_btn(self):
        # pop-up for line algorithm
        def show_radio_selector():
            popup = Toplevel(self.root)
            popup.title("Select Line Plot Algorithm")

            select = tk.StringVar()
            select.set("DDA")  # default

            radio_x = tk.Radiobutton(popup, text="DDA", variable=select, value="DDA")
            radio_x.pack(anchor="w")

            radio_y = tk.Radiobutton(popup, text="Bresenham", variable=select, value="Bresenham")
            radio_y.pack(anchor="w")

            ok_button = tk.Button(popup, text="OK", command=lambda: self.plot_line(select.get(), popup))
            ok_button.pack()

        if len(self.selected_points) != 2:
            messagebox.showinfo("Error", "Please select only 2 points.")
            return
        show_radio_selector()
    def plot_line(self, select, popup):
        popup.destroy()

        l = Line(self.selected_points[0], self.selected_points[1])

        if select == "DDA":
            line = l.dda()
        else:
            line = l.bresenham()
        
        self.draw_points(line)

    def circle_btn(self):
        if len(self.selected_points) != 2:
            messagebox.showinfo("Error", "Please select only 2 points.")
            return
        
        # 1st point selected is the center and the 2nd will define the radius length
        c = Circle(self.selected_points[0], self.selected_points[1])

        circle = c.bresenham()

        self.draw_points(circle)
        
