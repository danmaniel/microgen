import os
import math
from numpy import cos, sin, pi, abs
import pygalmesh


class Custom(pygalmesh.DomainBase):
    def __init__(self, rve, function, h):
        super().__init__()
        self.h = h
        self.z0 = 0.0
        self.z1 = rve.dz
        self.waist_radius = math.sqrt((0.5 * rve.dx) ** 2 + (0.5 * rve.dy) ** 2)
        self.bounding_sphere_squared_radius = math.sqrt((0.5 * rve.dx) ** 2 +
                                                        (0.5 * rve.dy) ** 2 +
                                                        (0.5 * rve.dz) ** 2) * 1.1
        self.function = function # "cos(2*pi*x) + cos(2*pi*y) + cos(2*pi*z)"

    def get_bounding_sphere_squared_radius(self):
        return self.bounding_sphere_squared_radius

    def eval(self, pos):
        x = pos[0]
        y = pos[1]
        z = pos[2]
        return eval(self.function) + self.h
class Hyperboloid(pygalmesh.DomainBase):
    def __init__(self, max_edge_size_at_feature_edges):
        super().__init__()
        self.z0 = -1.0
        self.z1 = 1.0
        self.waist_radius = 0.5
        self.max_edge_size_at_feature_edges = max_edge_size_at_feature_edges

    def eval(self, x):
        if self.z0 < x[2] and x[2] < self.z1:
            return x[0] ** 2 + x[1] ** 2 - (x[2] ** 2 + self.waist_radius) ** 2
        return 1.0

    def get_bounding_sphere_squared_radius(self):
        z_max = max(abs(self.z0), abs(self.z1))
        r_max = z_max**2 + self.waist_radius
        return r_max * r_max + z_max * z_max

    def getFeatures(self):
        radius0 = self.z0**2 + self.waist_radius
        n0 = int(2 * pi * radius0 / self.max_edge_size_at_feature_edges)
        circ0 = [
            [
                radius0 * cos((2 * pi * k) / n0),
                radius0 * sin((2 * pi * k) / n0),
                self.z0,
            ]
            for k in range(n0)
        ]
        circ0.append(circ0[0])

        radius1 = self.z1**2 + self.waist_radius
        n1 = int(2 * pi * radius1 / self.max_edge_size_at_feature_edges)
        circ1 = [
            [
                radius1 * cos((2 * pi * k) / n1),
                radius1 * sin((2 * pi * k) / n1),
                self.z1,
            ]
            for k in range(n1)
        ]
        circ1.append(circ1[0])
        return [circ0, circ1]


class SchwarzP(pygalmesh.DomainBase):
    def __init__(self, rve, h):
        super().__init__()
        self.h = h
        self.z0 = 0.0
        self.z1 = rve.dz
        self.waist_radius = math.sqrt((0.5 * rve.dx) ** 2 + (0.5 * rve.dy) ** 2)
        self.bounding_sphere_squared_radius = math.sqrt((0.5 * rve.dx) ** 2 +
                                                        (0.5 * rve.dy) ** 2 +
                                                        (0.5 * rve.dz) ** 2) * 1.1

    def get_bounding_sphere_squared_radius(self):
        return self.bounding_sphere_squared_radius

    def eval(self, x):
        x2 = cos(x[0] * 2 * pi)
        y2 = cos(x[1] * 2 * pi)
        z2 = cos(x[2] * 2 * pi)
        return x2 + y2 + z2 + self.h


class SchwarzD(pygalmesh.DomainBase):
    def __init__(self, rve, h):
        super().__init__()
        self.h = h
        self.z0 = 0.0
        self.z1 = rve.dz
        self.waist_radius = math.sqrt((0.5 * rve.dx) ** 2 + (0.5 * rve.dy) ** 2)
        self.bounding_sphere_squared_radius = math.sqrt((0.5 * rve.dx) ** 2 +
                                                        (0.5 * rve.dy) ** 2 +
                                                        (0.5 * rve.dz) ** 2) * 1.1

    def get_bounding_sphere_squared_radius(self):
        return self.bounding_sphere_squared_radius

    def eval(self, x):
        a = (
            sin(x[0] * 2 * pi)
            * sin(x[1] * 2 * pi)
            * sin(x[2] * 2 * pi)
        )
        b = (
            sin(x[0] * 2 * pi)
            * cos(x[1] * 2 * pi)
            * cos(x[2] * 2 * pi)
        )
        c = (
            cos(x[0] * 2 * pi)
            * sin(x[1] * 2 * pi)
            * cos(x[2] * 2 * pi)
        )
        d = (
            cos(x[0] * 2 * pi)
            * cos(x[1] * 2 * pi)
            * sin(x[2] * 2 * pi)
        )
        return a + b + c + d + self.h


class Neovius(pygalmesh.DomainBase):
    def __init__(self, rve, h):
        super().__init__()
        self.h = h
        self.z0 = 0.0
        self.z1 = rve.dz
        self.waist_radius = math.sqrt((0.5 * rve.dx) ** 2 + (0.5 * rve.dy) ** 2)
        self.bounding_sphere_squared_radius = math.sqrt((0.5 * rve.dx) ** 2 +
                                                        (0.5 * rve.dy) ** 2 +
                                                        (0.5 * rve.dz) ** 2) * 1.1

    def get_bounding_sphere_squared_radius(self):
        return self.bounding_sphere_squared_radius

    def eval(self, x):
        a = 3.0 * (
            cos(x[0] * 2 * pi)
            + cos(x[1] * 2 * pi)
            + cos(x[2] * 2 * pi)
        )
        b = 4.0 * (
            cos(x[0] * 2 * pi)
            * cos(x[1] * 2 * pi)
            * cos(x[2] * 2 * pi)
        )
        return a + b + self.h

class SchoenIWP(pygalmesh.DomainBase):
    def __init__(self, rve, h):
        super().__init__()
        self.h = h
        self.z0 = 0.0
        self.z1 = rve.dz
        self.waist_radius = math.sqrt((0.5 * rve.dx) ** 2 + (0.5 * rve.dy) ** 2)
        self.bounding_sphere_squared_radius = math.sqrt((0.5 * rve.dx) ** 2 +
                                                        (0.5 * rve.dy) ** 2 +
                                                        (0.5 * rve.dz) ** 2) * 1.1

    def get_bounding_sphere_squared_radius(self):
        return self.bounding_sphere_squared_radius

    def eval(self, x):
        l = 2 * ((cos(x[0] * 2 * pi)
            * cos(x[1] * 2 * pi)) +
            (cos(x[1] * 2 * pi)
			* cos(x[2] * 2 * pi)) +
			(cos(x[2] * 2 * pi)
			* cos(x[0] * 2 * pi)) 
        )
        m = (cos(x[0] * 4 * pi) +
            cos(x[1] * 4 * pi) +
            cos(x[2] * 4 * pi)
        )
        return l - m + self.h
    
class SchoenFRD(pygalmesh.DomainBase):
    def __init__(self, rve, h):
        super().__init__()
        self.h = h
        self.z0 = 0.0
        self.z1 = rve.dz
        self.waist_radius = math.sqrt((0.5 * rve.dx) ** 2 + (0.5 * rve.dy) ** 2)
        self.bounding_sphere_squared_radius = math.sqrt((0.5 * rve.dx) ** 2 +
                                                        (0.5 * rve.dy) ** 2 +
                                                        (0.5 * rve.dz) ** 2) * 1.1

    def get_bounding_sphere_squared_radius(self):
        return self.bounding_sphere_squared_radius

    def eval(self, x):
        a = 4 * ((cos(x[0] * 2 * pi) *
                  cos(x[1] * 2 * pi) *
                  cos(x[2] * 2 * pi))
                )
        b = ((cos(x[0] * 4 * pi) * cos(x[1] * 4 * pi)) +
             (cos(x[1] * 4 * pi) * cos(x[2] * 4 * pi)) +
             (cos(x[2] * 4 * pi) * cos(x[0] * 4 * pi))
            )
        return a - b + self.h
    
class FischerKochS(pygalmesh.DomainBase):
    def __init__(self, rve, h):
        super().__init__()
        self.h = h
        self.z0 = 0.0
        self.z1 = rve.dz
        self.waist_radius = math.sqrt((0.5 * rve.dx) ** 2 + (0.5 * rve.dy) ** 2)
        self.bounding_sphere_squared_radius = math.sqrt((0.5 * rve.dx) ** 2 +
                                                        (0.5 * rve.dy) ** 2 +
                                                        (0.5 * rve.dz) ** 2) * 1.1

    def get_bounding_sphere_squared_radius(self):
        return self.bounding_sphere_squared_radius

    def eval(self, x):
        a = (cos(x[0] * 4 * pi) *
             sin(x[1] * 2 * pi) *
             cos(x[2] * 2 * pi)
            )
        b = (cos(x[0] * 2 * pi) *
             cos(x[1] * 4 * pi) *
             sin(x[2] * 2 * pi)
            )
        c = (sin(x[0] * 2 * pi) *
             cos(x[1] * 2 * pi) *
             cos(x[2] * 4 * pi)
            )
        return a + b + c + self.h
    
class PMY(pygalmesh.DomainBase):
    def __init__(self, rve, h):
        super().__init__()
        self.h = h
        self.z0 = 0.0
        self.z1 = rve.dz
        self.waist_radius = math.sqrt((0.5 * rve.dx) ** 2 + (0.5 * rve.dy) ** 2)
        self.bounding_sphere_squared_radius = math.sqrt((0.5 * rve.dx) ** 2 +
                                                        (0.5 * rve.dy) ** 2 +
                                                        (0.5 * rve.dz) ** 2) * 1.1

    def get_bounding_sphere_squared_radius(self):
        return self.bounding_sphere_squared_radius

    def eval(self, x):
        a = 2 * ((cos(x[0] * 2 * pi) *
                  cos(x[1] * 2 * pi) *
                  cos(x[2] * 2 * pi))
                )
        b = (sin(x[0] * 4 * pi) *
             sin(x[1] * 2 * pi)
            ) 
        c = (sin(x[0] * 2 * pi) *
             sin(x[2] * 4 * pi)
            )
        d = (sin(x[1] * 4 * pi) *
             sin(x[2] * 2 * pi)
            )
        return a + b + c + d + self.h
    
class HoneyComb(pygalmesh.DomainBase):
    def __init__(self, rve, h):
        super().__init__()
        self.h = h
        self.z0 = 0.0
        self.z1 = rve.dz
        self.waist_radius = math.sqrt((0.5 * rve.dx) ** 2 + (0.5 * rve.dy) ** 2)
        self.bounding_sphere_squared_radius = math.sqrt((0.5 * rve.dx) ** 2 +
                                                        (0.5 * rve.dy) ** 2 +
                                                        (0.5 * rve.dz) ** 2) * 1.1

    def get_bounding_sphere_squared_radius(self):
        return self.bounding_sphere_squared_radius

    def eval(self, x):
        a = sin(x[0] * 2 * pi) * cos(x[1] * 2 * pi)
        b = sin(x[1] * 2 * pi)
        c = cos(x[2] * 2 * pi)
        return a + b + c + self.h
        
class Gyroid(pygalmesh.DomainBase):
    def __init__(self, rve, h):
        super().__init__()
        self.h = h
        self.z0 = 0.0
        self.z1 = rve.dz
        self.waist_radius = math.sqrt((0.5 * rve.dx) ** 2 + (0.5 * rve.dy) ** 2)
        self.bounding_sphere_squared_radius = math.sqrt((0.5 * rve.dx) ** 2 +
                                                        (0.5 * rve.dy) ** 2 +
                                                        (0.5 * rve.dz) ** 2) * 1.1

    def get_bounding_sphere_squared_radius(self):
        return self.bounding_sphere_squared_radius

    def eval(self, x):
        x2 = sin(x[0] * 2 * pi) * cos(x[1] * 2 * pi)
        y2 = sin(x[1] * 2 * pi) * cos(x[2] * 2 * pi)
        z2 = sin(x[2] * 2 * pi) * cos(x[0] * 2 * pi)
        if abs(x[0]) + abs(x[1]) + abs(x[2]) > 1.0e-8:
            return x2 + y2 + z2 + self.h
        else:
            return 1.0


def generateTPMS(
    type_tpms,
    thickness,
    rve,
    sizeMesh=0.05,
    minFacetAngle=10.0,
    maxRadius=0.05,
    path_data="",
    function=""
):

    thickness = thickness * pi

    if type_tpms == "custom":
        s_testplus = Custom(rve, function, thickness / 4.0)
        s_testminus = Custom(rve, function, -thickness / 4.0)
        s_plus = Custom(rve, function, thickness / 2.0)
        s_minus = Custom(rve, function, -1.0 * thickness / 2.0)  
    elif type_tpms == "honeycomb":
        s_testplus = HoneyComb(rve, thickness / 4.0)
        s_testminus = HoneyComb(rve, -thickness / 4.0)
        s_plus = HoneyComb(rve, thickness / 2.0)
        s_minus = HoneyComb(rve, -1.0 * thickness / 2.0)    
    elif type_tpms == "gyroid":
        s_testplus = Gyroid(rve, thickness / 4.0)
        s_testminus = Gyroid(rve, -thickness / 4.0)
        s_plus = Gyroid(rve, thickness / 2.0)
        s_minus = Gyroid(rve, -1.0 * thickness / 2.0)
    elif type_tpms == "schwarzP":
        s_testplus = SchwarzP(rve, thickness / 4.0)
        s_testminus = SchwarzP(rve, -thickness / 4.0)
        s_plus = SchwarzP(rve, thickness / 2.0)
        s_minus = SchwarzP(rve, -1.0 * thickness / 2.0)
    elif type_tpms == "schwarzD":
        s_testplus = SchwarzD(rve, thickness / 4.0)
        s_testminus = SchwarzD(rve, -thickness / 4.0)
        s_plus = SchwarzD(rve, thickness / 2.0)
        s_minus = SchwarzD(rve, -1.0 * thickness / 2.0)
    elif type_tpms == "neovius":
        s_testplus = Neovius(rve, thickness / 4.0)
        s_testminus = Neovius(rve, -thickness / 4.0)
        s_plus = Neovius(rve, thickness / 2.0)
        s_minus = Neovius(rve, -1.0 * thickness / 2.0)
    elif type_tpms == "schoenIWP":
        s_testplus = SchoenIWP(rve, thickness / 4.0)
        s_testminus = SchoenIWP(rve, -thickness / 4.0)
        s_plus = SchoenIWP(rve, thickness / 2.0)
        s_minus = SchoenIWP(rve, -1.0 * thickness / 2.0)
    elif type_tpms == "schoenFRD":
        s_testplus = SchoenFRD(rve, thickness / 4.0)
        s_testminus = SchoenFRD(rve, -thickness / 4.0)
        s_plus = SchoenFRD(rve, thickness / 2.0)
        s_minus = SchoenFRD(rve, -1.0 * thickness / 2.0)
    elif type_tpms == "fischerKochS":
        s_testplus = FischerKochS(rve, thickness / 4.0)
        s_testminus = FischerKochS(rve, -thickness / 4.0)
        s_plus = FischerKochS(rve, thickness / 2.0)
        s_minus = FischerKochS(rve, -1.0 * thickness / 2.0)
    elif type_tpms == "pmy":
        s_testplus = PMY(rve, thickness / 4.0)
        s_testminus = PMY(rve, -thickness / 4.0)
        s_plus = PMY(rve, thickness / 2.0)
        s_minus = PMY(rve, -1.0 * thickness / 2.0)
    else:
        print("Error, the tpms is not recognized")
        return False

    mesh_surf_testplus = pygalmesh.generate_surface_mesh(
        s_testplus,
        min_facet_angle=minFacetAngle,
        max_radius_surface_delaunay_ball=maxRadius,
        max_facet_distance=sizeMesh,
    )

    mesh_surf_testminus = pygalmesh.generate_surface_mesh(
        s_testminus,
        min_facet_angle=minFacetAngle,
        max_radius_surface_delaunay_ball=maxRadius,
        max_facet_distance=sizeMesh,
    )

    mesh_surf_plus = pygalmesh.generate_surface_mesh(
        s_plus,
        min_facet_angle=minFacetAngle,
        max_radius_surface_delaunay_ball=maxRadius,
        max_facet_distance=sizeMesh,
    )

    mesh_surf_minus = pygalmesh.generate_surface_mesh(
        s_minus,
        min_facet_angle=minFacetAngle,
        max_radius_surface_delaunay_ball=maxRadius,
        max_facet_distance=sizeMesh,
    )

    if path_data != '':
        if not os.path.isdir(path_data):
            os.mkdir(path_data)
        mesh_surf_testplus.write(path_data + '/' + 'tpms_testplus.stl')
        mesh_surf_testminus.write(path_data + '/' + 'tpms_testminus.stl')
        mesh_surf_plus.write(path_data + '/' + 'tpms_plus.stl')
        mesh_surf_minus.write(path_data + '/' + 'tpms_minus.stl')
    else:
        mesh_surf_testplus.write("tpms_testplus.stl")
        mesh_surf_testminus.write("tpms_testminus.stl")
        mesh_surf_plus.write("tpms_plus.stl")
        mesh_surf_minus.write("tpms_minus.stl")

    return True
