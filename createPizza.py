import numpy as np
from shapely.geometry import Point, Polygon


def createPizzaPolygon(bounds, startangle, endangle):
    """
    a function that creates the pizza slice
    assumes a circle base on bounds
    the slicing part is always(!) in clockwise direction, even when starting
    angle is greater than ending angle
    """

    # check if midpoint is the same for x and y direction
    xLeft,yBot, xRight, yTop = bounds
    radiusX = (xRight - xLeft) / 2
    radiusY = (yTop - yBot) / 2

    # get starting position from bounds items
    xCenter = (xLeft+xRight)/2.
    yCenter = (yTop+yBot)/2.

    # print(f"xCenter = {xCenter}")
    # print(f"yCenter = {yCenter}")

    if radiusX == radiusY:
        print("radiusX == radiusY is True")
        # make more checks if Polyon's bounds are bounds of a square or circle

    # modify startangles values from degree to radians
    startangle = startangle/360*2.*np.pi
    endangle = endangle/360*2.*np.pi


    x1 = np.sin(startangle)*radiusX
    y1 = np.cos(startangle)*radiusX

    x2 = np.sin(endangle)*radiusX
    y2 = np.cos(endangle)*radiusX

    # print(f"Point a of Polygon for {startangle}° is {x1}-{y1}")
    # print(f"Point a of Polygon for {endangle}° is {x2}-{y2}")

    centerPoint = (xCenter,yCenter)
    startPoint = (xCenter + x1, yCenter + y1)
    endPoint = (xCenter + x2,yCenter + y2)

    cornerlist = createCornerList(1.01, yCenter, xCenter, radiusY,
        radiusX)
    cornerlist1 = createCornerList(1.02, yCenter, xCenter, radiusY,
        radiusX)

    # get the start- and endquadrant
    startquadrant = int((startangle%(2.*np.pi))/(2.*np.pi) *4)
    endquadrant = int((endangle%(2.*np.pi))/(2.*np.pi)*4)
    # print(f"startquadrant = {startquadrant}")
    # print(f"endquadrant = {endquadrant}")

    # pizzaslice = Polygon([centerPoint,startPoint,endPoint]) # this is old stuff
    polygonpointlist = [centerPoint, startPoint]

    # take care of case where startangle is greater than endangle (so almost
    # complete cycle)
    startangle_mod = startangle % (np.pi*2.)
    endangle_mod = endangle % (np.pi*2.)
    if startangle_mod > endangle_mod:

        for item in cornerlist[startquadrant:]:
            polygonpointlist.append(item)
        """
        for item in cornerlist[0:endquadrant+1]:
            # check if item is already in polygonpointlist to see if there
            # will be clashes in the Polygon function (due to multiple identical
            # points)
            if item in polygonpointlist:
                newPoint = (item[0]*scaleFactor, item[1]*scaleFactor)
                polygonpointlist.append(newPoint)
            else:
                polygonpointlist.append(item)
        """
        # for the 2nd run through the outer corner points
        for item in cornerlist1[0:endquadrant+1]:
            polygonpointlist.append(item)

    else:
        # this is for the case that the start and endquadrant are "in order"
        # i.e between 0-360 and startangle is smaller
        # this only needs the per piece addition of the Points
        for item in cornerlist[startquadrant:endquadrant+1]:
            polygonpointlist.append(item)
    # add last point of polygon
    polygonpointlist.append(endPoint)

    # check if angle difference is greater than 2*pi (which would mean whole
    # circle )
    angledifference = endangle - startangle
    # if angle difference is greater than 2 pi just take the whole square
    if np.abs(angledifference) > 2.*np.pi:
        polygonpointlist = cornerlist

    # finally: create the polygon using a shapely class and the final Point list
    pizzaslice = Polygon(polygonpointlist)

    return pizzaslice


def createCircularSector(xCenter, yCenter, innerRadius, outerRadius, startAngle,
    endAngle):
    """
    create and return a circular sector as shapely object. the sector has an
    inner cicular cutout
    """
    innerCircle = Point(xCenter, yCenter).buffer(innerRadius)
    outerCircle = Point(xCenter, yCenter).buffer(outerRadius)

    bounds = outerCircle.bounds

    pizzaslice = createPizzaPolygon(bounds,startAngle,endAngle)

    # for Pizza ring
    sector = outerCircle.difference(innerCircle)
    sector = sector.intersection(pizzaslice)

    return sector



def createCornerList(scaleFactor, yCenter, xCenter, radiusY, radiusX):
    """
    create list of corner points dependent on scale factor,
    center coordinates and radius.
    the actual coordinates of the corner scale with the radius multiplied by
    the scale factor
    """
    # corner points: 1 is top right, 2 bottom right, 3 bottom left, 4 top left
    # use a scale factor to stop circle points intersecting with polygon border
    # lines
    top = yCenter + radiusY * scaleFactor
    bottom = yCenter - radiusY * scaleFactor
    left = xCenter - radiusX * scaleFactor
    right = xCenter + radiusX * scaleFactor
    corner1 = (right, top)
    corner2 = (right, bottom)
    corner3 = (left, bottom)
    corner4 = (left, top)
    # xLeft,yBot, xRight, yTop = bounds
    cornerlist = [corner1, corner2, corner3, corner4]
    #cornerlist *= 1.01

    return cornerlist
