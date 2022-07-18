import numpy as np

class Visualisation:


    def ToTable(self, num_hor_axes, num_ver_axes, testResult):
        testResult = np.rint(testResult)
        num_wall_hor_axis = num_ver_axes - 1
        num_wall_ver_axis = num_hor_axes - 1
        maxNumberOfWalls = (num_hor_axes - 1) * num_ver_axes + (num_ver_axes - 1) * num_hor_axes
        tableWidth = 2 * num_hor_axes - 1
        tableLength = 2 * num_ver_axes - 1
        vis = np.empty([tableWidth, tableLength], dtype=str)

        for i in range(tableWidth):
            for j in range(tableLength):
                if j % 2 == 0 and i % 2 == 0:
                    vis[(i, j)] = "+"
                elif j % 2 == 1 and i % 2 == 0:
                    vis[(i, j)] = "-"
                elif j % 2 == 0 and i % 2 == 1:
                    vis[(i, j)] = "|"
                else:
                    vis[(i, j)] = " "

        wallsy = []
        wallsz = []
        for i in range(num_hor_axes * num_wall_hor_axis):
            wallsy.append(testResult[i])
        for i in range(num_hor_axes * num_wall_hor_axis, maxNumberOfWalls):
            wallsz.append(testResult[i])

        solutionIndex = 0
        for i in range(0, tableWidth, 2):
            for j in range(1, tableLength, 2):
                if wallsy[solutionIndex] == 1:
                    vis[(i, j - 1)] = "#"
                    vis[(i, j)] = "#"
                    vis[(i, j + 1)] = "#"
                solutionIndex += 1

        solutionIndex = 0
        for i in range(0, tableLength, 2):
            for j in range(1, tableWidth, 2):
                if wallsz[solutionIndex] == 1:
                    vis[(j - 1, i)] = "#"
                    vis[(j, i)] = "#"
                    vis[(j + 1, i)] = "#"
                solutionIndex += 1
        return vis