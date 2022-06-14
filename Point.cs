namespace Master_Thesis;

class Point
{
    // Coordinates of each point of axes intersection
    private readonly double _xcoordinate;
    private readonly double _ycoordinate;

    public Point(double x, double y)
    {
        _xcoordinate = x;
        _ycoordinate = y;
    }

    // Used to obtain coordinates of a point
    public double[] DisplayCoordinates()
    {
        double[] coordinates = new double[2];
        coordinates[0] = _xcoordinate;
        coordinates[1] = _ycoordinate;
        return coordinates;
    }
}