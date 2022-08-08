import numpy as np
from CreateWalls import CreateWalls

class Visualisation:


    def ToTable(self, num_hor_axes, num_ver_axes, listOfPoints, testResult):
        # testResult = np.rint(testResult)



        num_wall_hor_axis = num_ver_axes - 1
        num_wall_ver_axis = num_hor_axes - 1
        maxNumberOfWalls = (num_hor_axes - 1) * num_ver_axes + (num_ver_axes - 1) * num_hor_axes
        tableWidth = 2 * num_hor_axes - 1
        tableLength = 2 * num_ver_axes - 1
        vis = np.empty([tableWidth, tableLength], dtype="<U2")

        for i in range(tableWidth):
            for j in range(tableLength):
                if j % 2 == 0 and i % 2 == 0:
                    vis[(i, j)] = "++"
                elif j % 2 == 1 and i % 2 == 0:
                    vis[(i, j)] = "=="
                elif j % 2 == 0 and i % 2 == 1:
                    vis[(i, j)] = "||"
                else:
                    vis[(i, j)] = "  "

        testResult = np.around(testResult, decimals=2)

        wallCreator = CreateWalls()
        walls = wallCreator.ConstructWalls(num_ver_axes, num_hor_axes, listOfPoints, testResult)

        wallsy = []
        wallsz = []

        for i in range(num_hor_axes * num_wall_hor_axis):
            if testResult[i] >= 0.15:
                wallsy.append(testResult[i])
            else:
                wallsy.append(0)
        for i in range(num_hor_axes * num_wall_hor_axis, maxNumberOfWalls):
            if testResult[i] >= 0.15:
                wallsz.append(testResult[i])
            else:
                wallsz.append(0)

        # for i in range(num_hor_axes * num_wall_hor_axis):
        #     wallsy.append(testResult[i])
        # for i in range(num_hor_axes * num_wall_hor_axis, maxNumberOfWalls):
        #     wallsz.append(testResult[i])

        wall_count = 0
        solutionIndex = 0
        for i in range(0, tableWidth, 2):
            is_wall = 0
            for j in range(1, tableLength, 2):
                if wallsy[solutionIndex] != 0 and is_wall == 0 and solutionIndex % 4 == 3:
                    is_wall = 1
                    vis[(i, j - 1)] = round(walls[wall_count].thickness, 2) * 100
                    vis[(i, j)] = round(walls[wall_count].thickness, 2) * 100
                    vis[(i, j + 1)] = round(walls[wall_count].thickness, 2) * 100
                    wall_count += 1
                elif wallsy[solutionIndex] != 0 and is_wall == 0 and solutionIndex % 4 != 3:
                    is_wall = 1
                    vis[(i, j - 1)] = round(walls[wall_count].thickness, 2) * 100
                    vis[(i, j)] = round(walls[wall_count].thickness, 2) * 100
                    vis[(i, j + 1)] = round(walls[wall_count].thickness, 2) * 100
                elif wallsy[solutionIndex] != 0 and is_wall == 1 and solutionIndex % 4 == 3:
                    vis[(i, j - 1)] = round(walls[wall_count].thickness, 2) * 100
                    vis[(i, j)] = round(walls[wall_count].thickness, 2) * 100
                    vis[(i, j + 1)] = round(walls[wall_count].thickness, 2) * 100
                    wall_count += 1
                elif wallsy[solutionIndex] != 0 and is_wall == 1 and solutionIndex % 4 != 3:
                    vis[(i, j - 1)] = round(walls[wall_count].thickness, 2) * 100
                    vis[(i, j)] = round(walls[wall_count].thickness, 2) * 100
                    vis[(i, j + 1)] = round(walls[wall_count].thickness, 2) * 100
                elif wallsy[solutionIndex] == 0 and is_wall == 1:
                    wall_count += 1
                    is_wall = 0
                else:
                    is_wall = 0
                solutionIndex += 1

        solutionIndex = 0
        for i in range(0, tableLength, 2):
            is_wall = 0
            for j in range(1, tableWidth, 2):
                if wallsz[solutionIndex] != 0 and is_wall == 0 and solutionIndex % 3 == 2:
                    is_wall = 1
                    vis[(j - 1, i)] = round(walls[wall_count].thickness, 2) * 100
                    vis[(j, i)] = round(walls[wall_count].thickness, 2) * 100
                    vis[(j + 1, i)] = round(walls[wall_count].thickness, 2) * 100
                    wall_count += 1
                elif wallsz[solutionIndex] != 0 and is_wall == 0 and solutionIndex % 3 != 2:
                    is_wall = 1
                    vis[(j - 1, i)] = round(walls[wall_count].thickness, 2) * 100
                    vis[(j, i)] = round(walls[wall_count].thickness, 2) * 100
                    vis[(j + 1, i)] = round(walls[wall_count].thickness, 2) * 100
                elif wallsz[solutionIndex] != 0 and is_wall == 1 and solutionIndex % 3 == 2:
                    vis[(j - 1, i)] = round(walls[wall_count].thickness, 2) * 100
                    vis[(j, i)] = round(walls[wall_count].thickness, 2) * 100
                    vis[(j + 1, i)] = round(walls[wall_count].thickness, 2) * 100
                    wall_count += 1
                elif wallsz[solutionIndex] != 0 and is_wall == 1 and solutionIndex % 3 != 2:
                    vis[(j - 1, i)] = round(walls[wall_count].thickness, 2) * 100
                    vis[(j, i)] = round(walls[wall_count].thickness, 2) * 100
                    vis[(j + 1, i)] = round(walls[wall_count].thickness, 2) * 100
                elif wallsz[solutionIndex] == 0 and is_wall == 1:
                    wall_count += 1
                    is_wall = 0
                else:
                    is_wall = 0
                solutionIndex += 1
        return vis