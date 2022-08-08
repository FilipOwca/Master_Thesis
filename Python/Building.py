from Wall import Wall


class Building:

    # Physical parameters of the bracing system (walls' layout)

    # Finding the Shear Center of the bracing system related to the given walls
    def ShearCentre(self, walls: [Wall]):
        wallsY = []
        wallsZ = []
        # Splitting the walls into groups according to their orientation
        self.SplittingWalls(walls,wallsY,wallsZ)
        # Summing up EquivalentStiffness and CorStiffProduct of each wall in 2 directions separately
        stiffnesses = self.SummingUpStiffness(wallsY, wallsZ)

        # Finding coordinates of the bracing system's shear center
        shearCentreCoordinates = []
        shearCentreCoordinates.append(stiffnesses[3] / stiffnesses[2])
        shearCentreCoordinates.append(stiffnesses[1] / stiffnesses[0])
        self._shearCentreCoordinateY = shearCentreCoordinates[0]
        self._shearCentreCoordinateZ = shearCentreCoordinates[1]

        return shearCentreCoordinates

    def SplittingWalls(self, walls, wallsY, wallsZ):
        for wall in walls:
            if wall.orientation == 'y':
                wallsY.append(wall.equivalentStiffness)
                wallsY.append(wall.corStiffProduct)
            else:
                wallsZ.append(wall.equivalentStiffness)
                wallsZ.append(wall.corStiffProduct)

    def SummingUpStiffness(self, wallsY, wallsZ):

        _sumeEqlStiffinY = 0
        _sumeEqlStiffinZ = 0
        _sumeCorStiffProdinY = 0
        _sumeCorStiffProdinZ = 0

        for i in range(0, len(wallsY)):
            if i % 2 == 0:
                _sumeEqlStiffinY += wallsY[i]
            else:
                _sumeCorStiffProdinY += wallsY[i]

        for i in range(0, len(wallsZ)):
            if i % 2 == 0:
                _sumeEqlStiffinZ += wallsZ[i]
            else:
                _sumeCorStiffProdinZ += wallsZ[i]

        return [_sumeEqlStiffinY, _sumeCorStiffProdinY, _sumeEqlStiffinZ, _sumeCorStiffProdinZ]

    # Finding the warping area moment of the bracing system
    def WarpingAreaMoment(self, walls):
        warpingAreaMoment = 0

        for wall in walls:
            distanceY = wall.CentreCoordinates()[0] - self._shearCentreCoordinateY
            distanceZ = wall.CentreCoordinates()[1] - self._shearCentreCoordinateZ

            if wall.orientation == 'y':
                warpingAreaMoment += distanceZ * distanceZ * wall.equivalentStiffness
            else:
                warpingAreaMoment += distanceY * distanceY * wall.equivalentStiffness

        return warpingAreaMoment

    # Summing up torsional moment of all walls
    def SumTorsionalMoment(self, walls):
        sumTorsionalMoment = 0

        for wall in walls:
            sumTorsionalMoment += wall.torsionalMoment

        return sumTorsionalMoment

    # Summing up moment of inertia of each wall in Y direction (horizontal)
    def SumInertialMomentY(self, walls):
        sumInertiaMomentY = 0

        for wall in walls:
            if wall.orientation == 'z':
                sumInertiaMomentY += wall.momentOfInertia

        return sumInertiaMomentY

    # Summing up moment of inertia of each wall in Z direction (vertical)
    def SumInertialMomentZ(self, walls):
        sumInertiaMomentZ = 0

        for wall in walls:
            if wall.orientation == 'y':
                sumInertiaMomentZ += wall.momentOfInertia

        return sumInertiaMomentZ

    def SumShearAreaY(self, walls):
        sumShearAreaY = 0
        for wall in walls:
            if wall.orientation == 'z':
                sumShearAreaY += wall.shearArea

        return sumShearAreaY

    # Summing up shear are  of each wall in Y direction (horizontal)
    def SumShearAreaZ(self, walls):
        sumShearAreaZ = 0
        for wall in walls:
            if wall.orientation == 'y':
                sumShearAreaZ += wall.shearArea

        return sumShearAreaZ
