import numpy as np
import cadquery as cq
import os

from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut

from OCP.ShapeUpgrade import ShapeUpgrade_UnifySameDomain


def rotateEuler(object, center, psi, theta, phi):
    """DESCRIPTION

    Parameters
    ----------
    object : TYPE
        DESCRIPTION
    center : TYPE
        DESCRIPTION
    psi : TYPE
        DESCRIPTION
    theta : TYPE
        DESCRIPTION
    phi : TYPE
        DESCRIPTION

    Returns
    -------
    object_r : TYPE
        DESCRIPTION
    """

    u = np.array([0.0, 0.0, 1.0])
    u = np.array([np.cos(psi * np.pi / 180.0), np.sin(psi * np.pi / 180.0), 0.0])
    z2 = np.array(
        [
            np.sin(psi * np.pi / 180.0) * np.sin(theta * np.pi / 180.0),
            -np.sin(theta * np.pi / 180.0) * np.cos(psi * np.pi / 180.0),
            np.cos(theta * np.pi / 180.0),
        ]
    )

    object_r = object.rotate(
        (center[0], center[1], center[2]), (center[0], center[1], center[2] + 1.0), psi
    )
    object_r = object_r.rotate(
        (center[0], center[1], center[2]),
        (center[0] + u[0], center[1] + u[1], center[2] + u[2]),
        theta,
    )
    object_r = object_r.rotate(
        (center[0], center[1], center[2]),
        (center[0] + z2[0], center[1] + z2[1], center[2] + z2[2]),
        phi,
    )
    return object_r


def removeEmptyLines(filename):
    """DESCRIPTION

    Parameters
    ----------
    filename : TYPE
        DESCRIPTION
    """
    if not os.path.isfile(filename):
        print("{} does not exist ".format(filename))
        return
    with open(filename) as filehandle:
        lines = filehandle.readlines()

    with open(filename, "w") as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines)


def fuseParts(cqShapeList, retain_edges):
    """DESCRIPTION

    Parameters
    ----------
    cqShapeList : TYPE
        DESCRIPTION
    retain_edges : TYPE
        DESCRIPTION

    Returns
    -------
    cq.Shape(fixed) : TYPE
        DESCRIPTION
    occ_solids_list : TYPE
        DESCRIPTION
    """

    #    occ_solids_list = (s.Solids() for s in cqShapeList)
    #    for cqshape in cqShapeList:

    occ_solids_list = [s.Solids() for s in cqShapeList]
    #    print("occ_solids_list = ", occ_solids_list)
    #    flat_list = [item for sublist in occ_solids_list for item in sublist]

    #   print("flat_list = ", flat_list)

    occ_Solids = cqShapeList[0].wrapped
    for i in range(1, len(cqShapeList)):
        fuse = BRepAlgoAPI_Fuse(occ_Solids, cqShapeList[i].wrapped)
        occ_Solids = fuse.Shape()

    if retain_edges:
        return (cq.Shape(occ_Solids), occ_solids_list)
    else:
        upgrader = ShapeUpgrade_UnifySameDomain(occ_Solids, True, True, True)
        upgrader.Build()
        fixed = upgrader.Shape()
        occ_solids_list = [[cq.Solid(fixed)]]

        return (cq.Shape(fixed), occ_solids_list)


# def cut_parts(cqShapeList):
#
#    print('inside cut')
#    phase_cut = []
#    phase_cut.append(cqShapeList[0].copy())
#    cut_objtemp = cqShapeList[0].copy()
#    upgrader = ShapeUpgrade_UnifySameDomain(cut_objtemp.wrapped, True, True, True)
#    upgrader.Build()
#    cut_obj = cq.Shape(upgrader.Shape())
#
#    for shape in cqShapeList[1::]:
#        print('tatayoyo')
#
#        SolidsCut = []
#        for s in shape.Solids():
#            sCut = s.wrapped
#            for t in cut_obj.Solids():
#                cut = BRepAlgoAPI_Cut(sCut, t.wrapped)
#                sCut = cut.Shape()
#            SolidsCut.append(cq.Shape(cut.Shape()))
#        cutted = fuse_parts(SolidsCut, False)
#        phase_cut.append(cutted[0])
#
#        fuse = BRepAlgoAPI_Fuse(cut_obj.wrapped, shape.wrapped)
#        fused = fuse.Shape()
#        upgrader = ShapeUpgrade_UnifySameDomain(fused, True, True, True)
#        upgrader.Build()
#        cut_obj = cq.Shape(upgrader.Shape())
#
#    occ_solids_list = [s.Solids() for s in phase_cut]
#    print(phase_cut)
#    print(occ_solids_list)
#    print('outside cut')
#
#    return (phase_cut, occ_solids_list)


def cutPhasesByShape(cqShapeList, cut_obj):
    """DESCRIPTION

    Parameters
    ----------
    cqShapeList : TYPE
        DESCRIPTION
    cut_obj : TYPE
        DESCRIPTION

    Returns
    -------
    phase_cut : TYPE
        DESCRIPTION
    occ_solids_list : TYPE
        DESCRIPTION
    """
    phase_cut = []

    for shape in cqShapeList:
        cut = BRepAlgoAPI_Cut(shape.wrapped, cut_obj.wrapped)
        if len(cq.Shape(cut.Shape()).Solids()) > 0:
            phase_cut.append(cq.Shape(cut.Shape()))

    occ_solids_list = [s.Solids() for s in phase_cut]
    print(phase_cut)
    print(occ_solids_list)
    print("outside cut")

    return (phase_cut, occ_solids_list)


def cutPhaseByShapeList(phaseToCut, cqShapeList):
    """DESCRIPTION

    Parameters
    ----------
    phaseToCut : TYPE
        DESCRIPTION
    print_cols : TYPE
        DESCRIPTION

    Returns
    -------
    ResultCut : TYPE
        DESCRIPTION
    occ_solids_list : TYPE
        DESCRIPTION
    """

    ResultCut = phaseToCut
    for shape in cqShapeList:
        cut = BRepAlgoAPI_Cut(ResultCut.wrapped, shape.wrapped)
        ResultCut = cq.Shape(cut.Shape())

    occ_solids_list = ResultCut.Solids()
    return (ResultCut, occ_solids_list)


def cutParts(cqShapeList, reverseOrder=True):
    """DESCRIPTION

    Parameters
    ----------
    cqShapeList : TYPE
        DESCRIPTION
    reverseOrder : TYPE, optional
        DESCRIPTION

    Returns
    -------
    phase_cut : TYPE
        DESCRIPTION
    occ_solids_list : TYPE
        DESCRIPTION
    """
    phase_cut = []
    if reverseOrder:
        cqShapeList_inv = cqShapeList[::-1]
    else:
        cqShapeList_inv = cqShapeList
    #    print(cqShapeList)
    #    print(cqShapeList_inv)

    cut_obj = cqShapeList_inv[0].copy()
    phase_cut.append(cut_obj)

    for shape in cqShapeList_inv[1::]:
        copy = shape.copy()
        cut = BRepAlgoAPI_Cut(copy.wrapped, cut_obj.wrapped)
        phase_cut.append(cq.Shape(cut.Shape()))

        fuse = BRepAlgoAPI_Fuse(cut_obj.wrapped, shape.wrapped)
        fused = fuse.Shape()
        upgrader = ShapeUpgrade_UnifySameDomain(fused, True, True, True)
        upgrader.Build()
        cut_obj = cq.Shape(upgrader.Shape())

    phase_cut.reverse()

    occ_solids_list = [s.Solids() for s in phase_cut]
    print(phase_cut)
    print(occ_solids_list)
    print("outside cut")

    return (phase_cut, occ_solids_list)


def rasterShapeList(cqShapeList, rve, grid):
    """DESCRIPTION

    Parameters
    ----------
    cqShapeList : TYPE
        DESCRIPTION
    rve : TYPE
        DESCRIPTION
    grid : TYPE
        DESCRIPTION

    Returns
    -------
    flat_list : TYPE
        DESCRIPTION
    occ_solids_list : TYPE
        DESCRIPTION
    volume_list : TYPE
        DESCRIPTION
    center_list : TYPE
        DESCRIPTION
    """

    occ_solids_list = []

    for cqshape in cqShapeList:
        wk_plane = cq.Workplane().add(cqshape.Solids())
        xgrid = np.linspace(0.0, rve.dx, num=grid[0])
        ygrid = np.linspace(0.0, rve.dy, num=grid[1])
        zgrid = np.linspace(0.0, rve.dz, num=grid[2])
        np.delete(xgrid, 0)
        np.delete(ygrid, 0)
        np.delete(zgrid, 0)
        for i in xgrid:
            Plane_x = cq.Face.makePlane(basePnt=(i, 0, 0), dir=(1, 0, 0))
            wk_plane = wk_plane.split(cq.Workplane().add(Plane_x))
        for j in ygrid:
            Plane_y = cq.Face.makePlane(basePnt=(0, j, 0), dir=(0, 1, 0))
            wk_plane = wk_plane.split(cq.Workplane().add(Plane_y))
        for k in zgrid:
            Plane_z = cq.Face.makePlane(basePnt=(0, 0, k), dir=(0, 0, 1))
            wk_plane = wk_plane.split(cq.Workplane().add(Plane_z))

        occ_solids_list.append(wk_plane.val().Solids())

    flat_list = [item for sublist in occ_solids_list for item in sublist]
    volume_list = [item.Volume() for sublist in occ_solids_list for item in sublist]
    center_list = [item.Center() for sublist in occ_solids_list for item in sublist]
    return (flat_list, occ_solids_list, volume_list, center_list)


# def cut_parts(cqShapeList):
#
#    phase_cut = []
#    occ_Solids = cqShapeList[-1].copy()
#    phase_cut.append(cqShapeList[-1])
#
#    for s in cqShapeList[-2::-1]:
#        print('s', s)
#        cut = BRepAlgoAPI_Cut(s.wrapped, occ_Solids.wrapped)
#        phase_cut.append(cq.Shape(cut.Shape()))
#
#        fuse = BRepAlgoAPI_Fuse(occ_Solids.wrapped, s.wrapped)
#        occ_Solids = fuse.Shape()
#        upgrader = ShapeUpgrade_UnifySameDomain(occ_Solids, True, True, True)
#        upgrader.Build()
#        occ_Solids = cq.Shape(upgrader.Shape())
#
#    print('phase_cut', phase_cut)
#    occ_solids_list = [s.Solids() for s in phase_cut[::-1]]
#    return (phase_cut[::-1], occ_solids_list)


def repeatGeometry(unit_geom, rve, grid):
    """DESCRIPTION

    Parameters
    ----------
    unit_geom : TYPE
        DESCRIPTION
    rve : TYPE
        DESCRIPTION
    grid : TYPE
        DESCRIPTION
    """

    xyz_repeat = cq.Assembly()
    for i_x in range(grid["x"]):
        for i_y in range(grid["y"]):
            for i_z in range(grid["z"]):
                xyz_repeat.add(
                    unit_geom,
                    loc=cq.Location(
                        cq.Vector(i_x * rve.dim_x, i_y * rve.dim_y, i_z * rve.dim_z)
                    ),
                )

    return xyz_repeat.toCompound()
