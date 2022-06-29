
namespace Master_Thesis;

class Wall
{
    // Geometrical and physical parameters of each instance of the class Wall.
    private double _centreYCor;
    private double _centreZCor;

    const double tWall = 0.3;
    const double heightOfBuilding = 12;
    const double youngModulus = 33000000000;
    private const double ShearCorrectionFactor = 0.8333333333;

    // Constructing an instance of the class Wall and calculating its geometrical and physical parameters
    public Wall(Point a, Point b)
    {
        CalculateParameters(a, b);
    }

    private void CalculateParameters(Point a, Point b)
    {
        // Assigning parameters of a wall
        var gModulus = youngModulus / (2 * (1 + 0.2));
        
        // Calling coordinates of the wall's beginning and end from the Point class
        var startYCor = a.DisplayCoordinates()[0];
        var startZCor = a.DisplayCoordinates()[1];
        var endYCor = b.DisplayCoordinates()[0];
        var endZCor = b.DisplayCoordinates()[1];

        // Finding the orientation of the wall's main axis
        if (startYCor - endYCor == 0)
            Orientation = 'z';
        else
            Orientation = 'y';

        // Coordinates of the wall's centre
        _centreYCor = startYCor + (endYCor - startYCor) / 2;
        _centreZCor = startZCor + (endZCor - startZCor) / 2;

        // Length of the wall
        if (Orientation == 'y')
            Length = (endYCor - startYCor);

        else if (Orientation == 'z')
            Length = (endZCor - startZCor);
        else
            throw new Exception("Invalid direction of the wall");

        // Second Moment of Inertia
        double momentOfInertia;
        if (Orientation == 'y')
        {
            momentOfInertia = tWall * ((endYCor - startYCor) * (endYCor - startYCor) * (endYCor - startYCor)) / 12;
        }
        else if (Orientation == 'z')
        {
            momentOfInertia = tWall * ((endZCor - startZCor) * (endZCor - startZCor) * (endZCor - startZCor)) / 12;
        }
        else
        {
            throw new Exception("Invalid direction of the wall");
        }

        InertiaMoment = momentOfInertia;

        // Bending Stiffness
        var bendingStiffness = (3 * youngModulus * momentOfInertia) / (heightOfBuilding * heightOfBuilding * heightOfBuilding);

        // Shear Area
        double shearArea;
        if (Orientation == 'y')
            shearArea = (endYCor - startYCor) * tWall * ShearCorrectionFactor;

        else if (Orientation == 'z')
            shearArea = (endZCor - startZCor) * tWall * ShearCorrectionFactor;

        else
            throw new Exception("Invalid direction of the wall");
        ShearArea = shearArea;

        // Shear Stiffness
        var shearStiffness = (gModulus * shearArea) / heightOfBuilding;

        // Equivalent Stiffness
        EquivalentStiffness = (bendingStiffness * shearStiffness) / (bendingStiffness + shearStiffness);

        // Product of centre coordinates and equivalent stiffness
        if (Orientation == 'y')
            CorStiffProduct = EquivalentStiffness * _centreZCor;

        else if (Orientation == 'z')
            CorStiffProduct = EquivalentStiffness * _centreYCor;

        else
            throw new Exception("Invalid direction of the wall");

        // Torsional Moment of Inertia
        TorsionalMoment = 0.323 * Length * tWall * tWall * tWall;
    }

    // Following methods are used to call each parameters of a wall separately
    public double EquivalentStiffness { get; private set; }
    public char Orientation { get; private set; }
    public double CorStiffProduct { get; private set; }
    public double Length { get; private set; }
    public double TorsionalMoment { get; private set; }
    public double InertiaMoment { get; private set; }
    public double ShearArea { get; private set; }

    public double[] CentreCoordinates()
    {
        double[] shearCentreCoordinates = new double[2];
        shearCentreCoordinates[0] = _centreYCor;
        shearCentreCoordinates[1] = _centreZCor;
        return shearCentreCoordinates;
    }

    
}