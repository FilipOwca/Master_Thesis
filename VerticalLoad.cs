namespace Master_Thesis;

class Load
{
    private double _verticalLoad;

    public Load(double width, double length, double tFloor, double gLoad, double qLoad, List<Wall> walls, double hFloor, double tWall, double columnCs, double columnNr, double floorNr)
    {
        
        var floorDeadLoad = (width * length) * (gLoad + 25000 * tFloor) * floorNr;
        var floorLiveLoad = (width * length * qLoad) * floorNr;

        double lengthWalls = 0;

        foreach (Wall wall in walls)
        {
            lengthWalls += wall.Length();
        }

        var wallsDeadLoad = (lengthWalls * hFloor * tWall * 25000) * floorNr;
        var columnDeadLoad = (hFloor * columnCs * columnNr * 25000) * floorNr;

        _verticalLoad = floorDeadLoad + wallsDeadLoad + columnDeadLoad + floorLiveLoad;
    }

    public double GetVerticalLoad()
    { return _verticalLoad; }
    
}