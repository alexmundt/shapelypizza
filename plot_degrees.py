import numpy as np
import matplotlib.pyplot as plt



def lengthOfLatitude(phi):
    length = 111132.92 - 559.82 * np.cos(2 * phi) +1.175 * np.cos(4 * phi) - \
        0.0023 * np.cos(6. * phi)

    return length

def lengthOfLongitude(phi):
    length = 111412.84 * np.cos(phi) - 93.5 * np.cos(3.*phi) + \
        0.118 * np.cos(5.*phi)

    return length

def mTokm(data):
    kmData = data / 1000
    return kmData


startLatitude = 0.
endLatitude = 90.
startLongitude = 0.
endLongitude = 90.

phiLatitude = np.linspace(startLatitude, endLatitude)
phiLatitude = np.deg2rad(phiLatitude)
phiLongitude = np.linspace(startLongitude, endLongitude)
phiLongitude = np.deg2rad(phiLongitude)

lengthLat = lengthOfLatitude(phiLatitude)
lengthLon = lengthOfLongitude(phiLongitude)

fig, (ax1, ax2) = plt.subplots(2,1)

phiLatitude = np.rad2deg(phiLatitude)
kmLatitude = mTokm(lengthLat)
ax1.plot(phiLatitude, kmLatitude)
ax1.set_title(r"Distance between latitudes at latitude $\phi$")
ax1.set_ylabel("distance [km]")
ax1.set_xlabel("latitude $\phi$ [deg]")



phiLongitude = np.rad2deg(phiLongitude)
kmLongitude = mTokm(lengthLon)
ax2.plot(phiLongitude, kmLongitude)
ax2.set_title(r"Distance between longitudes at latitude $\phi$")
ax2.set_xlabel("latitude $\phi$ [deg]")
ax2.set_ylabel("distance [km]")

plt.show()
