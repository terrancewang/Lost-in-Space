import csv
import math
import pickle

"""
Info:
# A more complex definition of absolute magnitude is used for planets and small
Solar System bodies, based on its brightness at one astronomical unit from the
observer and the Sun. The Sun has an apparent magnitude of −27 and Sirius, the
brightest visible star in the night sky, −1.46. This database is reduced so
that it only holds the magnitude and coordinates of the stars with a visual
magnitude below 5.3. Selecting the first 2300 brightest stars.

Attribution Information:
# The core projects were primarily created by Bryant Le (bryantl@berkeley.edu).
Algorithm was developed by Tjorven Delabie, Thomas Durt, Jeroen Vandersteen.
"""

class StarObject:
    """ A Star Object includes information about each star including name,
    position in 'ra' and position in 'dec,' and visual magnitude.
    """

    def __init__(self):
        self.name = ''
        self.starID = 0
        self.positionRa = 0
        self.positionDec = 0
        self.vMag = 0

class TriangleObject:
    """ A Triangle Object includes information about each triangle, including
    the three stars in the triangle, the angles and the distance in between them
    . """

    def __init__(self):
        self.starA, self.starB, self.starC = None, None, None
        self.magA, self.magB, self.magC = 0, 0, 0
        self.distAB, self.distAC, self.distBC = 0, 0, 0
        self.angleA, self.angleB, self.angleC = 0, 0, 0
        self.angleDiffSum = 0

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
        """ Helper function that calculates the position in terms of decimal
        from coordinate system of degrees, minutes, and seconds. """

        degree = float(degree) + float(minute) / 60
        degree = degree + float(second) / 3600
        return degree

    def extractId(name):
        """ Helper function that extracts the ID from the name and returns the
        integer form. """

        stringID = ''
        for i in name:
            if i in '0123456789':
                stringID = stringID + i
        stringID = int(stringID)
        return stringID

    for row in file:
        if initial == False:
            initial = True
        else:
            star = StarObject()
            name, ra1, ra2, ra3, dec1, dec2, dec3, vmag = row
            star.name = name
            star.starID = extractId(name)
            star.vMag = vmag
            star.positionRa = coordinateToDegree(ra1, ra2, ra3)
            star.positionDec = coordinateToDegree(dec1, dec2, dec3)
            starList.append(star)
    return starList

def euclideanDistance(starA, starB):
    """ Computes the euclidean distance between starA and starB and returns
    the distance."""

    raDiff = starA.positionRa - starB.positionRa
    decDiff = starA.positionDec - starB.positionDec
    distance = (raDiff ** 2 + decDiff ** 2) ** 0.5
    return distance

def distances(starA, starB, starC):
    """ Computes euclidean distance between each of the stars. Returns a list
    of euclidean distances between each star. """

    distAB = euclideanDistance(starA, starB)
    distAC = euclideanDistance(starA, starC)
    distBC = euclideanDistance(starB, starC)
    distances = [distAB, distAC, distBC]
    return distances

def angles(distAB, distAC, distBC):
    """ Computes the angles of the triangulation of the three stars using the
    Law of Cosine. """

    cosA = (distAB ** 2 + distAC ** 2 - distBC ** 2) / (2 * distAB * distAC)
    angleA = math.acos(cosA)
    cosB = (distAB ** 2 + distBC ** 2 - distAC ** 2) / (2 * distAB * distBC)
    angleB = math.acos(cosB)
    cosC = (distAC ** 2 + distBC ** 2 - distAB ** 2) / (2 * distAC * distBC)
    angleC = math.acos(cosC)
    angles = [angleA, angleB, angleC]
    return angles

def constructTriangle(starA, starB, starC):
    """ Constructs a triangle, determines distances between stars, angles
    between stars, and returns a TRIANGLE object. """

    triangle = TriangleObject()
    triangle.starA = starA
    triangle.starB = starB
    triangle.starC = starC
    distanceList = distances(starA, starB, starC)
    triangle.distAB, triangle.distAC, triangle.distBC = distanceList
    angleList = angles(triangle.distAB, triangle.distAC, triangle.distBC)
    triangle.angleA, triangle.angleB, triangle.angleC = angleList
    triangle.angleDiffSum = abs(triangle.angleA - triangle.angleB) + \
        abs(triangle.angleB - triangle.angleC) + \
        abs(triangle.angleA - triangle.angleC)
    triangle.magA = starA.vMag
    triangle.magB = starB.vMag
    triangle.magC = starC.vMag
    return triangle

def constructTriangles(starList):
    """ Constructs TRIANGLE object from a list of STAR objects from a SPACE
    object. Return a list of TRIANGLE objects. """
    count = 0
    triangles = []
    i = -1
    for starA in starList:
        i += 1
        j = i
        for starB in starList[i + 1: len(starList) + 1]:
            j += 1
            for starC in starList[j + 1 : len(starList) + 1]:
                triangle = constructTriangle(starA, starB, starC)
                triangles.append(triangle)
                print(count)
                count += 1
    return triangles

def sortByAngleSum(triangleList):
    def partition(triangleList,low,high):
        i = low - 1
        pivot = triangleList[high].angleDiffSum
        for j in range(low , high):
            if triangleList[j].angleDiffSum <= pivot:
                i = i + 1
                triangleList[i], triangleList[j] = triangleList[j], triangleList[i]
        triangleList[i+1], triangleList[high] = triangleList[high], triangleList[i+1]
        return i + 1

    def quickSort(triangleList, low, high):
        if low < high:
            pi = partition(triangleList, low, high)
            quickSort(triangleList, low, pi-1)
            quickSort(triangleList, pi+1, high)

    quickSort(triangleList, 0, len(triangleList)-1)

def getAngleSum(triangleList):
    angleSumList = []
    for triangle in triangleList:
        angleSumList.append(triangle.angleDiffSum)
    return angleSumList

def exportPickle(triangleList):
    with open("triangleAngleSum.txt", "wb") as fp:
        angleSumList = getAngleSum(triangleList)
        pickle.dump(angleSumList, fp)

def exportCSV(triangleList):
    """ Export the CSV file of triangle objects. """

    with open('customerOrderAverages.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',quotechar='|',\
            quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Star A', 'Star B', 'Star C', 'Distance AB', \
            'Distance AC', 'Distance BC', 'Angle A', 'Angle B', 'Angle C', \
            'Angle Sum', 'Magnitude A', 'Magnitude B', 'Magnitude C'])
        for triangle in triangleList:
            starA = str(triangle.starA.name)
            starB = str(triangle.starB.name)
            starC = str(triangle.starC.name)
            distAB = str(triangle.distAB)
            distAC = str(triangle.distAC)
            distBC = str(triangle.distBC)
            angleA = str(triangle.angleA)
            angleB = str(triangle.angleB)
            angleC = str(triangle.angleC)
            angleSum = str(triangle.angleDiffSum)
            magA = str(triangle.magA)
            magB = str(triangle.magB)
            magC = str(triangle.magC)
            filewriter.writerow([starA, starB, starC, distAB, distAC, distBC, \
                angleA, angleB, angleC, angleSum, magA, magB, magC])

if __name__ == "__main__":
    file = importFile('Star Data - Sheet2.csv')
    space = SpaceObject()
    starList = parseStars(file)
    space.stars = starList
    triangleList = constructTriangles(starList)
    space.triangles = triangleList
    sortedTriangleList = sortByAngleSum(triangleList)
    exportPickle(sortedTriangleList)
    exportCSV(sortedTriangleList)
