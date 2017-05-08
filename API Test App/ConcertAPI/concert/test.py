import unittest
#import views
import os
import commands

class TestAPIMethods(unittest.TestCase):
    
    def test_update_concert(self):
        result = commands.getoutput('http --json PUT http://127.0.0.1:8000/concert/12/ artist="Atena" date="2017-04-28" location="BogaziciUniTasoda"')
        
     
        expected = '{' + '"id": 12, ' + '"artist": "Atena", ' + '"location": "BogaziciUniTasoda", ' + '"date": "2017-04-28", ' + '"minprice": 0, ' + '"maxprice": 0' + '}'

        self.assertEqual(result, expected) # result should be equal to expected

if __name__ == '__main__':
    unittest.main()
