namespace Master_Thesis;

class Load
{
    private double _verticalLoad;

    // Calculating total value of characteristic vertical load acting on the structure: concrete dead load, finishing layers on each floor, live load on each floor
    public Load(double width, double length, double tFloor, double gLoad, double qLoad, List<Wall> walls, double hFloor, double tWall, double columnCs, double columnNr, double floorNr)
    {
        const int densityOfConcrete = 25000;
        var floorDeadLoad = (width * length) * (gLoad + densityOfConcrete * tFloor) * floorNr;
        var floorLiveLoad = (width * length * qLoad) * floorNr;

        double lengthWalls = 0;

        foreach (Wall wall in walls)
        {
            lengthWalls += wall.Length();
        }

        var wallsDeadLoad = (lengthWalls * hFloor * tWall * densityOfConcrete) * floorNr;
        var columnDeadLoad = (hFloor * columnCs * columnNr * densityOfConcrete) * floorNr;

        _verticalLoad = floorDeadLoad + wallsDeadLoad + columnDeadLoad + floorLiveLoad;
    }

    // Calling final value of the load
    public double GetVerticalLoad()
    { return _verticalLoad; }
    
}