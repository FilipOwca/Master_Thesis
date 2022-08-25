from Point import Point
from WallSegment import WallSegment
from Wall import Wall
from StructuralComponent import StructuralComponent
from FreeFormBuilding import FreeFormBuilding
from FreeformLoad import FreeFormLoad
import math

area = 800
hFloor = 4
heightOfBuilding = 60
floorNr = heightOfBuilding / hFloor
youngModulus = 33000000000
youngModulusDesign = youngModulus / 1.2
shearModulusDesign = youngModulusDesign / 2.4
tFloor = 0.3
columnCs = 0.09
columnNr = 10
gLoad = 2500
qLoad = 3000


# Definition of the list of points

points = []
p1 = Point(10,10)
p2 = Point(30,10)
p3 = Point(40,20)
p4 = Point(30,40)
p5 = Point(0,30)
p6 = Point(20,30)
p7 = Point(30,20)
points = [p1, p2, p3, p4, p5, p6, p7]
tWall = 0.2

# Definition of possible wall segments

numOfWalls = 11
wallA = WallSegment(p1,p2, tWall, "wallA")
wallB = WallSegment(p2,p3, tWall, "wallB")
wallC = WallSegment(p3,p4, tWall, "wallC")
wallD = WallSegment(p4,p5, tWall, "wallD")
wallE = WallSegment(p5,p1, tWall, "wallE")
wallF = WallSegment(p1,p6, tWall, "wallF")
wallG = WallSegment(p5,p6, tWall, "wallG")
wallH = WallSegment(p6,p4, tWall, "wallH")
wallI = WallSegment(p6,p7, tWall, "wallI")
wallJ = WallSegment(p7,p3, tWall, "wallJ")
wallK = WallSegment(p7,p2, tWall, "wallK")

segments = [wallA, wallB, wallC, wallD, wallE, wallF, wallG, wallH, wallI, wallJ, wallK]

# solution = [0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0]
# solution = [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1]
# solution = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
solution = [0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0]

list_comps_walls = []
list_comps_points = []

#Create a list of components, one wall = one component
for i in range(0, len(solution)):
    if solution[i] == 1:
        comp_walls = set()
        comp_points = set()
        comp_walls.add(segments[i])
        comp_points.add(segments[i].startPoint)
        comp_points.add(segments[i].endPoint)
        list_comps_walls.append(comp_walls)
        list_comps_points.append(comp_points)

#Joint the sets with intersection different than null
for i in range(0, len(list_comps_points)):
    for j in range(0, len(list_comps_points)):
        if i != j and not list_comps_points[i].isdisjoint(list_comps_points[j]):
            list_comps_points[i].update(list_comps_points[j])
            list_comps_walls[i].update(list_comps_walls[j])
            list_comps_points[j].clear()
            list_comps_walls[j].clear()

#Get rid of empty sets
finalList = []
for j in list_comps_walls:
    if j != set():
        finalList.append(list(j))

for i in finalList:
    print("Comp", i)
    for k in i:
        print(k.name)

components = []
for i in finalList:
    components.append(StructuralComponent(i))

print("mass center of component 1", components[0].centreYCor, components[0].centreZCor)
print("mass center of component 2",components[1].centreYCor, components[1].centreZCor)

building = FreeFormBuilding()

def TranslationY(components):
    FvBBy = 7.8 * floorNr / (floorNr + 1.6) * 0.4 * \
            (youngModulusDesign * building.SumsInertiaMoments(components)[1]) / (heightOfBuilding * heightOfBuilding)
    value = 0.1 * FvBBy / 1e6
    return value

def TranslationZ(components):
    FvBBz = 7.8 * floorNr / (floorNr + 1.6) * 0.4 * \
            (youngModulusDesign * building.SumsInertiaMoments(components)[0]) / (heightOfBuilding * heightOfBuilding)
    value = 0.1 * FvBBz / 1e6
    return value

Load = FreeFormLoad(area, tFloor, gLoad, qLoad, components, hFloor, columnCs, columnNr, floorNr)
verticalLoad = Load.GetVerticalLoad()


def Rotation(components, verticalLoad):
    shearCoordinates = building.ShearCenter(components)
    c = math.sqrt((length / 2 - shearCoordinates[0]) * (length / 2 - shearCoordinates[0]) +
                  (width / 2 - shearCoordinates[1]) * (width / 2 - shearCoordinates[1]))
    sumTorsionalMoment = building.SumTorsionalMoment(walls)
    warpingAreaMoment = building.WarpingAreaMoment(walls)
    RotationL = 1 / heightOfBuilding * math.sqrt((youngModulusDesign * warpingAreaMoment / 1e6) /
                                                 (verticalLoad * ((d * d / 12) + c * c))) + 1 / 2.28 * \
                math.sqrt(shearModulusDesign * sumTorsionalMoment / (verticalLoad * ((d * d / 12) + c * c)))
    return RotationL

# Validation of the translation and rotation conditions
print("Translation in Y Direction: ", verticalLoad / 1e6, " <= ", TranslationY(components)) # 14.67 = verticalLoad / 1e6
print("Translation in Z Direction: ", verticalLoad / 1e6, " <= ", TranslationZ(components))
# print("Rotation: ", Rotation(solution), " >= ", RotationLimit)

print("Shear center component 1:", components[0].shear_centreYCor, components[0].shear_centreZCor)
print("Shear center component 2:", components[1].shear_centreYCor, components[1].shear_centreZCor)

print("Shear center of the building:", building.ShearCenter(components)[0], building.ShearCenter(components)[1] )