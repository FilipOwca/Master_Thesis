from Point import Point


class Wall:

    shearCorrectionFactor = 0.8333333333
    E = 33000000000
    heightOfBuilding = 60

    # Creating an instance of the class Wall and calculating its geometrical and physical properties
    def __init__(self, A: Point, B: Point, tWall):

        self.startYCor = A.DisplayCoordinates()[0]
        self.startZCor = A.DisplayCoordinates()[1]
        self.endYCor = B.DisplayCoordinates()[0]
        self.endZCor = B.DisplayCoordinates()[1]
        self.CalculateParameters(tWall)

    # Calling coordinates of the wall's start and end
    def StartEndCord(self):
        startEndCord = [self.startYCor, self.startZCor, self.endYCor, self.endZCor]
        return startEndCord

    # Main function calculating parameters
    def CalculateParameters(self, tWall):

        # Thickness of wall
        self.thickness = tWall

        # Assigning parameters of a wall
        gModulus = self.E / (2 * (1 + 0.2))

        # Finding the orientation of the wall's main axis
        if self.startYCor - self.endYCor == 0:
            self.orientation = 'z'
        else:
            self.orientation = 'y'

        # Coordinates of the wall's centre
        self.centreYCor = self.startYCor + (self.endYCor - self.startYCor) / 2
        self.centreZCor = self.startZCor + (self.endZCor - self.startZCor) / 2

        # Length of the wall
        if self.orientation == 'y':
             self.length = (self.endYCor - self.startYCor)

        elif self.orientation == 'z':
             self.length = (self.endZCor - self.startZCor)

        # Second Moment of Inertia
        if self.orientation == 'y':
             self.momentOfInertia = self.thickness * (
                     (self.endYCor - self.startYCor) * (self.endYCor - self.startYCor) * (self.endYCor - self.startYCor)) / 12
        elif self.orientation == 'z':
             self.momentOfInertia = self.thickness * (
                     (self.endZCor - self.startZCor) * (self.endZCor - self.startZCor) * (self.endZCor - self.startZCor)) / 12

        # Bending Stiffness
        self.bendingStiffness = (3 * self.E * self.momentOfInertia) / (
                 self.heightOfBuilding * self.heightOfBuilding * self.heightOfBuilding)

        # Shear Area
        if self.orientation == 'y':
            self.shearArea = (self.endYCor - self.startYCor) * self.thickness * self.shearCorrectionFactor
        elif self.orientation == 'z':
            self.shearArea = (self.endZCor - self.startZCor) * self.thickness * self.shearCorrectionFactor

        # Shear Stiffness
        self.shearStiffness = (gModulus * self.shearArea) / self.heightOfBuilding

        # Equivalent Stiffness
        self.equivalentStiffness = (self.bendingStiffness * self.shearStiffness) / (self.bendingStiffness + self.shearStiffness)

        # Product of the quivalent stiffness and centre's coordinates
        if self.orientation == 'y':
             self.corStiffProduct = self.equivalentStiffness * self.centreZCor

        elif self.orientation == 'z':
             self.corStiffProduct = self.equivalentStiffness * self.centreYCor

        # Torsional Moment of Inertia
        self.torsionalMoment = 0.323 * self.length * self.thickness ** 3


    # Coordinates of wall's centre
    def CentreCoordinates(self):
        shearCentreCoordinates=[self.centreYCor, self.centreZCor]
        return shearCentreCoordinates
