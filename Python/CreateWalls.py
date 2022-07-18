from Wall import Wall
import numpy as np

class CreateWalls:

    def ConstructWalls(self, num_ver_axes, num_hor_axes, points, solution):

        maxNumberOfWalls = (num_hor_axes - 1) * num_ver_axes + (num_ver_axes - 1) * num_hor_axes
        num_wall_hor_axis = num_ver_axes - 1
        num_wall_ver_axis = num_hor_axes - 1

        # Auxiliary lists
        wallsy = []
        wallsz = []
        walls = []

        solution = np.rint(solution)

        # Splitting list of walls into 2 lists for different directions
        for i in range(num_hor_axes * num_wall_hor_axis):
            wallsy.append(solution[i])
        for i in range(num_hor_axes * num_wall_hor_axis, maxNumberOfWalls):
            wallsz.append(solution[i])

        # This loop detects horizontal walls, connects them together if walls are in one axis and adds them to the list
        for i in range(num_hor_axes):
            # Counter of walls in one line
            count = 0
            for j in range(num_wall_hor_axis):
                # Detects the end of the wall at the end of the building
                if wallsy[i * num_wall_hor_axis +j] == 1 and j == (num_wall_hor_axis -1):
                    wall = Wall(points[i * num_ver_axes + (j - count)], points[i * num_ver_axes + j + 1])
                    walls.append(wall)
                # Detects the beginning of the wall
                elif wallsy[i * num_wall_hor_axis + j] == 1:
                    count += 1
                # Detects the end of the wall inside the building
                elif count != 0 and wallsy[i * num_wall_hor_axis +j] == 0:
                    wall = Wall(points[i * num_ver_axes + (j - count)], points[i * num_ver_axes + j])
                    walls.append(wall)
                    count = 0
        # This loop detects vertical walls, connects them together if walls are in one line and adds them to the list
        for i in range(num_ver_axes):
            # Counter of walls in one line
            count = 0
            for j in range(num_wall_ver_axis):
                # Detects the end of the wall at the end of the building
                if wallsz[i * num_wall_ver_axis + j] == 1 and j == (num_wall_ver_axis -1):
                    wall = Wall(points[i + (j - count) * num_ver_axes], points[i + (j + 1) *num_ver_axes])
                    walls.append(wall)
                # Detects the beginning of the wall
                elif wallsz[i * num_wall_ver_axis + j] == 1:
                    count += 1
                # Detects the end of the wall inside the building
                elif count != 0 and wallsz[ i * num_wall_ver_axis + j] == 0:
                    wall = Wall(points[i + (j -count) * num_ver_axes], points[i + j * num_ver_axes])
                    walls.append(wall)
                    count = 0
        return walls