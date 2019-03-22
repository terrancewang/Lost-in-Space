import unittest
import triangulationData

class TestMain(unittest.TestCase):

    def testSort(self):
        triangles = [triangulationData.TriangleObject() for i in range(7)]
        triangles[0].angleDiffSum = 100
        triangles[1].angleDiffSum = 120
        triangles[2].angleDiffSum = 14
        triangles[3].angleDiffSum = 10
        triangles[4].angleDiffSum = 90
        triangles[5].angleDiffSum = 150
        triangles[6].angleDiffSum = 110
        triangulationData.sortByAngleSum(triangles)
        self.assertEqual(triangles[0].angleDiffSum, 10)
        self.assertEqual(triangles[1].angleDiffSum, 14)
        self.assertEqual(triangles[2].angleDiffSum, 90)
        self.assertEqual(triangles[3].angleDiffSum, 100)
        self.assertEqual(triangles[4].angleDiffSum, 110)
        self.assertEqual(triangles[5].angleDiffSum, 120)
        self.assertEqual(triangles[6].angleDiffSum, 150)
