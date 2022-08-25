from Point import Point
import math
from Wall import Wall

class WallSegment:


    def __init__(self, A: Point, B: Point, tWall, name):

        self.startPoint = A
        self.endPoint = B
        self.name = name

        self.startYCor = A.DisplayCoordinates()[0]
        self.startZCor = A.DisplayCoordinates()[1]
        self.endYCor = B.DisplayCoordinates()[0]
        self.endZCor = B.DisplayCoordinates()[1]
        self.CalculateAdditionalParameters(tWall)

    def CalculateAdditionalParameters(self, tWall):


        #Thickness
        self.thickness = tWall

        # Length of the wall
        self.length = math.sqrt((self.endYCor - self.startYCor)**2 + (self.endZCor - self.startZCor)**2)

        # Coordinates of the wall's centre
        self.centreYCor = self.startYCor + (self.endYCor - self.startYCor) / 2
        self.centreZCor = self.startZCor + (self.endZCor - self.startZCor) / 2
        # print("centreYCor", self.name, self.centreYCor)
        # print("centreZCor:", self.name, self.centreZCor)

        # Second Moment of Inertia

        self.momentOfInertiaY = self.thickness * (abs(self.endZCor - self.startZCor))**3 / 12
        self.momentOfInertiaZ = self.thickness * (abs(self.endYCor - self.startYCor))**3 / 12
        # print("momentOfInertiaY", self.name, self.momentOfInertiaY)
        # print("momentOfInertiaZ:", self.name, self.momentOfInertiaZ)


        # Area
        self.area = self.thickness * self.length

        #Product of inertia moment and coordinate

        self.coord_inertia_productY = self.momentOfInertiaY * self.centreYCor
        self.coord_inertia_productZ = self.momentOfInertiaZ * self.centreZCor
        # print("coord_inertia_productY", self.name, self.coord_inertia_productY)
        # print("coord_inertia_productZ:", self.name, self.coord_inertia_productZ)