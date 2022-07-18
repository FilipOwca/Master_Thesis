class Point:

    # Coordinates of each point of axes intersection
    def __init__(self, x, y):
        self.x_coordinate = x
        self.y_coordinate = y

    # Used to obtain coordinates of a point
    def DisplayCoordinates(self):
        coordinates = [self.x_coordinate, self.y_coordinate]
        return coordinates
