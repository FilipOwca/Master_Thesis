namespace Master_Thesis;

class CreateWalls
{
    public List<Wall> WallsCreation(List<Point> listOfPoints, int numberVerticalAxes, int numberHorizontalAxes)
    {
        var listOfWalls = new List<Wall>();
        var n = numberVerticalAxes;
        var m = numberHorizontalAxes;

        // Random number of walls to create, less than n+m (a condition to ensure the wall creation)
        var numberOfWalls = 4;

        for (int i = 0; i < numberOfWalls; i++)
        {
            // Choosing a random point to start a wall
            var randomPoint = listOfPoints[5];
            var y =randomPoint.DisplayCoordinates()[0];
            var z = randomPoint.DisplayCoordinates()[1];

            // Interior of the building
            if (y > 1 || y < n || z > 1 || z < m)
            {
                // Choosing the direction to create a wall (random), between 1 and 4
                var directionOfWall = 3;

                if (directionOfWall == 1)
                {
                    // Upwards
                    var maxWallLength = m - z;
                    // Choosing a length of the wall to create (random), less than maxWallLength
                    var randomWallLength = 2;
                    var pointB = new Point(y, z + randomWallLength);
                }
                else if (directionOfWall == 2)
                {
                    // Rightwards
                    var maxWallLength = n - y;
                    var randomWallLength = 2;
                    var pointB = new Point(y + randomWallLength, z);
                }
                else if (directionOfWall == 3)
                {
                    // Downwards
                    var maxWallLength = z - 1;
                    var randomWallLength = 2;
                    var pointB = new Point(y, z - randomWallLength);
                }
                else
                {
                    // Leftwards
                    var maxWallLength = y - 1;
                    var randomWallLength = 2;
                    var pointB = new Point(y - randomWallLength, z);
                }


            }
            // Bottom edge
            else if (y > 1 || y < n || z == 1)
            {
                // Choosing the direction to create a wall (random) between 1 and 3
                var directionOfWall = 3;

                if (directionOfWall == 1)
                {
                    // Upwards
                    var maxWallLength = m - z;
                    // Choosing a length of the wall to create (random), less than maxWallLength
                    var randomWallLength = 2;
                    var pointB = new Point(y, z + randomWallLength);
                }
                else if (directionOfWall == 2)
                {
                    // Rightwards
                    var maxWallLength = n - y;
                    var randomWallLength = 2;
                    var pointB = new Point(y + randomWallLength, z);
                }
                else
                {
                    // Leftwards
                    var maxWallLength = y - 1;
                    var randomWallLength = 2;
                    var pointB = new Point(y - randomWallLength, z);
                }
            }
            // Right edge
            else if (y == n || z > 1 || z < m)
            {
                // Choosing the direction to create a wall (random) between 1 and 3
                var directionOfWall = 3;

                if (directionOfWall == 1)
                {
                    // Upwards
                    var maxWallLength = m - z;
                    // Choosing a length of the wall to create (random), less than maxWallLength
                    var randomWallLength = 2;
                    var pointB = new Point(y, z + randomWallLength);
                }
                else if (directionOfWall == 2)
                {
                    // Downwards
                    var maxWallLength = z - 1;
                    var randomWallLength = 2;
                    var pointB = new Point(y, z - randomWallLength);
                }
                else
                {
                    // Leftwards
                    var maxWallLength = y - 1;
                    var randomWallLength = 2;
                    var pointB = new Point(y - randomWallLength, z);
                }
            }
            // Upper edge
            else if (y > 1 || y < n || z == m)
            {
                // Choosing the direction to create a wall (random) between 1 and 3
                var directionOfWall = 3;

                if (directionOfWall == 1)
                {
                    // Rightwards
                    var maxWallLength = n - y;
                    var randomWallLength = 2;
                    var pointB = new Point(y + randomWallLength, z);
                }
                else if (directionOfWall == 2)
                {
                    // Downwards
                    var maxWallLength = z - 1;
                    var randomWallLength = 2;
                    var pointB = new Point(y, z - randomWallLength);
                }
                else
                {
                    // Leftwards
                    var maxWallLength = y - 1;
                    var randomWallLength = 2;
                    var pointB = new Point(y - randomWallLength, z);
                }
            }
            // Left edge
            else if (y == 1 || z > 1 || z < m)
            {
                // Choosing the direction to create a wall (random), between 1 and 3
                var directionOfWall = 3;

                if (directionOfWall == 1)
                {
                    // Upwards
                    var maxWallLength = m - z;
                    // Choosing a length of the wall to create (random), less than maxWallLength
                    var randomWallLength = 2;
                    var pointB = new Point(y, z + randomWallLength);
                }
                else if (directionOfWall == 2)
                {
                    // Rightwards
                    var maxWallLength = n - y;
                    var randomWallLength = 2;
                    var pointB = new Point(y + randomWallLength, z);
                }
                else
                {
                    // Downwards
                    var maxWallLength = z - 1;
                    var randomWallLength = 2;
                    var pointB = new Point(y, z - randomWallLength);
                }
            }
            // Left bottom corner
            else if (y == 1 || z == 1)
            {
                // Choosing the direction to create a wall (random), between 1 and 2
                var directionOfWall = 2;

                if (directionOfWall == 1)
                {
                    // Upwards
                    var maxWallLength = m - z;
                    // Choosing a length of the wall to create (random), less than maxWallLength
                    var randomWallLength = 2;
                    var pointB = new Point(y, z + randomWallLength);
                }
                else
                {
                    // Rightwards
                    var maxWallLength = n - y;
                    var randomWallLength = 2;
                    var pointB = new Point(y + randomWallLength, z);
                }
            }
            // Right bottom corner
            else if (y == n || z == 1)
            {
                // Choosing the direction to create a wall (random), between 1 and 2
                var directionOfWall = 2;

                if (directionOfWall == 1)
                {
                    // Upwards
                    var maxWallLength = m - z;
                    // Choosing a length of the wall to create (random), less than maxWallLength
                    var randomWallLength = 2;
                    var pointB = new Point(y, z + randomWallLength);
                }
                else
                {
                    // Leftwards
                    var maxWallLength = y - 1;
                    var randomWallLength = 2;
                    var pointB = new Point(y - randomWallLength, z);
                }
            }
            // Right upper corner
            else if (y == n || z == m)
            {
                // Choosing the direction to create a wall (random), between 1 and 2
                var directionOfWall = 2;

                if (directionOfWall == 1)
                {
                    // Downwards
                    var maxWallLength = z - 1;
                    var randomWallLength = 2;
                    var pointB = new Point(y, z - randomWallLength);
                }
                else
                {
                    // Leftwards
                    var maxWallLength = y - 1;
                    var randomWallLength = 2;
                    var pointB = new Point(y - randomWallLength, z);
                }
            }
            // Left upper corner
            else if (y == 1 || z == m)
            {
                // Choosing the direction to create a wall (random), between 1 and 2
                var directionOfWall = 2;

                if (directionOfWall == 1)
                {
                    // Downwards
                    var maxWallLength = z - 1;
                    var randomWallLength = 2;
                    var pointB = new Point(y, z - randomWallLength);
                }
                else
                {
                    // Rightwards
                    var maxWallLength = n - y;
                    var randomWallLength = 2;
                    var pointB = new Point(y + randomWallLength, z);
                }
            }

            // var wall = new Wall(randomPoint, pointB);
            // listOfWalls.Add(wall);
        }

        return listOfWalls;
    }
}