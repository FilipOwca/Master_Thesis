import math
from Building import Building
from CreateWalls import CreateWalls
from Grid import Grid
from Visualisation import Visualisation
from Wall import Wall
from Vertical_Load import Load
from pymoo.optimize import minimize
from pymoo.core.problem import ElementwiseProblem
import numpy as np
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.factory import get_sampling, get_crossover, get_mutation

# Input data for the program: building's dimensions, thickness of walls and floor, loads, material parameters.
# *Given in SI Units*
width = 15
length = 20
hFloor = 4
heightOfBuilding = 60
floorNr = heightOfBuilding / hFloor
tFloor = 0.3
columnCs = 0.09
columnNr = 10
gLoad = 2500
qLoad = 3000
youngModulus = 33000000000
youngModulusDesign = youngModulus / 1.2
shearModulusDesign = youngModulusDesign / 2.4
num_ver_axes = 5
num_hor_axes = 4
num_wall_hor_axis = num_ver_axes - 1
num_wall_ver_axis = num_hor_axes - 1
min_thick = 0.15

# Diagonal of the building's plan
d = math.sqrt(width * width + length * length)

# New instance of class Building
building = Building()

# Creating the list of points (axes' intersections) based on given number of axes
grid = Grid(num_ver_axes, num_hor_axes)
listOfPoints = grid.SetGrid(length, width)

maxNumberOfWalls = (num_hor_axes - 1) * num_ver_axes + (num_ver_axes - 1) * num_hor_axes

# Finding the coordinates of the shear centre of the bracing system (walls)

# Distance between geometrical center and shear center of the building

# Physical parameters related to the bracing system (layout of walls)

# Global buckling loads for pure bending about Y (horizontal) and Z (vertical) axes

# Global buckling load for pure shear about Y(horizontal) and Z (vertical) axes

# Total characteristic vertical load acting on the building

# Global buckling load taking into account bending and shear

# Left and right-hand side of rotational stability formula
RotationLimit = 1 / math.sqrt(0.31 * floorNr / (floorNr + 1.6))

def AmountOfConcrete(walls):

    amountOfConcrete = 0
    for wall in walls:
        concrete = wall.length * wall.thickness * hFloor
        amountOfConcrete += concrete

    return amountOfConcrete

def WallCounter(solution):

    solution = np.around(solution, decimals=2)
    wallsy = []
    wallsz = []
    for i in range(num_hor_axes * num_wall_hor_axis):
        if solution[i] >= 0.15:
            wallsy.append(solution[i])
        else:
            wallsy.append(0)
    for i in range(num_hor_axes * num_wall_hor_axis, maxNumberOfWalls):
        if solution[i] >= 0.15:
            wallsz.append(solution[i])
        else:
            wallsz.append(0)

    sumOfWalls = [sum(wallsy), sum(wallsz)]
    return sumOfWalls

def TranslationY(walls):
    FvBBy = 7.8 * floorNr / (floorNr + 1.6) * 0.4 * \
            (youngModulusDesign * building.SumInertialMomentY(walls)) / (heightOfBuilding * heightOfBuilding)
    FvBSy = shearModulusDesign * building.SumShearAreaY(walls)
    FVBy = FvBBy / (1 + FvBBy / FvBSy)
    value = 0.1 * FVBy / 1e6
    return value

def TranslationZ(walls):
    FvBBz = 7.8 * floorNr / (floorNr + 1.6) * 0.4 * \
            (youngModulusDesign * building.SumInertialMomentZ(walls)) / (heightOfBuilding * heightOfBuilding)
    FvBSz = shearModulusDesign * building.SumShearAreaZ(walls)
    FVBz = FvBBz / (1 + FvBBz / FvBSz)
    value = 0.1 * FVBz / 1e6
    return value

def Rotation(walls, verticalLoad):
    shearCoordinates = building.ShearCentre(walls)
    c = math.sqrt((length / 2 - shearCoordinates[0]) * (length / 2 - shearCoordinates[0]) +
                  (width / 2 - shearCoordinates[1]) * (width / 2 - shearCoordinates[1]))
    sumTorsionalMoment = building.SumTorsionalMoment(walls)
    warpingAreaMoment = building.WarpingAreaMoment(walls)
    RotationL = 1 / heightOfBuilding * math.sqrt((youngModulusDesign * warpingAreaMoment / 1e6) /
                                                 (verticalLoad * ((d * d / 12) + c * c))) + 1 / 2.28 * \
                math.sqrt(shearModulusDesign * sumTorsionalMoment / (verticalLoad * ((d * d / 12) + c * c)))
    return RotationL

class QuantityOfConcrete(ElementwiseProblem):

    def __init__(self):
        super().__init__(n_var=maxNumberOfWalls,
                         n_obj=4,
                         n_constr=3,
                         xl=np.zeros(maxNumberOfWalls),
                         xu=np.ones(maxNumberOfWalls) * 0.5)

    def _evaluate(self, solution, out, *args, **kwargs):
        from Vertical_Load import Load

        nrWalls = WallCounter(solution)

        if np.all(nrWalls):

            wallCreator = CreateWalls()
            walls = wallCreator.ConstructWalls(num_ver_axes, num_hor_axes, listOfPoints, solution, min_thick)
            Load = Load(width, length, tFloor, gLoad, qLoad, walls, hFloor, columnCs, columnNr, floorNr)
            verticalLoad = Load.GetVerticalLoad()

            transZ = TranslationZ(walls)
            transY = TranslationY(walls)
            rot = Rotation(walls, verticalLoad)

            f1 = AmountOfConcrete(walls)
            f2 = - transY
            f3 = - transZ
            f4 = - rot

            g1 = verticalLoad / 1e6 - transY
            g2 = verticalLoad / 1e6 - transZ
            g3 = RotationLimit - rot
        else:
            f1 = np.infty
            f2 = np.infty
            f3 = np.infty
            f4 = np.infty
            g1 = np.infty
            g2 = np.infty
            g3 = np.infty

        out['F'] = [f1, f2, f3, f4]
        out['G'] = [g1, g2, g3]

problem = QuantityOfConcrete()

algorithm = NSGA2(pop_size=100, eliminate_duplicates=True)

stop_criteria = ('n_gen',100)

results = minimize(problem=problem, algorithm=algorithm, termination=stop_criteria)

# solution = [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0]
# # solution = np.rint(results.X[0])
# # Validation of the translation and rotation conditions
# print("ŚRODEK : (0, 0)")
# print("Translation in Y Direction: ", TranslationY(solution)[1] / 1e6, " <= ", TranslationY(solution)[0]) # 14.67 = verticalLoad / 1e6
# print("Translation in Z Direction: ", TranslationZ(solution)[1] / 1e6, " <= ", TranslationZ(solution)[0])
# print("Rotation: ", Rotation(solution), " >= ", RotationLimit)

# print(results.F)
# print(results.G)
# print(np.rint(results.X[0]))

sorted_values = results.F[results.F[:, 0].argsort()]
print(sorted_values)

results.X = results.X[results.F[:, 0].argsort()]

print(results.X[0])
rounded_X = np.around(results.X[0], decimals=2)
print("Rounded X :", rounded_X)

f = open("data.txt", "w")

visualisation = Visualisation()
for i in range(np.array(results.X).shape[0]):
    vis = visualisation.ToTable(num_hor_axes, num_ver_axes, listOfPoints, results.X[i], min_thick)
    f.write(str(vis))
    f.write("\n")
    f.write("\n")
f.close()

wallCreator = CreateWalls()
walls = wallCreator.ConstructWalls(num_ver_axes, num_hor_axes, listOfPoints, (results.X[0]), min_thick)

for wall in walls:
    print("Wall coordinates: START({},{}) END({},{}) THICKNESS: {}".format(wall.StartEndCord()[0], wall.StartEndCord()[1], wall.StartEndCord()[2], wall.StartEndCord()[3], round(wall.thickness, 2)))

wallsy = []
wallsz = []

for i in range(num_hor_axes * num_wall_hor_axis):
    if results.X[0][i] >= min_thick:
        wallsy.append(rounded_X[i])
    else:
        wallsy.append(0)
for i in range(num_hor_axes * num_wall_hor_axis, maxNumberOfWalls):
    if results.X[0][i] >= min_thick:
        wallsz.append(rounded_X[i])
    else:
        wallsz.append(0)

print("Walls Y :", wallsy)
print("Walls Z :", wallsz)