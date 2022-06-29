
namespace Master_Thesis;

class Building
{
    // Physical parameters of the bracing system (walls' layout)
    private double _sumeEqlStiffinY;
    private double _sumeEqlStiffinZ;
    private double _sumeCorStiffProdinY;
    private double _sumeCorStiffProdinZ;
    private double _shearCentreCoordinateY;
    private double _shearCentreCoordinateZ;
    
    // Finding the Shear Center of the bracing system related to the given walls
    public double[] ShearCentre(List<Wall> walls)
    {
        var wallsY = new List<double>();
        var wallsZ = new List<double>();
        SplittingWalls(walls, wallsY, wallsZ);

        // Summing up EquivalentStiffness and CorStiffProduct of each wall in 2 directions separately
        SummingUpStiffness(wallsY, wallsZ);

        // Finding coordinates of the bracing system's shear center
        double[] shearCentreCoordinates = new double[2];
        shearCentreCoordinates[0] = _sumeCorStiffProdinZ / _sumeEqlStiffinZ;
        shearCentreCoordinates[1] = _sumeCorStiffProdinY / _sumeEqlStiffinY;
        _shearCentreCoordinateY = shearCentreCoordinates[0];
        _shearCentreCoordinateZ = shearCentreCoordinates[1];
        return shearCentreCoordinates;
    }

    // Splitting list of walls into 2 groups: 1) in Y direction (horizontal) and 2) in Z direction (vertical). In each list even members contain EquivalentStiffness of following walls and odd members contain CorStiffProduct of following walls.
    private void SummingUpStiffness(IReadOnlyList<double> wallsY, List<double> wallsZ)
    {
        for (int i = 0; i < wallsY.Count; i++)
        {
            if (i % 2 == 0)
                _sumeEqlStiffinY += wallsY[i];
            else
                _sumeCorStiffProdinY += wallsY[i];
        }

        for (int i = 0; i < wallsZ.Count; i++)
        {
            if (i % 2 == 0)
                _sumeEqlStiffinZ += wallsZ[i];
            else
                _sumeCorStiffProdinZ += wallsZ[i];
        }
    }

    private void SplittingWalls(IReadOnlyList<Wall> walls, List<double> wallsY, List<double> wallsZ)
    {
        foreach (Wall wall in walls)
        {
            if (wall.Orientation == 'y')
            {
                wallsY.Add(wall.EquivalentStiffness);
                wallsY.Add(wall.CorStiffProduct);
            }
            else
            {
                wallsZ.Add(wall.EquivalentStiffness);
                wallsZ.Add(wall.CorStiffProduct);
            }
        }
    }

    // Finding the warping area moment of the bracing system
    public double WarpingAreaMoment(IReadOnlyList<Wall> walls)
    {
        double warpingAreaMoment = 0;
        foreach (var wall in walls)
        {
            var distanceY = wall.CentreCoordinates()[0] - _shearCentreCoordinateY;
            var distanceZ = wall.CentreCoordinates()[1] - _shearCentreCoordinateZ;
    
            if (wall.Orientation == 'y')
            {
                warpingAreaMoment += distanceZ * distanceZ * wall.EquivalentStiffness;
            }
            else
            {
                warpingAreaMoment += distanceY * distanceY * wall.EquivalentStiffness;
            }
        }
        return warpingAreaMoment;
    }
  
    // Summing up torsional moment of all walls
    public double SumTorsionalMoment(IReadOnlyList<Wall> walls)
    {
        double sumTorsionalMoment = 0;
    
        foreach (var wall in walls)
        {
            sumTorsionalMoment += wall.TorsionalMoment;
        }
        return sumTorsionalMoment;
    }

    // Summing up moment of inertia of each wall in Y direction (horizontal)
    public double SumInertialMomentY(IReadOnlyList<Wall> walls)
    {
        double sumInertiaMomentY = 0;

        foreach (var wall in walls)
        {
            if (wall.Orientation == 'z')
            {
                sumInertiaMomentY += wall.InertiaMoment;
            }
        }
        return sumInertiaMomentY;
    }

    // Summing up moment of inertia of each wall in Z direction (vertical)
    public double SumInertialMomentZ(IReadOnlyList<Wall> walls)
    {
        double sumInertiaMomentZ = 0;
        foreach (var wall in walls)
        {
            if (wall.Orientation == 'y')
            {
                sumInertiaMomentZ += wall.InertiaMoment;
            }
        }
        return sumInertiaMomentZ;
    }

    // Summing up shear are  of each wall in Y direction (horizontal)
    public double SumShearAreaY(IReadOnlyList<Wall> walls)
    {
        double sumShearAreaY = 0;
        foreach (var wall in walls)
        {
            if (wall.Orientation == 'z')
            {
                sumShearAreaY += wall.ShearArea;
            }
        }
        return sumShearAreaY;
    }

    // Summing up shear are  of each wall in Z direction (vertical)
    public double SumShearAreaZ(IReadOnlyList<Wall> walls)
    {
        double sumShearAreaZ = 0;
        foreach (var wall in walls)
        {
            if (wall.Orientation == 'y')
            {
                sumShearAreaZ += wall.ShearArea;
            }
        }
        return sumShearAreaZ;
    }



}
