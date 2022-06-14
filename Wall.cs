
namespace Master_Thesis;

class Wall
{
    // Geometrical and physical parameters of each instance of the class Wall.
    private readonly double _centreYCor;
    private readonly double _centreZCor;
    private readonly double _length;
    private readonly char _orientation;
    private readonly double _shearArea;
    private readonly double _momentOfInertia;
    private readonly double _torsionalMoment;
    private const double _shearCorrectionFactor = 0.8333333333;
    private readonly double _equivalentStiffness;
    private readonly double _corStiffProduct;

    // Constructing an instance of the class Wall and calculating its geometrical and physical parameters
    public Wall(Point A, Point B, double t, char o, double E, double heigth)
    {
        // Assigning parameters of a wall
        var thickness = t;
        _orientation = o;
        var heigthWall = heigth;
        var gModulus = E / (2 * (1 + 0.2));

        // Calling coordinates of the wall's beginning and end from the Point class
        var startYCor = A.DisplayCoordinates()[0];
        var startZCor = A.DisplayCoordinates()[1];
        var endYCor = B.DisplayCoordinates()[0];
        var endZCor = B.DisplayCoordinates()[1];
        
        // Coordinates of the wall's centre
        _centreYCor = startYCor + (endYCor - startYCor) / 2;
        _centreZCor = startZCor + (endZCor - startZCor) / 2;

        // Length of the wall
        if (_orientation == 'y')
            _length += (endYCor - startYCor);

        else if (_orientation == 'z')
            _length += (endZCor - startZCor);
        else
            throw new Exception("Invalid direction of the wall");

        // Second Moment of Inertia
        double momentOfInertia;
        if (_orientation == 'y')
        {
            momentOfInertia = thickness * ((endYCor - startYCor) * (endYCor - startYCor) * (endYCor - startYCor)) / 12;
        }
        else if (_orientation == 'z')
        {
            momentOfInertia = thickness * ((endZCor - startZCor) * (endZCor - startZCor) * (endZCor - startZCor)) / 12;
        }
        else
        {
            throw new Exception("Invalid direction of the wall");
        }
        _momentOfInertia = momentOfInertia;

        // Bending Stiffness
        var bendingStiffness = (3 * E * momentOfInertia) / (heigthWall * heigthWall * heigthWall);

        // Shear Area
        double shearArea;
        if (_orientation == 'y')
            shearArea = (endYCor - startYCor) * thickness * _shearCorrectionFactor;

        else if (_orientation == 'z')
            shearArea = (endZCor - startZCor) * thickness * _shearCorrectionFactor;

        else
            throw new Exception("Invalid direction of the wall");
        _shearArea = shearArea;

        // Shear Stiffness
        var shearStiffness = (gModulus * shearArea) / heigthWall;

        // Equivalent Stiffness
        _equivalentStiffness = (bendingStiffness * shearStiffness) / (bendingStiffness + shearStiffness);

        // Product of centre coordinates and equivalent stiffness
        if (_orientation == 'y')
            _corStiffProduct = _equivalentStiffness * _centreZCor;

        else if (_orientation == 'z')
            _corStiffProduct = _equivalentStiffness * _centreYCor;

        else
            throw new Exception("Invalid direction of the wall");

        // Torsional Moment of Inertia
        _torsionalMoment = 0.323 * _length * thickness * thickness * thickness;
    }

    // Following methods are used to call each parameters of a wall separately
    public double EquivalentStiffness()
    {
        return _equivalentStiffness;
    }

    public char Orientation()
    {
        return _orientation;
    }

    public double CorStiffProduct()
    {
        return _corStiffProduct;
    }

    public double[] CentreCoordinates()
    {
        double[] shearCentreCoordinates = new double[2];
        shearCentreCoordinates[0] = _centreYCor;
        shearCentreCoordinates[1] = _centreZCor;
        return shearCentreCoordinates;
    }

    public double Length()
    {
        return _length;
    }

    public double TorsionalMoment()
    {
        return _torsionalMoment;
    }

    public double InertiaMoment()
    {
        return _momentOfInertia;
    }

    public double ShearArea()
    {
        return _shearArea;
    }
}