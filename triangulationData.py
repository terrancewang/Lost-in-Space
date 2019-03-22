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

def parseStars(file):
    """ Takes in a file containing information about stars and parses the file
    into the constructor for the STAR object. Return a list of stars. """

    initial = False
    starList = []

    def coordinateToDegree(degree, minute, second):
        """ Calculates the position in terms of decimal from coordinate system
        of degrees, minutes, and seconds. """

        degree = float(degree) + float(minute / 60)
        degree = degree + float(second / 3600)
        return degree

    for row in csvFile:
        if initial == False:
            initial = True
        else:
            star = StarObject()
            name, ra1, ra2, ra3, dec1, dec2, dec3, vmag = row
            star.name = name
            star.vMag = vmag
            star.positionRa = coordinateToDegree(ra1, ra2, ra3)
            star.positionDec = coordinateToDegree(dec1, dec2, dec3)
            starList.append(star)
    return starList

if __name__ == "__main__":
    file = importFile('Star Data - Sheet2.csv')
    space = SpaceObject()
