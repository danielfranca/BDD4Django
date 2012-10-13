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

Parse the feature file with the name <i>app</i>.feature inside your app or the <i>file_path</i> you want to evaluate specified.
You can specificy which scenarios to run with the argument <i>scenarios</i>.
<i>scenarios</i> is a tuple of scenario names or None if you want to run all the scenarios.

    def prepare_database(self):

Prepare the database, override this method to prepare your own objects in the database.
    
    def step_I_load_value_in(self, value, key):
        r'I load value "([^"]+)" in "([^"]+)"'
        
Load the value <i>value</i> in the key variable <i>key</i><br/>
You can reference a module in the <i>value</i> using the python sintax.<br/>
Ex: myapp.models.Model.objects.get(id=1)

    def step_I_see_an_object_with_values(self, object, values):
        r'I see an object "([^"]+)" with values "([^"]+)"'

Verifies the existence of an object in the database of type <i>object</i>, with values <i>values</i>.<br/>
You can reference a module in the <i>object</i> using the python sintax.<br/>
Ex: myapp.models.Model

The values parameter must be a dictionary, so in your .feature file you need to write something like this:</br>
<i>I see an object "django.contrib.auth.User" with values "{'username':'test'}"</i>

Methods from BDDTestCase
----------------------------

    def step_i_visit_url(self, url):
        r'I visit url "([^"]+)"'

Visit the <i>url</i>



    def step_I_click_the_link(self, name):
        r'I click the link "([^"]+)"'

Click the link specified by <i>name</i>.
Tries to find following the priority list:
+ by text
+ by partial text
+ by href
+ by partial href

#####

    def step_i_click_the_button(self, name):
        r'I click the button "([^"]+)"'

Click the button specified by <i>name</i>.
Tries to find following the priority list:
+ by id
+ by name
+ by text
+ by css

#####

    def step_I_login_as_with_password(self, username, password):
        r'I login as "([^"]+)" with password "([^"]+)"'

Login using the credentials <i>username</i> and <i>password</i>.
Tries to find fields with names "username" and "password" and a submit input.

    def step_i_check_fields(self, fields):
        r'I check fields "([^"]+)"'

Check/Uncheck the checkboxes separated by comma ','

    def step_i_fill_in_field_with_value(self, field, value):
        r'I fill in field "([^"]+)" with value "([^"]+)"'

Fill the field named <i>field</i> with <i>value</i>.
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

Fill a list of <i>fields</i> separated by comma with a list of <i>values</i> separated by comma, using the same criteria from step_i_fill_in_field_with_value.

    def step_i_see_the_text(self, text):
        r'I see the text "([^"]+)"'

Assert the presence of <i>text</i> in the HTML output.

    def step_i_see_the_element(self, id):
        r'I see the element "([^"]+)"'

Assert the presence of <i>element</i> in the html output.

    def step_im_redirected_to_url(self, url):
        r'I\'m redirected to url "([^"]+)"'

Assert the redirection <i>url</i>


    def step_I_see_the_element_with_class(self, name, class_name):
        r'I see the element "([^"]+)" with class "([^"]+)"'

Assert the existence of an element with <i>name</i> that has the class <i>class_name</i>

    def step_I_see_the_element_parent_with_class(self, name, class_name):
        r'I see the element "([^"]+)" parent with class "([^"]+)"'

Assert the existence of an element with <i>name</i> that one of its parents has the class <i>class_name</i>

    def step_I_see_the_field_with_value(self, field, value):
        r'I see the field "([^"]+)" with value "([^"]+)"'

Assert the existence of a <i>field</i> with value <i>value</i>

    def step_I_see_the_fields_with_values(self, fields, values):
        r'I see the fields "([^"]+)" with values "([^"]+)"'

Assert the existence of a list of <i>fields</i> separated by comma, each one of them with its correspondent value in <i>values</i>


Methods from BDDCoreTestCase
----------------------------

    def step_I_call_view(self, view):
        r'I call view "([^"]+)"'
Call the <i>view</i> with get method

    def step_I_call_view_as_user_with_password(self, view, username, password):
        r'I call view "([^"]+)" as user "([^"]+)" with password "([^"]+)"'

Call the <i>view</i> with get method and the user <i>username</i> logged with <i>password</i>

    def step_I_get_the_template_rendered(self, template_name):
        r'I get the template "([^"]+)" rendered'

Assert the righ template was rendered

    def step_I_call_view_with_data(self, view, type, data):
        r'I call view "([^"]+)" with ([^"]+) data "([^"]+)"'

Call view <i>view</i> with type using the method <i>type</i>(post or get) and with data <i>data</i>
Data is a dictionary passed between quote. Ex: "{'data1':value1,'data2':'value2'}

    def step_I_call_view_with_data_as_user_with_password(self, view, type, data, username, password):
        r'I call view "([^"]+)" with ([^"]+) data "([^"]+)" as user "([^"]+)" with password "([^"]+)"'

Call view <i>view</i> with type using the method <i>type</i>(post or get) and with data <i>data</i> and the user <i>username</i> logged with <i>password</i>
<i>data</i> is a dictionary passed between quote. Ex: "{'data1':value1,'data2':'value2'}

    def step_I_call_view_with_params(self, view, params):
        r'I call view "([^"]+)" with params "([^"]+)"'

Call view <i>view</i> with parameters <i>params</i>
<i>params</i> is a dictionary passed between quote. Ex: "{'data1':value1,'data2':'value2'}

    def step_I_call_method_with_params(self, method, params):
        r'I call method "([^"]+)" with params "([^"]+)"'

Call method <i>method</i> with parameters <i>params</i>
<i>params</i> is a dictionary passed between quote. Ex: "{'data1':value1,'data2':'value2'}

    def step_I_get_the_return(self, return_values):
        r'I get the return "([^"]+)"'

Check the return of a method call, the <i>return_values</i> parameter can be a single value or a colon separated list of values.
You can reference a module in the <i>return_values</i> using the python sintax.
Ex: myapp.utils.myobject

    def step_I_see_an_object_with_values(self, object, values):
        r'I see an object "([^"]+)" with values "([^"]+)"'

Assert the existence of the object in the database with the values <i>values</i>
<i>values</i> is a dictionary passed between quote. Ex: "{'data1':value1,'data2':'value2'}

    def step_I_get_the_context_variables_with_values(self, variables, values):
        r'I get the context variables "([^"]+)" with values "([^"]+)"'

Assert the existence of the context <i>variables</i> with <i>values</i>
<i>variables</i> and <i>values</i> are passed separated by "|"(pipe)
You can use a python statement as both of them.

    def step_I_see_the_text_in_template(self, text):
        r'I see the text "([^"]+)" in template'

Assert the existence of the <i>text</i> content in the output template

