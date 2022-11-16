# testclass
from PizzaClass import Pizza
import matplotlib.pyplot as plt
import numpy as np
from random import random

innerRadius = 0.20
outerRadius = 3.
startAngle = 45.
endAngle = 130.
xCenter = 77.70
yCenter = 240.


pizzaobject = Pizza(xCenter, yCenter, innerRadius, outerRadius, startAngle,
    endAngle)

fig, ax = pizzaobject.plot()


# check if stuff works
x1 = 77
x2 = 81
y1 = 238
y2 = 242


noise_variance = 0.05

for x in np.linspace(x1,x2, num = 20):
    for y in np.linspace(y1,y2, num = 20):

        x_noise = random()*noise_variance - noise_variance/2.
        y_noise = random()*noise_variance - noise_variance/2.
        x = x + x_noise
        y = y + y_noise
        olive  = "#9AB973"
        black = "black"
        if random() < 0.5:
            color = olive
        else:
            color = black
        # ax.plot(x,y,'o') #
        red = "red"
        ################# why is this plot doing nothing?
        if pizzaobject.is_in_domain(y,x):
            ax.plot(x,y,'o', color=color)
        else:
            ax.plot(x,y,'o', color=red)


plt.show()
