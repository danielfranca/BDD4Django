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

    class MyTests(BDDTestCase):

        def test_evaluate_file(self):
            self.parse_feature_file( 'accounts' )

Just write a test method that calls self.parse_feature_file passing the app name as argument (The feature file must have the name "app_name.feature")

Methods from BDDTestCase
----------------------------
    def extra_setup(self):

Add extra setup, this is an abstract method that you should override to run.

    def parse_feature_file(self, app, scenarios = None):

Parse the feature file with the name <b>app</b>.feature inside your app.
You can specificy which scenarios to run with the argument <b>scenarios</b>.
<b>scenarios</b> is a tuple of scenario names or None if you want to run all the scenarios.

    def step_i_visit_url(self, url):
        r'I visit url "([^"]+)"'

Visit the <b>url</b>



    def step_I_click_the_link(self, name):
        r'I click the link "([^"]+)"'

Click the link specified by <b>name</b>.
Tries to find following the priority list:
+ by text
+ by partial text
+ by href
+ by partial href



    def step_i_click_the_button(self, name):
        r'I click the button "([^"]+)"'

Click the button specified by <b>name</b>.
Tries to find following the priority list:
+ by id
+ by name
+ by text
+ by css

    def step_I_login_as_with_password(self, username, password):
        r'I login as "([^"]+)" with password "([^"]+)"'

Login using the credentials <b>username</b> and <b>password</b>.
Tries to find fields with names "username" and "password" and a submit input.

    def step_i_check_fields(self, fields):
        r'I check fields "([^"]+)"'

Check/Uncheck the checkboxes separated by comma ','

    def step_i_fill_in_field_with_value(self, field, value):
        r'I fill in field "([^"]+)" with value "([^"]+)"'

Fill the field named <b>field</b> with <b>value</b>.
Tries to fill following the priority:
+ Simple text field
+ Multiple selection
+ Radio

    def step_i_fill_in_fields_with_values(self, fields, values):
        r'I fill in fields "([^"]+)" with values "([^"]+)"'

Fill a list of <b>fields</b> separated by comma with a list of <b>values</b> separated by comma, using the same criteria from step_i_fill_in_field_with_value.

    def step_i_see_the_text(self, text):
        r'I see the text "([^"]+)"'

Assert the presence of <b>text</b> in the HTML output.

    def step_i_see_the_element(self, id):
        r'I see the element "([^"]+)"'

Assert the presence of <b>element</b> in the html output.

    def step_im_redirected_to_url(self, url):
        r'I\'m redirected to url "([^"]+)"'

Assert the redirection <b>url</b>
