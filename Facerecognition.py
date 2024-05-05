from __future__ import print_function

__doc__ == """ Loads a STEP file and identify geometrical nature of each face
(cylindrical face, planar etc.)
See github issue https://github.com/tpaviot/pythonocc-core/issues/470
Two options in this example:
1. Click any planar or cylindrical face from the 3d window. They will
be identified as known surfaces, their properties displayed in the
console
2. A batch mode : click the menu button. All the faces will be traversed
and analyzed
"""

import random
import os
import os.path
import sys

from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone,IFSelect_ItemsByEntity
from OCC.Core.GeomAbs import GeomAbs_Plane, GeomAbs_Cylinder, GeomAbs_BSplineSurface
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.TopoDS import TopoDS_Face
from OCC.Display.SimpleGui import init_display
from OCC.Extend.DataExchange import read_step_file
from OCC.Extend.TopologyUtils import TopologyExplorer
def read_step_file(filename):
    """ read the STEP file and returns a compound
    """
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile(filename)

    if status == IFSelect_RetDone:  # check status
        failsonly = False
        step_reader.PrintCheckLoad(failsonly, IFSelect_ItemsByEntity)
        step_reader.PrintCheckTransfer(failsonly, IFSelect_ItemsByEntity)

        ok = step_reader.TransferRoot(1)
        _nbs = step_reader.NbShapes()
        aResShape = step_reader.Shape(1)
    else:
        print("Error: can't read file.")
        sys.exit(0)
    return aResShape


def recognize_face(a_face):
    """ Takes a TopoDS shape and tries to identify its nature
    whether it is a plane a cylinder a torus etc.
    if a plane, returns the normal
    if a cylinder, returns the radius
    """
    if not type(a_face) is TopoDS_Face:
        print("Please hit the 'G' key to switch to face selection mode")
        return False
    surf = BRepAdaptor_Surface(a_face, True)
    surf_type = surf.GetType()
    if  surf_type == GeomAbs_Plane:
        print("This is a Plane Geometry")
        # look for the properties of the plane
        # first get the related gp_Pln
        gp_pln = surf.Plane()
        location = gp_pln.Location()  # a point of the plane
        normal = gp_pln.Axis().Direction()  # the plane normal
        # then export location and normal to the console output
        print("--> Location (global coordinates)", location.X(), location.Y(), location.Z())
        print("--> Normal (global coordinates)", normal.X(), normal.Y(), normal.Z())
    elif surf_type == GeomAbs_Cylinder:
        print("This is a Cylinder")
        # look for the properties of the cylinder
        # first get the related gp_Cyl
        gp_cyl = surf.Cylinder()
        location = gp_cyl.Location()  # a point of the axis
        axis = gp_cyl.Axis().Direction()  # the cylinder axis
        # then export location and normal to the console output
        print("--> Location (global coordinates)", location.X(), location.Y(), location.Z())
        print("--> Axis (global coordinates)", axis.X(), axis.Y(), axis.Z())
    elif surf_type == GeomAbs_BSplineSurface:
        print("This is a Bspline Surface")
        gp_bsrf =surf.Surface
        degree = gp_bsrf.NbUKnots()
    else:
        # TODO there are plenty other type that can be checked
        # see documentation for the BRepAdaptor class
        # https://www.opencascade.com/doc/occt-6.9.1/refman/html/class_b_rep_adaptor___surface.html
        print("not implemented")


def recognize_clicked(shp, *kwargs):
    """ This is the function called every time
    a face is clicked in the 3d view
    """
    for shape in shp:  # this should be a TopoDS_Face TODO check it is
        print("Face selected: ", shape)
        recognize_face(shape)


def recognize_batch(event=None):
    """ Menu item : process all the faces of a single shape
    """
    # loops over faces
    for face in TopologyExplorer(shp).faces():
        #call the recognition function
        recognize_face(face)

def exit(event=None):
    sys.exit()


if __name__ == '__main__':
    display, start_display, add_menu, add_function_to_menu = init_display()
    display.SetSelectionModeFace()  # switch to Face selection mode
    display.register_select_callback(recognize_clicked)
    # first loads the STEP file and display
    shp = read_step_file("C:/Users/nadjei/Documents/Cardio/Part2 (1).STEP")
    display.DisplayShape(shp, update=True)
    add_menu('recognition')
    add_function_to_menu('recognition', recognize_batch)
    start_display()