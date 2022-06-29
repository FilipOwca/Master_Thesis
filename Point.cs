namespace Master_Thesis;

class Point
{
    // Coordinates of each point of axes intersection
    private readonly int _ycoordinate;
    private readonly int _zcoordinate;

    public Point(int y, int z)
    {
        _ycoordinate = y;
        _zcoordinate = z;
    }

    // Used to obtain coordinates of a point
    public int[] DisplayCoordinates()
    {
        int[] coordinates = new int[2];
        coordinates[0] = _ycoordinate;
        coordinates[1] = _zcoordinate;
        return coordinates;
    }
}