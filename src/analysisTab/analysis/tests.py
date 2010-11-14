#from django.test import TestCase
import unittest

class TestTraj(unittest.TestCase):

#    def testTrajClient(self):
#        from django.test.client import Client
#        c = Client()
##        response = c.post('/login/', {'username':'john', 
##                                      'password':'smith'})
##        response.status_code
#        response = c.get('/analysis/sqeCoh/getTrajectory/')
#        print response.content
        
    def testTraj(self):
        from analysisTab.analysis.views import getTrajectory
        class request:
            path = 'dummy'
        r = request()
        response = getTrajectory(r)
        if False:
            from analysisTab.analysis.models import Trajectory
            import datetime
            t = Trajectory(filename='gulp.nc', initial_chemical_formula='Fe_2',
                           num_timesteps=100, time_step_interval=0.001,
                           total_time=0.1, creator='jbk', 
                           timestamp=datetime.datetime.now(),
                           short_description='demo trajectory')
            t.save()
        print response
        
        
if __name__=='__main__':
    unittest.main()

#class SimpleTest(TestCase):
#    def test_basic_addition(self):
#        """
#        Tests that 1 + 1 always equals 2.
#        """
#        self.failUnlessEqual(1 + 1, 2)
#
#__test__ = {"doctest": """
#Another way to test that 1 + 1 is equal to 2.
#
#>>> 1 + 1 == 2
#True
#"""}

