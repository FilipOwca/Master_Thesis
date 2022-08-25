from StructuralComponent import StructuralComponent


class FreeFormLoad:

    # Calculating total value of characteristic vertical load acting on the structure: concrete dead load, finishing layers on each floor, live load on each floor
    def __init__(self, area, tFloor, gLoad, qLoad, components, hFloor, columnCs, columnNr, floorNr):
        densityOfConcrete = 25000
        floorDeadLoad = (area) * (gLoad + densityOfConcrete * tFloor) * floorNr
        floorLiveLoad = (area * qLoad) * floorNr

        wallsDeadLoad = 0

        for component in components:
            wallsDeadLoad += component.area * hFloor * densityOfConcrete * floorNr

        columnDeadLoad = (hFloor * columnCs * columnNr * densityOfConcrete) * floorNr

        self._verticalLoad = floorDeadLoad + wallsDeadLoad + columnDeadLoad + floorLiveLoad

    # Calling final value of the load
    def GetVerticalLoad(self):
        return self._verticalLoad
