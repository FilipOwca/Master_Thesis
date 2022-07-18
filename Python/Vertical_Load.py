class Load:
    _verticalLoad = None

    # Calculating total value of characteristic vertical load acting on the structure: concrete dead load, finishing layers on each floor, live load on each floor
    def __init__(self, width, length, tFloor, gLoad, qLoad, walls, hFloor, tWall, columnCs, columnNr, floorNr):
        densityOfConcrete = 25000
        floorDeadLoad = (width * length) * (gLoad + densityOfConcrete * tFloor) * floorNr
        floorLiveLoad = (width * length * qLoad) * floorNr

        lengthWalls = 0

        for wall in walls:
            lengthWalls += wall.length

        wallsDeadLoad = (lengthWalls * hFloor * tWall * densityOfConcrete) * floorNr
        columnDeadLoad = (hFloor * columnCs * columnNr * densityOfConcrete) * floorNr

        self._verticalLoad = floorDeadLoad + wallsDeadLoad + columnDeadLoad + floorLiveLoad

    # Calling final value of the load
    def GetVerticalLoad(self):
        return self._verticalLoad
