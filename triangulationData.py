import csv

class StarObject:
    """ A Star Object includes information about each star including name,
    position in 'ra' and position in 'dec,' and visual magnitude. """

    def __init__(self):
        self.name = ''
        self.positionRa = 0
        self.positionDec = 0
        self.vMag = 0

class TriangleObject:
    """ A Triangle Object includes information about each triangle, including
    the three stars in the triangle, the angles and the distance in between them
    . """

    def __init__(self):
        self.starA, self.starB, self.starC = None, None, None
        self.distanceAB, self.distanceAC, self.distanceBC = 0, 0, 0
        self.angleAB, self.angleAC, self.angleBC = 0, 0, 0

class SpaceObject:
    """ A space object contians information about all stars. """

    def __init__(self):
        self.stars = []
        self.triangles = []

def importFile(file):
    """ Imports the file through CSV. Outputs the read file. """

    f = open(file)
    csv_f = csv.reader(f)
    return csv_f
