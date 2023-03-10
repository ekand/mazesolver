from tkinter import Tk, BOTH, Canvas

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def draw(self, canvas, fill_color='red'):
        canvas.create_line(
            self.p1.x, self.p1.y,
            self.p2.x, self.p2.y,
            fill=fill_color, width=2
        )
        canvas.pack(fill=BOTH, expand=1)
        

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, bg="white", width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")
    
    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color='green'):
        line.draw(self.__canvas, fill_color)

class Cell:
    """
    _x1 and _y1 represent the top left corner of the cell
    _x2 and _y2 represent the bottom right corner of the cell
    """
    def __init__(self, _x1, _x2, _y1, _y2,
        visited: bool = False,
        _win: Window = None,
        has_left_wall=True,
        has_right_wall=True,
        has_top_wall=True,
        has_bottom_wall=True,
    ):
        self._x1 = _x1
        self._x2 = _x2
        self._y1 = _y1
        self._y2 = _y2
        self.visited = visited
        self._win = _win
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall

    def draw(self):
        if self._win is None:
            return
        l = Line(Point(self._x1,self._y1), Point(self._x2, self._y1))
        if self.has_top_wall:
            self._win.draw_line(l)
        else:
            self._win.draw_line(l, 'white')
        l = Line(Point(self._x2,self._y1), Point(self._x2, self._y2))
        if self.has_right_wall:
            self._win.draw_line(l)
        else:
            self._win.draw_line(l, 'white')
        l = Line(Point(self._x2,self._y2), Point(self._x1, self._y2))
        if self.has_bottom_wall:        
            self._win.draw_line(l)
        else:
            self._win.draw_line(l, 'white')
        l = Line(Point(self._x1,self._y2), Point(self._x1, self._y1))
        if self.has_left_wall:
            self._win.draw_line(l)
        else:
            self._win.draw_line(l, 'white')

    def __repr__(self):
        return f'Cell: ({self._x1},{self._y1}),({self._x2},{self._y2})'
    
    def draw_move(self, to_cell, undo=False):
        self_x_center = (self._x1 + self._x2) / 2
        to_cell_x_center = (to_cell._x1 + to_cell._x2) / 2
        self_y_center = (self._y1 + self._y2) / 2
        to_cell_y_center = (to_cell._y1 + to_cell._y2) / 2    
        if undo:
            color = 'red'
        else:
            color = 'gray'
        l = Line(Point(self_x_center, self_y_center), Point(to_cell_x_center, to_cell_y_center)) 
        self._win.draw_line(l, color)