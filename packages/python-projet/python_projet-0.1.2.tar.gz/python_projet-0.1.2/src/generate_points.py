from shapely.geometry import Point
import random

def takeFirst(elem):
    """
    Return the first coordinate (x) of a point.
    Args:
        elem (int): a shapely point
    Retuns: the first coordinate (x) of a point

    """
    return elem.coords[0][0]


def takeSecond(elem):
    """
    Return the second coordinate (y) of a point.
    Args:
        elem (int): a shapely point
    Returns: the second coordinate (y) of a point

    """
    return elem.coords[0][1]

def generate_random_around(number, polygon):
    """
    Generates random points around a polygon
    Args:
        number (int): number of points to generate per side
        polygon (Polygon): the polygon around which you want to generate the points

    Returns: 4 lists of points generated for each side

    """
    left = []
    right = []
    top = []
    bot = []

    minx, miny, maxx, maxy = polygon.bounds
    while len(left) < number:
        left.append(Point(random.uniform(minx + 10, minx - 50), random.uniform(miny, maxy)))
        right.append(Point(random.uniform(maxx - 100, maxx - 50), random.uniform(miny, maxy)))
        top.append(Point(random.uniform(minx + 100, maxx - 60), random.uniform(maxy, maxy + 1)))
        bot.append(Point(random.uniform(minx + 100, maxx - 60), random.uniform(miny - 1, miny)))

    left.sort(key=takeSecond)
    right.sort(key=takeSecond)
    top.sort(key=takeFirst)
    bot.sort(key=takeFirst)

    return left, right, top, bot
