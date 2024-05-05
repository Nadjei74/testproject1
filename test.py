"""from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

display, start_display, add_menu, add_function_to_menu = init_display()
my_box = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()

display.DisplayShape(my_box, update=True)
start_display()"""
import  math

from OCC.Core.gp import (
gp_Pnt, gp_Vec,gp_Trsf,gp_Ax2,gp_Ax3,gp_Pnt2d,gp_Dir2d,gp_Ax2d,gp_Pln
)

from OCC.Core.GC import GC_MakeArcOfCircle, GC_MakeSegment
from OCC.Core.GCE2d import GCE2d_MakeSegment
from OCC.Core.Geom import Geom_CylindricalSurface
from OCC.Core.Geom2d import Geom2d_Ellipse, Geom2d_TrimmedCurve
from OCC.Core.BRepBuilderAPI import (
BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeWire,BRepBuilderAPI_Transform
)

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepLib import breplib
from OCC.Core.BRep import BRep_Builder
from OCC.Core.GeomAbs import GeomAbs_Plane
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.TopoDS import topods, TopoDS_Compound, TopoDS_Face
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_FACE
from OCC.Core.TopTools import TopTools_ListOfShape

# Creating my points
height= 70
#width = 50
#thickness = 30

aPnt1= gp_Pnt(-25,10,0)
aPnt2 = gp_Pnt(-25,-10,0)
aPnt3 = gp_Pnt(25,-10,0)
aPnt4 = gp_Pnt(25,10,0)

#Creating Edges
aEdge1 = BRepBuilderAPI_MakeEdge(aPnt1, aPnt2)
aEdge2 = BRepBuilderAPI_MakeEdge(aPnt2, aPnt3)
aEdge3 = BRepBuilderAPI_MakeEdge(aPnt3, aPnt1)
#aEdge4 = BRepBuilderAPI_MakeEdge(aPnt4, aPnt1)

#Creating Wire
#aWire = BRepBuilderAPI_MakeWire(aEdge1.Edge(), aEdge2.Edge(), aEdge3.Edge(), aEdge4.Edge())
aWire = BRepBuilderAPI_MakeWire(aEdge1.Edge(), aEdge2.Edge(), aEdge3.Edge())
myWireProfile = aWire.Wire()

#Covert Wire to Face
FaceProfile = BRepBuilderAPI_MakeFace(myWireProfile)

#Direction to sweep the face along to create the solid
aPrismVec = gp_Vec(0,0,height)
myBody = BRepPrimAPI_MakePrism(FaceProfile.Face(), aPrismVec)

if __name__ == "__main__":
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()
    display.DisplayShape(myBody.Shape(), update=True)
    start_display()

