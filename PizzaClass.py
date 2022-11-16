from obspy.clients.fdsn.mass_downloader import Domain
import createPizza as pizza
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from shapely.geometry import Point

class Pizza(Domain):
    """ a class that creates a pizza slice object
    """
    def __init__(self, longitude, latitude, innerRadius, outerRadius, startAngle,
        endAngle):
        """ function documentation
        """
        Domain.__init__(self)

        self.pizza = pizza.createCircularSector(longitude, latitude, innerRadius,
            outerRadius, startAngle, endAngle)

        self.longitude = longitude
        self.latitude = latitude
        self.innerRadius = innerRadius
        self.outerRadius = outerRadius
        self.startAngle = startAngle
        self.endAngle = endAngle

    def get_query_parameters(self):
        """
        Return the domain specific query parameters for the get_stations()
        method as a dictionary.
        """
        return {"latitude": self.latitude,
                "longitude": self.longitude,
                "minradius": self.innerRadius,
                "maxradius": self.outerRadius}

    def is_in_domain(self, latitude, longitude):
        """
        Returns True/False depending on the point being in the domain.
        """
        point = Point(longitude, latitude)
        TruthValue = False
        if self.pizza.contains(point):
            TruthValue = True
        return TruthValue


    def plot(self, color="green", ax = None):
        """ function to plots
        """

        sector = self.pizza
        fig = None
        if ax == None:
            fig, ax = plt.subplots()

        xlims = [-self.outerRadius + self.longitude,
            self.outerRadius + self.longitude]
        ylims = [-self.outerRadius + self.latitude,
            self.outerRadius + self.latitude]

        try:
            patchc = PolygonPatch(sector, fc=color, ec=color, alpha=0.5,
                zorder=2)
            ax.add_patch(patchc)
        except Exception as ex:
             print("There was problem during plotting:")
             print(ex)


        ax.set_title('Pizza Slice')

        ax.set_xlim(xlims)
        ax.set_ylim(ylims)


        # plt.show()

        return fig, ax
