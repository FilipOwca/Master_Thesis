


class FreeFormBuilding:

    def ShearCenter(self, components):

        products = self.SumsInertiaProducts(components)
        sums = self.SumsInertiaMoments(components)
        print("products: ", products)
        print("sums: ", sums)

        y0 = ((products[0] - products[3]) * (sums[1]) - (products[1] - products[2]) * (sums[2])) / (sums[0] * sums[1] - sums[2]**2)
        z0 = ((products[0] - products[3]) * (sums[2]) - (products[1] - products[2]) * (sums[0])) / (sums[0] * sums[1] - sums[2]**2)

        shear_center_coordinates = [y0, z0]
        return shear_center_coordinates

    def SumsInertiaMoments(self, components):

        sum_inertia_momentY = 0
        sum_inertia_momentZ = 0
        sum_inertia_product = 0
        for component in components:
            sum_inertia_momentY = sum_inertia_momentY + component.inertia_moment_Y
            sum_inertia_momentZ = sum_inertia_momentZ + component.inertia_moment_Z
            sum_inertia_product = sum_inertia_product + component.inertia_product

        sums = [sum_inertia_momentY, sum_inertia_momentZ, sum_inertia_product]
        return sums

    def SumsInertiaProducts(self, components):

        sum_Iy_product_y0 = 0
        sum_Iyz_product_y0 = 0
        sum_Iz_product_z0 = 0
        sum_Iyz_product_z0 = 0
        for component in components:
            sum_Iy_product_y0 =  sum_Iy_product_y0 + component.inertia_moment_Y * component.shear_centreYCor
            sum_Iyz_product_y0 = sum_Iyz_product_y0 + component.inertia_product * component.shear_centreYCor
            sum_Iz_product_z0 = sum_Iz_product_z0 + component.inertia_moment_Z * component.shear_centreZCor
            sum_Iyz_product_z0 = sum_Iyz_product_z0 + component.inertia_product * component.shear_centreZCor

        products = [sum_Iy_product_y0, sum_Iyz_product_y0, sum_Iz_product_z0, sum_Iyz_product_z0]
        return products