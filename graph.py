from scipy.stats import multivariate_normal
import numpy as np
import matplotlib.pyplot as plt

X = np.linspace(10000, 30000, 1000)
Y = np.linspace(1, 2.2, 1000)
X, Y = np.meshgrid(X,Y)
X_mean = 20000; Y_mean = 1.6
X_std = 4000; Y_std = 0.2

pos = np.empty(X.shape+(2,))
pos[:,:,0]=X
pos[:,:,1]=Y

rv = multivariate_normal(mean=[X_mean, Y_mean],
                         cov=[[X_std**2, 0.75*X_std*Y_std], [0.75j*X_std*Y_std, Y_std**2]])
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, rv.pdf(pos), cmap='plasma')
plt.show()
