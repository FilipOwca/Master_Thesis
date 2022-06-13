
namespace Master_Thesis;

class Building
{
    private double _sumeEqlStiffinY;
    private double _sumeEqlStiffinZ;
    private double _sumeCorStiffProdinY;
    private double _sumeCorStiffProdinZ;
    private double _shearCentreCoordinateY;
    private double _shearCentreCoordinateZ;

    public Building(int length, int width)
    {

    }

    public double[] ShearCentre(List<Wall> walls)
    {
        var wallsY = new List<double>();
        var wallsZ = new List<double>();
    
        foreach (Wall wall in walls)
        {
            if (wall.Orientation() == 'y')
            {
                wallsY.Add(wall.EquivalentStiffness());
                wallsY.Add(wall.CorStiffProduct());
            }
            else
            {
                wallsZ.Add(wall.EquivalentStiffness());
                wallsZ.Add(wall.CorStiffProduct());
            }
        }

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
        //
        // Console.WriteLine("The sume of Eql Stiff in Y direction: " + _sumeEqlStiffinY);
        // Console.WriteLine("The sume of Coordinate and Stiffness Product in Y direction: " + _sumeCorStiffProdinY);
        // Console.WriteLine("The sume of Eql Stiff in Z direction: " + _sumeEqlStiffinZ);
        // Console.WriteLine("The sume of Coordinate and Stiffness Product in Z direction: " + _sumeCorStiffProdinZ);

        double[] shearCentreCoordinates = new double[2];
        shearCentreCoordinates[0] = _sumeCorStiffProdinZ / _sumeEqlStiffinZ;
        shearCentreCoordinates[1] = _sumeCorStiffProdinY / _sumeEqlStiffinY;
        _shearCentreCoordinateY = shearCentreCoordinates[0];
        _shearCentreCoordinateZ = shearCentreCoordinates[1];

        return shearCentreCoordinates;
    }


    public double WarpingAreaMoment(List<Wall> walls)
    {
        double warpingAreaMoment = 0;
    
        foreach (var wall in walls)
        {
            double distanceY;
            double distanceZ;
    
            distanceY = wall.CentreCoordinates()[0] - _shearCentreCoordinateY;
            distanceZ = wall.CentreCoordinates()[1] - _shearCentreCoordinateZ;
    
            if (wall.Orientation() == 'y')
            {
                warpingAreaMoment += distanceZ * distanceZ * wall.EquivalentStiffness();
            }
            else
            {
                warpingAreaMoment += distanceY * distanceY * wall.EquivalentStiffness();
            }
    
        }
    
        return warpingAreaMoment;
    }
    // public double GetSumeEqlStiffinY()
    // {
    //     return _sumeEqlStiffinY;
    // }
    //
    // public double GetSumeEqlStiffinZ()
    // {
    //     return _sumeEqlStiffinZ;
    // }
    // public double GetSumeCorStiffProdinY()
    // {
    //     return _sumeCorStiffProdinY;
    // }
    //
    // public double GetSumeCorStiffProdinZ()
    // {
    //     return _sumeCorStiffProdinZ;
    // }
    //
    public double SumTorsionalMoment(List<Wall> walls)
    {
        double sumTorsionalMoment = 0;
    
        foreach (var wall in walls)
        {
            sumTorsionalMoment += wall.TorsionalMoment();
        }
        return sumTorsionalMoment;
    }

    public double SumInertialMomentY(List<Wall> walls)
    {
        double sumInertiaMomentY = 0;

        foreach (var wall in walls)
        {
            if (wall.Orientation() == 'z')
            {
                sumInertiaMomentY += wall.InertiaMoment();
            }
        }
        return sumInertiaMomentY;
    }

    public double SumInertialMomentZ(List<Wall> walls)
    {
        double sumInertiaMomentZ = 0;

        foreach (var wall in walls)
        {
            if (wall.Orientation() == 'y')
            {
                sumInertiaMomentZ += wall.InertiaMoment();
            }
        }
        return sumInertiaMomentZ;
    }

    public double SumShearAreaY(List<Wall> walls)
    {
        double sumShearAreaY = 0;

        foreach (var wall in walls)
        {
            if (wall.Orientation() == 'z')
            {
                sumShearAreaY += wall.ShearArea();
            }
        }
        return sumShearAreaY;
    }

    public double SumShearAreaZ(List<Wall> walls)
    {
        double sumShearAreaZ = 0;

        foreach (var wall in walls)
        {
            if (wall.Orientation() == 'y')
            {
                sumShearAreaZ += wall.ShearArea();
            }
        }
        return sumShearAreaZ;
    }



}
