import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
from descartes import PolygonPatch
from createPizza import createPizzaPolygon, createCircularSector
import numpy as np

BLUE = "blue"
GRAY = "red"
GREEN = "green"

k=1
j = 3.576
innerRadius = 0.20
outerRadius = 3.
startingAngle =0+90*k
endAngle =90 +90*j
xCenter = 77.70
yCenter = 540.

xlims = [-outerRadius + xCenter, outerRadius + xCenter]
ylims = [-outerRadius + yCenter, outerRadius + yCenter]

"""
bug values:
    startingAngle = -219.
    endAngle = -220.

    startingAngle = 131.
    endAngle = 130.


    startingAngle = 131.+90
    endAngle = 130.+90
"""

sector = createCircularSector(xCenter, yCenter,innerRadius, outerRadius,
    startingAngle, endAngle)


fig, ax = plt.subplots()

try:
    patchc = PolygonPatch(sector, fc=GREEN, ec=GREEN, alpha=0.5, zorder=2)
    ax.add_patch(patchc)
except:
    print("didnt work")


ax.set_title('Pizza Slice')

ax.set_xlim(xlims)
ax.set_ylim(ylims)


plt.show()
