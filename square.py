class Square:
    def __init__(self, offset_x, offset_y, width, height, color, invisible=False):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.width = width
        self.height = height
        self.color = color
        self.invisible = invisible