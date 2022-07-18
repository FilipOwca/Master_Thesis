from Point import Point

# Characteristic parameters of the grid and main (horizontal and vertical) axes of the building.
class Grid:
    def __init__(self, num_ver_axes, num_hor_axes):
        self.num_ver_axes = num_ver_axes
        self.num_hor_axes = num_hor_axes

    # Creating a list of axes intersection points related to the defined grid.
    def SetGrid(self, length, width):
        spacing_x_direction = length // (self.num_ver_axes -1)
        spacing_y_direction = width // (self.num_hor_axes -1)
        points = []
        i = 0
        j = 0
        while i <= width:
            while j <= length:
                point = Point(j,i)
                points.append(point)
                j += spacing_x_direction
            j = 0
            i += spacing_y_direction
        return points

