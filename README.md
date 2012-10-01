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

Install
-------

Install it with pip:
> pip install bdd4django

Requirements
------------
+ Splinter
+ Django >= 1.4 or Django 1.3 with django-live-server

Now there's a port of django live server for Django 1.3, so you can use BDD4Django with it: https://github.com/adamcharnock/django-live-server

Usage Instructions
------------------
Create a testcase class that inherits from BDDTestCase or BDDCoreTestCase:

> Use BDDCoreTestCase as the base class if you want an off-browser test
#
> Use BDDCoreTestCase as the base class if you want an in-browser(using Splinter) test
#
> Both inherit from BDDBaseTestCase
#

Simple Examples
---------------

    from bdd4django.helpers import BDDTestCase

    class MyTests(BDDTestCase):

        def test_evaluate_file(self):
            self.parse_feature_file( 'accounts' )

#
or
#

    from bdd4django.helpers import BDDCoreTestCase

    class MyTests(BDDCoreTestCase):

        def test_evaluate_file(self):
            self.parse_feature_file( 'accounts' )


Just write a test method that calls self.parse_feature_file passing the app name as argument (The feature file must have the name "app_name.feature")

Methods from BDDBaseTestCase
----------------------------
    def extra_setup(self):

Add extra setup, this is an abstract method that you should override to run.

    def parse_feature_file(self, app=None, file_path=None, scenarios=None):

Parse the feature file with the name <b>app</b>.feature inside your app or the <b>file_path</b> you want to evaluate specified.
You can specificy which scenarios to run with the argument <b>scenarios</b>.
<b>scenarios</b> is a tuple of scenario names or None if you want to run all the scenarios.


Methods from BDDTestCase
----------------------------

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

#####

    def step_i_click_the_button(self, name):
        r'I click the button "([^"]+)"'

Click the button specified by <b>name</b>.
Tries to find following the priority list:
+ by id
+ by name
+ by text
+ by css

#####

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
This method allows a python expression as value (just put "eval:<expression>" in the value field)
Ex: I fill in field "test" with value "self.today(add_days=1)"
#
Tries to fill following the priority:
+ Simple text field
+ Multiple selection
+ Select

#####

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


    def step_I_see_the_element_with_class(self, name, class_name):
        r'I see the element "([^"]+)" with class "([^"]+)"'

Assert the existence of an element with <b>name</b> that has the class <b>class_name</b>

    def step_I_see_the_element_parent_with_class(self, name, class_name):
        r'I see the element "([^"]+)" parent with class "([^"]+)"'

Assert the existence of an element with <b>name</b> that one of its parents has the class <b>class_name</b>

    def step_I_see_the_field_with_value(self, field, value):
        r'I see the field "([^"]+)" with value "([^"]+)"'

Assert the existence of a <b>field</b> with value <b>value</b>

    def step_I_see_the_fields_with_values(self, fields, values):
        r'I see the fields "([^"]+)" with values "([^"]+)"'

Assert the existence of a list of <b>fields</b> separated by comma, each one of them with its correspondent value in <b>values</b>


Methods from BDDCoreTestCase
----------------------------

    def step_I_call_view(self, view):
        r'I call view "([^"]+)"'
Call the <b>view</b> with get method

    def step_I_call_view_as_user_with_password(self, view, username, password):
        r'I call view "([^"]+)" as user "([^"]+)" with password "([^"]+)"'

Call the <b>view</b> with get method and the user <b>username</b> logged with <b>password</b>

    def step_I_get_the_template_rendered(self, template_name):
        r'I get the template "([^"]+)" rendered'

Assert the righ template was rendered

    def step_I_call_view_with_data(self, view, type, data):
        r'I call view "([^"]+)" with ([^"]+) data "([^"]+)"'

Call view <b>view</b> with type using the method <b>type</b>(post or get) and with data <b>data</b>
Data is a dictionary passed between quote. Ex: "{'data1':value1,'data2':'value2'}

    def step_I_call_view_with_data_as_user_with_password(self, view, type, data, username, password):
        r'I call view "([^"]+)" with ([^"]+) data "([^"]+)" as user "([^"]+)" with password "([^"]+)"'

Call view <b>view</b> with type using the method <b>type</b>(post or get) and with data <b>data</b> and the user <b>username</b> logged with <b>password</b>
<b>data</b> is a dictionary passed between quote. Ex: "{'data1':value1,'data2':'value2'}

    def step_I_see_an_object_with_values(self, object, values):
        r'I see an object "([^"]+)" with values "([^"]+)"'

Assert the existence of the object in the database with the values <b>values</b>
<b>values</b> is a dictionary passed between quote. Ex: "{'data1':value1,'data2':'value2'}

    def step_I_get_the_context_variables_with_values(self, variables, values):
        r'I get the context variables "([^"]+)" with values "([^"]+)"'

Assert the existence of the context <b>variables</b> with <b>values</b>
<b>variables</b> and <b>values</b> are passed separated by "|"(pipe)
You can use a python statement as both of them.

    def step_I_see_the_text_in_template(self, text):
        r'I see the text "([^"]+)" in template'

Assert the existence of the <b>text</b> content in the output template

