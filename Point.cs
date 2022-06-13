namespace Master_Thesis;

class Point
{
    private double _xcoordinate;
    private double _ycoordinate;

    public Point(double x, double y)
    {
        _xcoordinate = x;
        _ycoordinate = y;
    }

    public double[] DisplayCoordinates()
    {
        double[] coordinates = new double[2];
        coordinates[0] = _xcoordinate;
        coordinates[1] = _ycoordinate;

        return coordinates;
    }
}