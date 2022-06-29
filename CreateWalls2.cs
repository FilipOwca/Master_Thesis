
namespace Master_Thesis;

class CreateWalls2
{
    static void Main(int numberVerticalAxes, int numberHorizontalAxes, List<Point> listOfPoints)
    {
        var maxNumberOfWalls = (numberHorizontalAxes-1)*numberVerticalAxes + (numberVerticalAxes - 1) * numberHorizontalAxes;
        var numberWallsInHorAxis = numberVerticalAxes - 1;
        var numberWallsInVerAxis = numberHorizontalAxes - 1;
        var solution = new List<int>(maxNumberOfWalls);
        solution[2] = 1;
        solution[3] = 1;
        solution[4] = 1;
        solution[21] = 1;
        solution[26] = 1;
        solution[27] = 1;

        var wallsY = new List<int>();
        var wallsZ = new List<int>();
        var walls = new List<Wall>();

        for (int i = 0; i < numberHorizontalAxes * numberWallsInHorAxis; i++)
            wallsY.Add(solution[i]);
        for (int i = numberHorizontalAxes * numberWallsInHorAxis + 1; i < maxNumberOfWalls; i++)
            wallsZ.Add(solution[i]);

        for (int i = 0; i < numberHorizontalAxes; i++)
        {
            for (int j = 0; j < numberWallsInHorAxis; j++)
            {
                if (wallsY[i * numberHorizontalAxes + j] == 1)
                {
                    var wall = new Wall(listOfPoints[i * numberVerticalAxes + j], listOfPoints[i * numberVerticalAxes + j + 1]);
                    walls.Add(wall);
                }
            }
        }

        for (int i = 0; i < numberVerticalAxes; i++)
        {
            for (int j = 0; j < numberWallsInVerAxis; j++)
            {
                if (wallsZ[i * numberVerticalAxes + j] == 1)
                {
                    var wall = new Wall(listOfPoints[i * numberVerticalAxes + j], listOfPoints[i * numberVerticalAxes + j + 1]);
                    walls.Add(wall);
                }
            }
        }




        static List<List<T>> Split<T>(IList<T> source)
        {
            return source
                .Select((x, i) => new { Index = i, Value = x })
                .GroupBy(x => x.Index / 3)
                .Select(x => x.Select(v => v.Value).ToList())
                .ToList();
        }

    }
}