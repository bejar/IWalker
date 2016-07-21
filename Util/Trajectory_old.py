"""
.. module:: Trajectory

Trajectory
*************

:Description: Trajectory

    

:Authors: bejar
    

:Version: 

:Created on: 15/10/2015 10:30 

"""

__author__ = 'bejar'

import numpy as np


def geodesic(vec):
    """
    Sum of distances of a path (the geodesic distance)

    :param vec: Vector of the coordinates of the trajectory
    :return:
    """

    dif = 0.0
    for i in range(vec.shape[0]-1):
        dif += np.sqrt(((vec[i,0] - vec[i+1,0])**2) + ((vec[i,1] - vec[i+1,1])**2))

    return dif


def parametric_select(vec, dist, min, max):
    """
    Uses the trajectory in vec parametrically normalizing its distance to the interval [0-1] and selects from the
    trajectory a segment betwee min and max

    :param vec: array with the trajectory data
    :param dist: array with the incremental sum of distances of the trajectory
    :param min: minimum element of the trajectory
    :param max: maximum element of the trajectory
    :return:
    """
    dist /= np.max(dist)

    rows = [j for j in range(vec.shape[0]) if min <= dist[j] <= max]

    return(vec[rows, :])


def straightness(vec):
    """
    Straightness coefficient

    returns:
      - Ratio between geodesic and euclidean distance among initial and final point
      - Ratio between geodesic and euclidean distance among initial and final point to the CDM of the curve

    :param vec:
    :return:
    """
    mx = np.sum(vec[:,0])/(vec.shape[0]*1.0)
    my = np.sum(vec[:,1])/(vec.shape[0]*1.0)
    otocdm = np.sqrt(((vec[0,0] - mx)**2) + ((vec[0,1] - my)**2))
    ftocdm = np.sqrt(((vec[-1,0] - mx)**2) + ((vec[-1,1] - my)**2))
    euc = otocdm + ftocdm
    euc2 = np.sqrt(((vec[-1,0] - vec[0,0])**2) + ((vec[-1,1] - vec[0,1])**2))
    geo = geodesic(vec)
    return euc2/geo, euc/geo

def convex_hull(points):
    """Computes the convex hull of a set of 2D points.

    Taken from wikipedia

    Input: an iterable sequence of (x, y) pairs representing the points.
    Output: a list of vertices of the convex hull in counter-clockwise order,
      starting from the vertex with the lexicographically smallest coordinates.
    Implements Andrew's monotone chain algorithm. O(n log n) complexity.
    """

    # Sort the points lexicographically (tuples are compared lexicographically).
    # Remove duplicates to detect the case we have just one unique point.
    points = [(x,y) for x, y in zip(points[:,0], points[:,1])]
    points = sorted(set(points))

    # Boring case: no points or a single point, possibly repeated multiple times.
    if len(points) <= 1:
        return points

    # 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
    # Returns a positive value, if OAB makes a counter-clockwise turn,
    # negative for clockwise turn, and zero if the points are collinear.
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenation of the lower and upper hulls gives the convex hull.
    # Last point of each list is omitted because it is repeated at the beginning of the other list.
    return np.array(lower[:-1] + upper[:-1])

def PolyArea(points):
    """
    Area of a 2D convex Polygon

    :param points:
    :return:
    """
    x= points[:,0]
    y= points[:,1]
    return(0.5*np.abs(np.dot(x, np.roll(y, 1))-np.dot(y,np.roll(x, 1))))

def convex_hull_area(points):
    """
    Computes the area of the convex hull
    :param points:
    :return:
    """
    return(PolyArea(convex_hull(points)))


def aspect_ratio_convex_hull(points):
    """
    Computes the aspect ration of the convex
    :param vec:
    :return:
    """
