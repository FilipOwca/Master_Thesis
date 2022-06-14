namespace Master_Thesis;

class Grid
{
    // Characteristic parameters of the grid and main (horizontal and vertical) axes of the building.
    private readonly double _numberVerticalAxes;
    private readonly double _numberHorizontalAxes;
    private double _spacingXdirection;
    private double _spacingYdirection;

    public Grid(double numVerAxes, double numHorAxes)
    {
        _numberVerticalAxes = numVerAxes;
        _numberHorizontalAxes = numHorAxes;
    }

    // Creating a list of axes intersection points related to the defined grid.
    public List<Point> SetGrid(double length, double width)
    {
        _spacingXdirection = length / (_numberVerticalAxes - 1);
        _spacingYdirection = width / (_numberHorizontalAxes - 1);

        List<Point> points = new List<Point>();

        for (double i = 0; i <= width; i += _spacingYdirection)
        {
            for (double j = 0; j <= length; j += _spacingXdirection)
            {
                var point = new Point(j, i);
                points.Add(point);
            }
        }
        return points;
    }

}