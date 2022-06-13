// See https://aka.ms/new-console-template for more information


using System.Diagnostics;

namespace Master_Thesis
{
    class Program
    {
        static void Main(string[] args)
        {
            var building = new Building(20, 15);
            var grid = new Grid(5, 4);

            var listOfPoints = grid.SetGrid(20, 15);

            double YoungsModulus = 33000000000;
            double youngsModulusDesign = YoungsModulus / 1.2;
            double shearModulusDesign = youngsModulusDesign / 2.4;
            double heigthOfBuilding = 12;
            double tWall = 0.3;
            double hFloor = 4;
            double columnCs = 0.09;
            double columnNr = 10;
            double width = 15;
            double length = 20;
            double tFloor = 0.3;
            double gLoad = 2500;
            double qLoad = 3000;
            double floorNr = 3;
            double d = Math.Sqrt(width * width + length * length);
            Console.WriteLine("d:" + d);

            var wall1 = new Wall(listOfPoints[2], listOfPoints[4], tWall, 'y', YoungsModulus, heigthOfBuilding);
            var wall2 = new Wall(listOfPoints[8], listOfPoints[18], tWall, 'z', YoungsModulus, heigthOfBuilding);
            var wall3 = new Wall(listOfPoints[11], listOfPoints[16], tWall, 'z', YoungsModulus, heigthOfBuilding);
            var wall4 = new Wall(listOfPoints[5], listOfPoints[6], tWall, 'y', YoungsModulus, heigthOfBuilding);

            var walls = new List<Wall>();
            walls.Add(wall1);
            walls.Add(wall2);
            walls.Add(wall3);
            walls.Add(wall4);


            // Console.WriteLine("Number of Points: " + listOfPoints.Count);
            // Console.WriteLine("Number of Walls: " + walls.Count);

            var count = 0;
            foreach (var point in listOfPoints)
            {
                var coordinates = point.DisplayCoordinates();
                Console.WriteLine("Nr." + count + "(" + coordinates[0] + "," + coordinates[1] + ")");
                count++;
            }

            // for (int i = 0; i < walls.Count; i++)
            // {
            //     Console.WriteLine("Bending stiffness of wall {0}: {1}", i, walls[i].BendingStiffness());
            // }
            //
            // for (int i = 0; i < walls.Count; i++)
            // {
            //     Console.WriteLine("Shear stiffness of wall {0}: {1}", i, walls[i].ShearStiffness());
            // }
            //
            // for (int i = 0; i < walls.Count; i++)
            // {
            //     Console.WriteLine("Equivalent stiffness of wall {0}: {1}", i, walls[i].EquivalentStiffness());
            // }
            //
            // for (int i = 0; i < walls.Count; i++)
            // {
            //     
            //     var shearCoordinates = walls[i].CentreCoordinates();
            //
            //     Console.WriteLine("Coordinates of the center of wall {0}: ( {1} , {2} )", i, shearCoordinates[0], shearCoordinates[1]);
            // }
            //
            // for (int i = 0; i < walls.Count; i++)
            // {
            //     Console.WriteLine("Coordinate Stiffness Product of wall {0}: {1}", i, walls[i].CorStiffProduct());
            // }
            string elo = "elo elo";

            var shearOrdinates = building.ShearCentre(walls);

            double c = Math.Sqrt((length / 2 - shearOrdinates[0]) * (length / 2 - shearOrdinates[0]) +
                                 (width / 2 - shearOrdinates[1]) * (width / 2 - shearOrdinates[1]));

            Console.WriteLine("c: " +c);


            // Console.WriteLine("Y coordinate of the shear centre: " + shearOrdinates[0]);
            // Console.WriteLine("Z coordinate of the shear centre: " + shearOrdinates[1]);

            var Load = new Load(width, length, tFloor, gLoad, qLoad, walls, hFloor, tWall, columnCs,
                columnNr, floorNr);
            double verticalLoad = Load.GetVerticalLoad();
            //
            Console.WriteLine("Total vertical load equals: " + verticalLoad);
            //
            double sumTorionalMoment = building.SumTorsionalMoment(walls);
            double warpingAreaMoment = building.WarpingAreaMoment(walls);

            Console.WriteLine("Warping Area Moment = " + building.WarpingAreaMoment(walls));
            //
            // Console.WriteLine("Sum of Torsional Moment of inertia: " +building.SumTorsionalMoment(walls));
            //
            // Console.WriteLine("Sum Inertia moment Y: " + building.SumInertialMomentY(walls));
            // Console.WriteLine("Sum Inertia moment Z: " + building.SumInertialMomentZ(walls));

            double FvBBy = 7.8 * floorNr / (floorNr + 1.6) * 0.4 *
                (youngsModulusDesign * building.SumInertialMomentY(walls)) / (heigthOfBuilding * heigthOfBuilding);

            double FvBBz = 7.8 * floorNr / (floorNr + 1.6) * 0.4 *
                (youngsModulusDesign * building.SumInertialMomentZ(walls)) / (heigthOfBuilding * heigthOfBuilding);

            // Console.WriteLine("Buckling bending load Y: " + FvBBy);
            //
            // Console.WriteLine("Shear area Y: " + building.SumShearAreaY(walls));
            // Console.WriteLine("Shear area Z: " + building.SumShearAreaZ(walls));

            double FvBSy = shearModulusDesign * building.SumShearAreaY(walls);
            double FvBSz = shearModulusDesign * building.SumShearAreaZ(walls);

            double FVBy = FvBBy / (1 + FvBBy / FvBSy);
            double FVBz = FvBBz / (1 + FvBBz / FvBSz);

            Console.WriteLine("Translation in Z Direction: {0} <= {1} ", verticalLoad / 1e6, 0.1*FVBy);
            Console.WriteLine("Translation in Y Direction: {0} <= {1} ", verticalLoad / 1e6, 0.1 * FVBz);

            // double RotationL = 1 /
            //                    ((1 / heigthOfBuilding * heigthOfBuilding) * ((youngsModulusDesign * sumTorionalMoment) /
            //                                                                  (verticalLoad * d * d * c * c / 12)) +
            //                     (1 / 2.28) * Math.Sqrt((shearModulusDesign * sumTorionalMoment) /
            //                                            (verticalLoad * d * d * c * c / 12)));

            // double EF = (youngsModulusDesign * warpingAreaMoment/1e6) / (verticalLoad * ((d * d * c * c) / (12)));

            // double GF = Math.Sqrt((shearModulusDesign * sumTorionalMoment) / (verticalLoad * ((d * d * c * c) / (12))));

            // Console.WriteLine("EF = " + EF);
            // Console.WriteLine("GF = " + GF);


            double RotationL = 1 / (1 / (heigthOfBuilding * heigthOfBuilding) * (youngsModulusDesign * warpingAreaMoment / 1e6) / (verticalLoad * (d * d * c * c / 12)) + 1 / 2.28 * Math.Sqrt(shearModulusDesign * sumTorionalMoment / (verticalLoad * (d * d * c * c / 12))));

            Console.WriteLine("Left side rotation: " + RotationL);
        }
    }
}