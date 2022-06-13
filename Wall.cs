
namespace Master_Thesis;

class Wall
{
    private readonly double _endYCor;
    private readonly double _endZCor;
    private readonly double _centreYCor;
    private readonly double _centreZCor;
    private readonly char _orientation;
    private readonly double _bendingStiffness;
    private readonly double _shearStiffness;
    private double _shearArea;
    private double _momentOfInertia;
    private double _torsionalMoment;
    private double _shearCorrectionFactor = 0.8333333333;
    private double _equivalentStiffness;
    private double _corStiffProduct;
    private double _length;

    public Wall(Point A, Point B, double t, char o, double E, double L)
    {
        double shearArea;
        double momentOfInertia;
        double[] coordinatesA = A.DisplayCoordinates();
        double[] coordinatesB = B.DisplayCoordinates();

        var startYCor = coordinatesA[0];
        var startZCor = coordinatesA[1];
        _endYCor = coordinatesB[0];
        _endZCor = coordinatesB[1];
        var thickness = t;
        _orientation = o;
        var l = L;
        var gModulus = E / (2 * (1 + 0.2));

        // Coordinates of the wall's centre
        _centreYCor = startYCor + (_endYCor - startYCor) / 2;
        _centreZCor = startZCor + (_endZCor - startZCor) / 2;

        // Length of the wall
        if (_orientation == 'y')
            _length += (_endYCor - startYCor);

        else if (_orientation == 'z')
            _length += (_endZCor - startZCor);

        else
            throw new Exception("Invalid direction of the wall");

        // Second Moment of Inertia
        if (_orientation == 'y')
        {
            momentOfInertia = thickness * ((_endYCor - startYCor) * (_endYCor - startYCor) * (_endYCor - startYCor)) / 12;
        }
        else if (_orientation == 'z')
        {
            momentOfInertia = thickness * ((_endZCor - startZCor) * (_endZCor - startZCor) * (_endZCor - startZCor)) / 12;
        }
        else
        {
            throw new Exception("Invalid direction of the wall");
        }

        _momentOfInertia = momentOfInertia;

        // Bending Stiffness
        _bendingStiffness = (3 * E * momentOfInertia) / (l * l * l);

        // Shear Area
        if (_orientation == 'y')
            shearArea = (_endYCor - startYCor) * thickness * _shearCorrectionFactor;

        else if (_orientation == 'z')
            shearArea = (_endZCor - startZCor) * thickness * _shearCorrectionFactor;

        else
            throw new Exception("Invalid direction of the wall");

        _shearArea = shearArea;

        // Shear Stiffness
        _shearStiffness = (gModulus * shearArea) / l;

        // Equivalent Stiffness
        _equivalentStiffness = (_bendingStiffness * _shearStiffness) / (_bendingStiffness + _shearStiffness);

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

    // public double BendingStiffness()
    // {
    //     return _bendingStiffness;
    // }
    //
    // public double ShearStiffness()
    // {
    //     return _shearStiffness;
    // }

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

    // public double[] EndCoordinates()
    // {
    //     double[] endCoordinates = new double[2];
    //     endCoordinates[0] = _endYCor;
    //     endCoordinates[1] = _endZCor;
    //     return endCoordinates;
    // }

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