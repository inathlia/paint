# comp grafica
## notes
- `interface.py`
    - points are stored in `self.points` and `self.selected_points` on the order they were draw on the canvas
    - `self.points` array store the real value of the pixel, but when ploted with the Interface.update() function it is ronded since there's no float pixel values
    - rotation, scale and reflection take the object center as reference
## libraries
- tkinter
- math
