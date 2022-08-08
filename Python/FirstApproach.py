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
tWall = 0.3
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


# Diagonal of the building's plan
d = math.sqrt(width * width + length * length)

# New instance of class Building
building = Building()

# Creating the list of points (axes' intersections) based on given number of axes
grid = Grid(num_ver_axes, num_hor_axes)
listOfPoints = grid.SetGrid(length, width)

maxNumberOfWalls = (num_hor_axes - 1) * num_ver_axes + (num_ver_axes - 1) * num_hor_axes
# solution = [1] * maxNumberOfWalls
# solution = np.random.rand(maxNumberOfWalls)
# print(solution)

# Creation of walls
# wallCreator = CreateWalls()
# walls = wallCreator.ConstructWalls(num_ver_axes, num_hor_axes, listOfPoints, solution)

# for wall in walls:
#     print("Wall coordinates: START({},{}) END({},{})".format(wall.StartEndCord()[0], wall.StartEndCord()[1], wall.StartEndCord()[2], wall.StartEndCord()[3]))
#
# # Finding the coordinates of the shear centre of the bracing system (walls)
# shearCoordinates = building.ShearCentre(walls)
#
# # Distance between geometrical center and shear center of the building
# c = math.sqrt((length / 2 - shearCoordinates[0]) * (length / 2 - shearCoordinates[0]) +
#           (width / 2 - shearCoordinates[1]) * (width / 2 - shearCoordinates[1]))
#
# # Physical parameters related to the bracing system (layout of walls)
# sumTorsionalMoment = building.SumTorsionalMoment(walls)
# warpingAreaMoment = building.WarpingAreaMoment(walls)
#
# # Global buckling loads for pure bending about Y (horizontal) and Z (vertical) axes
# FvBBy = 7.8 * floorNr / (floorNr + 1.6) * 0.4 * \
#          (youngModulusDesign * building.SumInertialMomentY(walls)) / (heightOfBuilding * heightOfBuilding)
# FvBBz = 7.8 * floorNr / (floorNr + 1.6) * 0.4 * \
#          (youngModulusDesign * building.SumInertialMomentZ(walls)) / (heightOfBuilding * heightOfBuilding)
#
# # Global buckling load for pure shear about Y(horizontal) and Z (vertical) axes
# FvBSy = shearModulusDesign * building.SumShearAreaY(walls)
# FvBSz = shearModulusDesign * building.SumShearAreaZ(walls)
#
# # Total characteristic vertical load acting on the building
# Load = Load(width, length, tFloor, gLoad, qLoad, walls, hFloor, tWall, columnCs, columnNr, floorNr)
# verticalLoad = Load.GetVerticalLoad()
#
# # Global buckling load taking into account bending and shear
# FVBy = FvBBy / (1 + FvBBy / FvBSy)
# FVBz = FvBBz / (1 + FvBBz / FvBSz)

# # Left and right-hand side of rotational stability formula
# RotationL = 1 / heightOfBuilding * math.sqrt((youngModulusDesign * warpingAreaMoment / 1e6) /
#                                          (verticalLoad * ((d * d / 12) + c * c))) + 1 / 2.28 * \
#              math.sqrt(shearModulusDesign * sumTorsionalMoment / (verticalLoad * ((d * d / 12) + c * c)))
RotationLimit = 1 / math.sqrt(0.31 * floorNr / (floorNr + 1.6))

def AmountOfConcrete(solution):

    amountOfConcrete = 0
    wallCreator = CreateWalls()
    walls = wallCreator.ConstructWalls(num_ver_axes, num_hor_axes, listOfPoints, solution)

    for wall in walls:
        concrete = wall.length * tWall * hFloor
        amountOfConcrete += concrete

    return amountOfConcrete

def WallCounter(solution):

    solution = np.rint(solution)
    wallsy = []
    wallsz = []
    for i in range(num_hor_axes * num_wall_hor_axis):
        wallsy.append(solution[i])
    for i in range(num_hor_axes * num_wall_hor_axis, maxNumberOfWalls):
        wallsz.append(solution[i])
    sumOfWalls = [sum(wallsy), sum(wallsz)]
    return sumOfWalls

def TranslationY(solution):
    from Vertical_Load import Load
    wallCreator = CreateWalls()
    walls = wallCreator.ConstructWalls(num_ver_axes, num_hor_axes, listOfPoints, solution)
    FvBBy = 7.8 * floorNr / (floorNr + 1.6) * 0.4 * \
            (youngModulusDesign * building.SumInertialMomentY(walls)) / (heightOfBuilding * heightOfBuilding)
    FvBSy = shearModulusDesign * building.SumShearAreaY(walls)
    FVBy = FvBBy / (1 + FvBBy / FvBSy)
    value = 0.1 * FVBy / 1e6
    Load = Load(width, length, tFloor, gLoad, qLoad, walls, hFloor, tWall, columnCs, columnNr, floorNr)
    verticalLoad = Load.GetVerticalLoad()
    result = [value, verticalLoad]
    return result

def TranslationZ(solution):
    from Vertical_Load import Load
    wallCreator = CreateWalls()
    walls = wallCreator.ConstructWalls(num_ver_axes, num_hor_axes, listOfPoints, solution)
    FvBBz = 7.8 * floorNr / (floorNr + 1.6) * 0.4 * \
            (youngModulusDesign * building.SumInertialMomentZ(walls)) / (heightOfBuilding * heightOfBuilding)
    FvBSz = shearModulusDesign * building.SumShearAreaZ(walls)
    FVBz = FvBBz / (1 + FvBBz / FvBSz)
    value = 0.1 * FVBz / 1e6
    Load = Load(width, length, tFloor, gLoad, qLoad, walls, hFloor, tWall, columnCs, columnNr, floorNr)
    verticalLoad = Load.GetVerticalLoad()
    result = [value, verticalLoad]
    return result

def Rotation(solution):
    from Vertical_Load import Load
    wallCreator = CreateWalls()
    walls = wallCreator.ConstructWalls(num_ver_axes, num_hor_axes, listOfPoints, solution)
    shearCoordinates = building.ShearCentre(walls)
    Load = Load(width, length, tFloor, gLoad, qLoad, walls, hFloor, tWall, columnCs, columnNr, floorNr)
    verticalLoad = Load.GetVerticalLoad()
    c = math.sqrt((length / 2 - shearCoordinates[0]) * (length / 2 - shearCoordinates[0]) +
                  (width / 2 - shearCoordinates[1]) * (width / 2 - shearCoordinates[1]))
    sumTorsionalMoment = building.SumTorsionalMoment(walls)
    warpingAreaMoment = building.WarpingAreaMoment(walls)
    RotationL = 1 / heightOfBuilding * math.sqrt((youngModulusDesign * warpingAreaMoment / 1e6) /
                                                 (verticalLoad * ((d * d / 12) + c * c))) + 1 / 2.28 * \
                math.sqrt(shearModulusDesign * sumTorsionalMoment / (verticalLoad * ((d * d / 12) + c * c)))
    return RotationL

# class QuantityOfConcrete(ElementwiseProblem):
#
#     def __init__(self):
#         super().__init__(n_var=maxNumberOfWalls,
#                          n_obj=4,
#                          n_constr=3,
#                          xl=np.zeros(maxNumberOfWalls),
#                          xu=np.ones(maxNumberOfWalls) * 0.5)
#
#     def _evaluate(self, solution, out, *args, **kwargs):
#
#         nrWalls = WallCounter(solution)
#
#         if np.all(nrWalls):
#
#             f1 = AmountOfConcrete(solution)
#
#             transZ = TranslationZ(solution)
#             transY = TranslationY(solution)
#             rot = Rotation(solution)
#
#             f2 = - transY[0]
#             f3 = - transZ[0]
#             f4 = - rot
#
#             g1 = transY[1] / 1e6 - transY[0]
#             g2 = transZ[1] / 1e6 - transZ[0]
#             g3 = RotationLimit - rot
#         else:
#             f1 = np.infty
#             f2 = np.infty
#             f3 = np.infty
#             f4 = np.infty
#             g1 = np.infty
#             g2 = np.infty
#             g3 = np.infty
#
#         out['F'] = [f1, f2, f3, f4]
#         out['G'] = [g1, g2, g3]
#
# problem = QuantityOfConcrete()
#
# algorithm = NSGA2(pop_size=100, eliminate_duplicates=True)
#
# stop_criteria = ('n_gen',100)
#
# results = minimize(problem=problem, algorithm=algorithm, termination=stop_criteria)


# class QuantityOfConcrete(ElementwiseProblem):
#
#     def __init__(self):
#         super().__init__(n_var=maxNumberOfWalls,
#                          n_obj=1,
#                          n_constr=3,
#                          xl=np.zeros(maxNumberOfWalls),
#                          xu=np.ones(maxNumberOfWalls))
#
#     def _evaluate(self, solution, out, *args, **kwargs):
#
#         nrWalls = WallCounter(solution)
#
#         if np.all(nrWalls):
#
#
#             transZ = TranslationZ(solution)
#             transY = TranslationY(solution)
#             rot = Rotation(solution)
#
#             f1 = 0.94 * AmountOfConcrete(solution) - 0.02 * transY[0] - 0.02 * transZ[0] - 0.02 * rot
#
#             g1 = transY[1] / 1e6 - transY[0]
#             g2 = transZ[1] / 1e6 - transZ[0]
#             g3 = RotationLimit - rot
#         else:
#             f1 = np.infty
#             g1 = np.infty
#             g2 = np.infty
#             g3 = np.infty
#
#         out['F'] = [f1]
#         out['G'] = [g1, g2, g3]
#
# problem = QuantityOfConcrete()
#
# algorithm = GA(pop_size=100, eliminate_duplicates=True)
#
# stop_criteria = ('n_gen',100)
#
# results = minimize(problem=problem, algorithm=algorithm, termination=stop_criteria)


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

# sorted_result = results.F[results.F[:, 0].argsort()]
# print(sorted_result)
#
# results.X = results.X[results.F[:, 0].argsort()]
#
# f = open("data.txt", "w")
#
# visualisation = Visualisation()
# for i in range(np.array(results.X).shape[0]):
#     vis = visualisation.ToTable(num_hor_axes, num_ver_axes, results.X[i])
#     f.write(str(vis))
#     f.write("\n")
#     f.write("\n")
# f.close()

