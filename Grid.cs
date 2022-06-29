namespace Master_Thesis;

class Grid
{
    // Characteristic parameters of the grid and main (horizontal and vertical) axes of the building.
    private readonly int _numberVerticalAxes;
    private readonly int _numberHorizontalAxes;

    public Grid(int numVerAxes, int numHorAxes)
    {
        _numberVerticalAxes = numVerAxes;
        _numberHorizontalAxes = numHorAxes;
    }

    // Creating a list of axes intersection points related to the defined grid.
    public List<Point> SetGrid(int length, int width)
    {
         var spacingXdirection = length / (_numberVerticalAxes - 1);
         var spacingYdirection = width / (_numberHorizontalAxes - 1);

        List<Point> points = new List<Point>();

        for (int i = 0; i <= width; i += spacingYdirection)
        {
            for (int j = 0; j <= length; j += spacingXdirection)
            {
                var point = new Point(j, i);
                points.Add(point);
            }
        }
        return points;
    }

    public List<Point> GridOfAxes()
    {

        List<Point> points = new List<Point>();

        for (int i = 1; i <= _numberHorizontalAxes; i ++)
        {
            for (int j = 1; j <= _numberVerticalAxes; j ++)
            {
                var point = new Point(j, i);
                points.Add(point);
            }
        }
        return points;
    }
}