from WallSegment import WallSegment
from Wall import Wall


class StructuralComponent:

    def __init__(self, segments: [WallSegment]):

        self.CalculateParameters(segments)

    def CalculateParameters(self, segments: [WallSegment]):

        #Area
        self.area = 0
        for segment in segments:
            self.area = self.area + segment.area

        #Center of mass
        self.area_momentY = 0
        self.area_momentZ = 0
        for segment in segments:
            self.area_momentY = self.area_momentY + segment.area * segment.centreYCor
            self.area_momentZ = self.area_momentZ + segment.area * segment.centreZCor

        self.centreYCor = self.area_momentY / self.area
        self.centreZCor = self.area_momentZ / self.area

        #Moment of Inertia
        self.inertia_moment_Y = 0
        self.inertia_moment_Z = 0
        for segment in segments:
            self.inertia_moment_Y = self.inertia_moment_Y + segment.momentOfInertiaY + segment.area * (segment.centreZCor - self.centreZCor)**2
            self.inertia_moment_Z = self.inertia_moment_Z + segment.momentOfInertiaZ + segment.area * (
                        segment.centreYCor - self.centreYCor) ** 2
        print("sum of momkents: ", self.inertia_moment_Y)

        #Inertia Product
        self.inertia_product = 0
        for segment in segments:
            self.inertia_product = self.inertia_product + segment.area * (self.centreYCor - segment.centreYCor) * (self.centreZCor - segment.centreZCor)


        # Shear center

        sum_coord_inertia_prodY = 0
        sum_coord_inertia_prodZ = 0
        sum_inertia_momentsY = 0
        sum_inertia_momentsZ = 0
        for segment in segments:
            sum_coord_inertia_prodY = sum_coord_inertia_prodY + segment.coord_inertia_productY
            sum_coord_inertia_prodZ = sum_coord_inertia_prodZ + segment.coord_inertia_productZ
            sum_inertia_momentsY = sum_inertia_momentsY + segment.momentOfInertiaY
            sum_inertia_momentsZ = sum_inertia_momentsZ + segment.momentOfInertiaZ

        self.shear_centreYCor = sum_coord_inertia_prodY / sum_inertia_momentsY
        self.shear_centreZCor = sum_coord_inertia_prodZ / sum_inertia_momentsZ


