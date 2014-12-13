# -*- coding: utf-8 -*-
"""Copyright 2014 Roger R Labbe Jr.

filterpy library.
http://github.com/rlabbe/filterpy

Documentation at:
https://filterpy.readthedocs.org

Supporting book at:
https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python

This is licensed under an MIT license. See the readme.MD file
for more information.
"""

from numpy.random import randn
import numpy as np
import matplotlib.pyplot as plt
from filterpy.kalman import EnsembleKalmanFilter as EnKF
from filterpy.common import Q_discrete_white_noise


DO_PLOT = False

def test_1d_const_vel():

    def hx(x):
        return np.array([x[0]])

    F = np.array([[1., 1.],[0., 1.]])
    def fx(x, dt):
        return np.dot(F, x)

    x = np.array([0., 1.])
    P = np.eye(2)* 100.
    f = EnKF(x=x, P=P, dim_z=1, dt=1., N=8, hx=hx, fx=fx)

    std_noise = 10.

    f.R *= std_noise**2
    f.Q = Q_discrete_white_noise(2, 1., .001)

    measurements = []
    results = []
    ps = []

    zs = []
    for t in range (0,100):
        # create measurement = t plus white noise
        z = t + randn()*std_noise
        zs.append(z)

        f.predict()
        f.update(np.asarray([z]))

        # save data
        results.append (f.x[0])
        measurements.append(z)
        ps.append(3*(f.P[0,0]**.5))

    results = np.asarray(results)
    ps = np.asarray(ps)

    if DO_PLOT:
        plt.plot(results, label='EnKF')
        plt.plot(measurements, c='r', label='z')
        plt.plot (results-ps, c='k',linestyle='--', label='3$\sigma$')
        plt.plot(results+ps, c='k', linestyle='--')
        plt.legend(loc='best')
        #print(ps)



if __name__ == '__main__':
    DO_PLOT = True

    test_1d_const_vel()


#test_noisy_1d()