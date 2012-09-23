BDD4Django
=============

BDD4DJango unifies 4 elements:
+ Django
+ Morelia Viridis (with added features and better Django integration)
+ Splinter
+ A TestCase class with helper methods to run Django tests.

Morelia *viridis*** is fully documented on the "C2 Wiki":http://c2.com/cgi/wiki?MoreliaViridis

Splinter is fully documented here http://splinter.cobrateam.info/docs/

BDD4Django comes with a TestCase class that inherits Django LiveServerTestCase, this allow the tests to be executed in a browser running on the test database.

Usage Instructions
------------------
Create a testcase class that inherits from BDDTestCase:

from bdd4django.helpers import BDDTestCase

> class MyTests(BDDTestCase):

>     def test_evaluate_file(self):
>         self.parse_feature_file( 'accounts' )

Just write a test method that calls self.parse_feature_file passing the app name as argument (The feature file must have the name "app_name.feature")

All methods from BDDTestCase
----------------------------
