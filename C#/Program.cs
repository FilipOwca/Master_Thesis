// See https://aka.ms/new-console-template for more information

using JMetalCSharp;

namespace Master_Thesis
{
    class Program
    {
        static void Main(string[] args)
        {

            // Input data for the program: building's dimensions, thickness of walls and floors, loads, material parameters. *Given in SI units*

            const int width = 15;
            const int length = 20;
            const double hFloor = 4;
            const double heightOfBuilding = 12;
            const double floorNr = heightOfBuilding / hFloor;
            const double tFloor = 0.3;
            const double tWall = 0.3;
            const double columnCs = 0.09;
            const double columnNr = 10;
            const double gLoad = 2500;
            const double qLoad = 3000;
            const double youngModulus = 33000000000;
            const double youngModulusDesign = youngModulus / 1.2;
            const double shearModulusDesign = youngModulusDesign / 2.4;
            const int numberVerticalAxes = 5;
            const int numberHorizontalAxes = 4;

            // diagonal of the building plan
            var d = Math.Sqrt(width * width + length * length);

            // New instance of class Building
            var building = new Building();

            // New instance of class Grid (The purpose of this class is to determine the list of points, representing intersections of the main building's axes.
            var grid = new Grid(numberVerticalAxes, numberHorizontalAxes);
            var listOfPoints = grid.SetGrid(length, width);


            var gridOfAxes = grid.GridOfAxes();
            foreach (Point point in gridOfAxes)
            {
                Console.WriteLine("({0} , {1} )", point.DisplayCoordinates()[0], point.DisplayCoordinates()[1]);
            }

            var algorythm = new NSGAII();
            

            // Definition of walls in terms of:(start point, end point, thickness, orientation acc. to coordinate system, E-module, height of the wall). Horizontal walls (y): left to right, Vertical walls (z): bottom to the top.
            var wall1 = new Wall(listOfPoints[2], listOfPoints[4]);
            var wall2 = new Wall(listOfPoints[8], listOfPoints[18]);
            var wall3 = new Wall(listOfPoints[11], listOfPoints[16]);
            var wall4 = new Wall(listOfPoints[5], listOfPoints[6]);
            var walls = new List<Wall> { wall1, wall2, wall3, wall4 };

            // Finding the coordinates of the shear centre of the bracing system (walls)
            var shearCoordinates = building.ShearCentre(walls);

            // Distance between geometrical center and shear center of the building
            var c = Math.Sqrt((length / 2 - shearCoordinates[0]) * (length / 2 - shearCoordinates[0]) +
                              (width / 2 - shearCoordinates[1]) * (width / 2 - shearCoordinates[1]));

            // Physical parameters related to the bracing system (layout of walls)
            var sumTorsionalMoment = building.SumTorsionalMoment(walls);
            var warpingAreaMoment = building.WarpingAreaMoment(walls);

           
            // Global buckling loads for pure bending about Y (horizontal) and Z (vertical) axes.
            var fvBBy = 7.8 * floorNr / (floorNr + 1.6) * 0.4 *
                (youngModulusDesign * building.SumInertialMomentY(walls)) / (heightOfBuilding * heightOfBuilding);

            var fvBBz = 7.8 * floorNr / (floorNr + 1.6) * 0.4 *
                (youngModulusDesign * building.SumInertialMomentZ(walls)) / (heightOfBuilding * heightOfBuilding);

            // Global buckling load for pure shear about Y (horizontal) and Z (vertical) axes.
            var fvBSy = shearModulusDesign * building.SumShearAreaY(walls);
            var fvBSz = shearModulusDesign * building.SumShearAreaZ(walls);

            // Calculation of total characteristic vertical load acting ont the building (dead load of concrete and finishing layers + live load on the floors)
            var load = new Load(width, length, tFloor, gLoad, qLoad, walls, hFloor, tWall, columnCs,
                columnNr, floorNr);
            var verticalLoad = load.GetVerticalLoad();

            // Global buckling load taking into account bending and shear
            var fvBy = fvBBy / (1 + fvBBy / fvBSy);
            var fvBz = fvBBz / (1 + fvBBz / fvBSz);

            // Left and right hand side of rotational stability formula
            var rotationL = 1 / (heightOfBuilding) * Math.Sqrt((youngModulusDesign * warpingAreaMoment / 1e6) / (verticalLoad * ((d * d / 12) + c * c)))  + 1 / 2.28 * Math.Sqrt(shearModulusDesign * sumTorsionalMoment / (verticalLoad * ((d * d / 12) + c * c)));
            var rotationR = 1 / Math.Sqrt(0.31 * floorNr / (floorNr + 1.6));

            // Validation of the translation and rotation proof:
            Console.WriteLine("Translation in Z Direction: {0} <= {1} ", verticalLoad / 1e6, 0.1*fvBy/1e6);
            Console.WriteLine("Translation in Y Direction: {0} <= {1} ", verticalLoad / 1e6, 0.1 * fvBz/1e6);
            Console.WriteLine("Rotation: {0} >= {1}", rotationL, rotationR);
        }
    }
}