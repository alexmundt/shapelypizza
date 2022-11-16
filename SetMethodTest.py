# code from  https://shapely.readthedocs.io/en/latest/code/difference.py
# slighty modified

from matplotlib import pyplot
from shapely.geometry import Point, Polygon
from descartes import PolygonPatch
import numpy as np

#from figures import SIZE, BLUE, GRAY, set_limits

BLUE = "blue"
GRAY = "red"
GREEN = "green"

fig = pyplot.figure(1)

xlims = [-2,2]
ylims = [-2,2]

a = Point(0, 0).buffer(1.5)
b = Point(0, 0).buffer(0.2)

# pizza slice Polygon

pizza = Polygon([(0,0),(0.5,2),(-0.5,2)])

# 1

bounds = a.bounds
xLeft,yBot, xRight, yTop = bounds
print(f"xLeft = {xLeft}")
print(f"bounds = {bounds}")

def createPizzaPolygon(bounds, startangle, endangle):
    """
    a function that creates the pizza slice
    assumes a circle base on bounds
    the slicing part is always(!) in clockwise direction, even when starting
    angle is greater than ending angle
    """
    # fix starting position
    xCenter = 0.
    yCenter = 0.

    # check if midpoint is the same for x and y direction
    xLeft,yBot, xRight, yTop = bounds
    radiusX = (xRight - xLeft) / 2
    radiusY = (yTop - yBot) / 2

    if radiusX == radiusY:
        print("radiusX == radiusY is True")
        # make more checks if Polyon's bounds are bounds of a square or circle

    # modify startangles values from degree to radians
    startangle = startangle/360*2.*np.pi
    endangle = endangle/360*2.*np.pi


    x1 = np.sin(startangle)*yTop
    y1 = np.cos(startangle)*yTop

    x2 = np.sin(endangle)*yTop
    y2 = np.cos(endangle)*yTop

    print(f"Point a of Polygon for {startangle}° is {x1}-{y1}")
    print(f"Point a of Polygon for {endangle}° is {x2}-{y2}")

    centerPoint = (xCenter,yCenter)
    startPoint = (x1,y1)
    endPoint = (x2,y2)

    # corner points: 1 is top right, 2 bottom right, 3 bottom left, 4 top left
    # use a scale factor to stop circle points intersecting with polygon border
    # lines
    scaleFactor = 1.01
    corner1 = (xRight*scaleFactor, yTop*scaleFactor)
    corner2 = (xRight*scaleFactor, yBot*scaleFactor)
    corner3 = (xLeft*scaleFactor, yBot*scaleFactor)
    corner4 = (xLeft*scaleFactor, yTop*scaleFactor)
    # xLeft,yBot, xRight, yTop = bounds
    cornerlist = [corner1, corner2, corner3, corner4]
    #cornerlist *= 1.01

    # get the start- and endquadrant
    startquadrant = int((startangle%(2.*np.pi))/(2.*np.pi) *4)
    endquadrant = int((endangle%(2.*np.pi))/(2.*np.pi)*4)
    print(f"startquadrant = {startquadrant}")
    print(f"endquadrant = {endquadrant}")

    # pizzaslice = Polygon([centerPoint,startPoint,endPoint]) # this is old stuff
    polygonpointlist = [centerPoint, startPoint]

    # take care of case where startangle is greater than endangle (so almost
    # complete cycle)
    startangle_mod = startangle % (np.pi*2.)
    endangle_mod = endangle % (np.pi*2.)
    if startangle_mod > endangle_mod:
        # idea: change first corner point to avoid problems with multiple
        # identical points in Polygon list
        print("###############")
        firstCorner = cornerlist[startquadrant]
        changedStartCorner = (firstCorner[0]*1.01, firstCorner[1]*1.01)
        polygonpointlist.append(changedStartCorner)
        for item in cornerlist[startquadrant+1:]:
            polygonpointlist.append(item)
        for item in cornerlist[0:endquadrant+1]:
            polygonpointlist.append(item)
    else:
        # this is for the case that the start and endquadrant are "in order"
        # i.e between 0-360 and startangle is smaller
        # this only needs the per piece addition of the Points
        for item in cornerlist[startquadrant:endquadrant+1]:
            polygonpointlist.append(item)
    # add last point of polygon
    polygonpointlist.append(endPoint)

    print(f"polyonpointist = {polygonpointlist}")
    # check if angle difference is greater than 2*pi (which would mean whole
    # circle )
    angledifference = endangle - startangle
    print(f"angle-difference is {angledifference}")
    # if angle difference is greater than 2 pi just take the whole square
    if angledifference > 2.*np.pi:
        polygonpointlist = cornerlist

    # finally: create the polygon using a shapely class and the final Point list
    pizzaslice = Polygon(polygonpointlist)

    return pizzaslice


for i in range(0,36):
    angle = -10.*i
    realangle = 360 + angle
    angle_rad = angle/360*2*np.pi
    quadrant = int(angle_rad/(2.*np.pi)*4) % 4
    print(f"angle = {angle}, realangle = {realangle} and quadrant = {quadrant}" )
pizzaslice = createPizzaPolygon(bounds,-300,-90)
# fix this behavior


#a few of these bugs probably have to do with modulo problems with negative numbers

#


ax = fig.add_subplot(121)

patch1 = PolygonPatch(a, fc=GRAY, ec=GRAY, alpha=0.2, zorder=1)
ax.add_patch(patch1)
patch2 = PolygonPatch(b, fc=BLUE, ec=BLUE, alpha=0.2, zorder=1)
ax.add_patch(patch2)
c = a.difference(b)
print(c.geom_type)
patchc = PolygonPatch(c, fc=GREEN, ec=GREEN, alpha=0.5, zorder=2)
ax.add_patch(patchc)

ax.set_title('a.difference(b)')

# set_limits(ax, -1, 4, -1, 3)
ax.set_xlim(xlims)
ax.set_ylim(ylims)

#2
ax = fig.add_subplot(122)

patch1 = PolygonPatch(a, fc=BLUE, ec=BLUE, alpha=0.2, zorder=1)
ax.add_patch(patch1)
patch2 = PolygonPatch(b, fc=GRAY, ec=GRAY, alpha=0.2, zorder=1)
#ax.add_patch(patch2)
# c = b.difference(a)

# for Pizza ring
c = a.difference(b)
c = c.intersection(pizzaslice)

# for simple pizza
# c = a.intersection(pizza)

print(c.geom_type)
try:
    patchc = PolygonPatch(c, fc=GREEN, ec=GREEN, alpha=0.5, zorder=2)
    ax.add_patch(patchc)
except:
    print("didnt work")


ax.set_title('Pizza Slice')

ax.set_xlim(xlims)
ax.set_ylim(ylims)

#set_limits(ax, -1, 4, -1, 3)

pyplot.show()
