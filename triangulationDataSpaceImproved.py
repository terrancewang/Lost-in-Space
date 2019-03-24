import csv
import math
import pickle
import sqlite3
from sqlite3 import Error

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
            name, ra1, ra2, ra3, dec1, dec2, dec3, vmag = row
            star = [name, coordinateToDegree(ra1, ra2, ra3), \
                coordinateToDegree(dec1, dec2, dec3), float(vmag)]
            starList.append(star)
    return starList

def euclideanDistance(starA, starB):
    """ Computes the euclidean distance between starA and starB and returns
    the distance."""

    raDiff = starA[1] - starB[1]
    decDiff = starA[2] - starB[2]
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
    angleA = math.degrees(math.acos(cosA))
    cosB = (distAB ** 2 + distBC ** 2 - distAC ** 2) / (2 * distAB * distBC)
    angleB = math.degrees(math.acos(cosB))
    cosC = (distAC ** 2 + distBC ** 2 - distAB ** 2) / (2 * distAC * distBC)
    angleC = math.degrees(math.acos(cosC))
    angles = [angleA, angleB, angleC]
    return angles

def constructTriangle(starA, starB, starC):
    """ Constructs a triangle, determines distances between stars, angles
    between stars, and returns a TRIANGLE object. """
    distanceList = distances(starA, starB, starC)
    maxD = max(distanceList)
    distanceList = [d / maxD for d in distanceList]
    copyDistList = list(distanceList)
    copyDistList.remove(max(copyDistList))
    secondMaxDist = max(copyDistList)
    angleList = angles(distanceList[0], distanceList[1], distanceList[2])
    angleSum = abs(angleList[0] - angleList[1]) + \
        abs(angleList[1] - angleList[2]) + abs(angleList[2] - angleList[0])
    triangle = [starA[0], starB[0], starC[0]] + distanceList \
        + [starA[3], starB[3], starC[3]] + [secondMaxDist]
    return triangle

def constructTriangles(db_file, starList):
    """ Constructs TRIANGLE object from a list of STAR objects from a SPACE
    object. Return a list of TRIANGLE objects. """
    i = -1
    for starA in starList:
        i += 1
        j = i
        for starB in starList[i + 1: len(starList) + 1]:
            j += 1
            for starC in starList[j + 1 : len(starList) + 1]:
                triangle = constructTriangle(starA, starB, starC)
                print(triangle)
                insertTable(db_file, triangle)
                return None
    return None

def insertTable(db_file, triangle):
    conn = sqlite3.connect(db_file)
    sql = ''' INSERT INTO TRIANGLES (STAR_A_NAME, STAR_B_NAME,
        STAR_C_NAME, DIST_A, DIST_B, DIST_C, MAG_A, MAG_B, MAG_C, RATIO)
        VALUES (?,?,?,?,?,?,?,?,?,?) '''
    """conn.execute(sql, (str(triangle[0]), str(triangle[1]), str(triangle[2]), \
    str(triangle[3]), str(triangle[4]), str(triangle[5]), str(triangle[6]), \
    str(triangle[7]), str(triangle[8]), str(triangle[9]) ))"""
    conn.execute(" INSERT INTO TRIANGLES (STAR_A_NAME, STAR_B_NAME,STAR_C_NAME, DIST_A, DIST_B, DIST_C, MAG_A, MAG_B, MAG_C, RATIO) VALUES ("Star","star","star",1,2,3,4,5,6,7)")
    print('inserted')

def selectTable(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.execute("SELECT STAR_A_NAME, STAR_B_NAME, STAR_C_NAME, DIST_A, DIST_B, DIST_C, MAG_A, MAG_B, MAG_C, RATIO from TRIANGLES")
    for row in cursor:
        print(row[0])
    conn.close()

"""def sortByAngleSum(triangleList):
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
        pickle.dump(angleSumList, fp)"""

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        conn.execute('''CREATE TABLE TRIANGLES
         (STAR_A_NAME TEXT ,
         STAR_B_NAME TEXT ,
         STAR_C_NAME TEXT  ,
         DIST_A REAL,
         DIST_B REAL,
         DIST_C REAL,
         MAG_A REAL,
         MAG_B REAL,
         MAG_C REAL,
         RATIO REAL);''')
    except Error as e:
        print(e)
    finally:
        conn.close()
    print('Done making table')

if __name__ == "__main__":
    file = importFile('Star Data - Sheet2.csv')
    create_connection("triangles.db")
    starList = parseStars(file)
    triangleList = constructTriangles("triangles.db", starList)
    selectTable("triangles.db")
