"""from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

display, start_display, add_menu, add_function_to_menu = init_display()
my_box = BRepPrimAPI_MakeBox(10., 20., 30.).Shape()

display.DisplayShape(my_box, update=True)
start_display()"""
import  math

from OCC.Core.gp import (
gp_Pnt, gp_Vec,gp_Trsf,gp_Ax2,gp_Ax3,gp_Pnt2d,gp_Dir2d,gp_Ax2d,gp_Pln,gp_Circ,gp_Dir
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
from OCC.Core.TopoDS import topods, TopoDS_Compound, TopoDS_Face, TopoDS_Edge,TopoDS_Wire
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_FACE
from OCC.Core.TopTools import TopTools_ListOfShape
from math import pi

# Creating my points
height= 70
#width = 50
#thickness = 30

"""aPnt1= gp_Pnt(-25,10,0)
aPnt2 = gp_Pnt(-25,-10,0)
aPnt3 = gp_Pnt(0,-20,0)
aPnt4 = gp_Pnt(25,-10,0)
aPnt5 = gp_Pnt(25,10,0)

#Creating Edges
aEdge1 = BRepBuilderAPI_MakeEdge(aPnt1, aPnt2)
aEdge2 = BRepBuilderAPI_MakeEdge(aPnt2, aPnt3)
aEdge3 = BRepBuilderAPI_MakeEdge(aPnt3, aPnt4)
aEdge4 = BRepBuilderAPI_MakeEdge(aPnt4, aPnt5)
aEdge5 = BRepBuilderAPI_MakeEdge(aPnt5, aPnt1)

theEdges = [aEdge1,aEdge2,aEdge3,aEdge4, aEdge5 ]
"""
# Ask the user for the number of points
num_points = int(input("Enter the number of points: "))

# Initialize an empty list to collect the edges
theEdges = []

# Initialize the first point
x, y, z = map(float, input("Enter coordinates for point 1 (x y z): ").split())
prev_point = gp_Pnt(x, y, z)
#prev_point = gp_Pnt(*map(float, input("Enter coordinates for point 1 (x y z): ").split()))

# Loop to create points and edges
for i in range(2, num_points + 1):
    # Ask the user for the coordinates of the next point
    x, y, z = map(float, input(f"Enter coordinates for point {i} (x y z): ").split())
    next_point = gp_Pnt(x, y, z)
    #next_point = gp_Pnt(*map(float, input(f"Enter coordinates for point {i} (x y z): ").split()))

    # Create an edge between the previous point and the current point
    edge = BRepBuilderAPI_MakeEdge(prev_point, next_point)

    # Add the edge to the list
    theEdges.append(edge)

    # Update the previous point for the next iteration
    prev_point = next_point

# Create the final edge connecting the last point to the first point to form a closed loop
x, y, z = map(float, input("Enter coordinates for point 1 (x y z): ").split())
Point1 = gp_Pnt(x, y, z)
final_edge = BRepBuilderAPI_MakeEdge(prev_point, Point1)

# Add the final edge to the list
theEdges.append(final_edge)
print(theEdges)

#Creating Wire
aWire = BRepBuilderAPI_MakeWire()
for edge in theEdges:
    aWire.Add(edge.Edge())

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

