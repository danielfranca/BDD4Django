# *-* coding: utf-8 *-*
try:
   from django.test import LiveServerTestCase
except ImportError: #For Django 1.3
   from django_liveserver.testcases import LiveServerTestCase

from django.core.management import call_command
from django.test import TestCase
from django.core.urlresolvers import reverse

from bdd4django import Parser
from splinter.browser import Browser
from selenium.common.exceptions import WebDriverException, InvalidSelectorException

from django.conf import settings

import time

class BDDBaseTestCase():

    def extra_setup(self):
        pass

    def setUp(self, from_bdd=False):
        if from_bdd:
            if isinstance( self, BDDTestCase ):
                self.browser = Browser()
            self.extra_setup()
        else:
            self.prepare_database()

    def tearDown(self, from_bdd=False):
        if from_bdd and isinstance( self, BDDTestCase ):
            self.browser.quit()

    def prepare_database(self):
        """
        Prepare the database
        Insert/Update data
        """
        pass

    def parse_feature_file(self, app=None, file_path=None, scenarios=None):

        """
        Parse the file of BDD features
        @param app:
        @param scenarios:
        """
        try:
            import userena
            call_command('check_permissions')
        except ImportError:
            pass

        if file_path is None:
            exec 'import '+app
            file_path = eval('{0}.__path__'.format( app ))[0]
            file_path = '{0}/{1}.feature'.format( file_path, app )

        Parser().parse_file(file_path, scenarios).evaluate(self)

    def today(self,format='%Y-%m-%d', add_days = 0):
        import datetime
        td = datetime.date.today()
        new_dt = td

        new_dt += datetime.timedelta(days=add_days)
        return new_dt.strftime( format )

class BDDCoreTestCase(BDDBaseTestCase,TestCase):

    def step_I_call_view(self, view):
        r'I call view "([^"]+)"'
        self.response = self.client.get( reverse(view) )

    def step_I_call_view_as_user_with_password(self, view, username, password):
        r'I call view "([^"]+)" as user "([^"]+)" with password "([^"]+)"'
        self.client.login(username=username, password=password)
        self.step_I_call_view(view)

    def step_I_get_the_template_rendered(self, template_name):
        r'I get the template "([^"]+)" rendered'
        self.assertTemplateUsed( self.response, template_name=template_name )

    def step_I_call_view_with_data(self, view, type, data):
        r'I call view "([^"]+)" with ([^"]+) data "([^"]+)"'
        if type.lower() == 'post':
            method = self.client.post
        else:
            method = self.client.get

        data = eval( data )

        self.response = method( reverse(view), data=data )

    def step_I_call_view_with_data_as_user_with_password(self, view, type, data, username, password):
        r'I call view "([^"]+)" with ([^"]+) data "([^"]+)" as user "([^"]+)" with password "([^"]+)"'
        self.client.login(username=username, password=password)
        self.step_I_call_view_with_data( view, type, data )

    def step_I_see_an_object_with_values(self, object, values):
        r'I see an object "([^"]+)" with values "([^"]+)"'
        obj = None

        last_dot = object.rfind('.')
        if last_dot >= 0:
            modules = object[:last_dot]
            model   = object[last_dot+1:]
        else:
            app = self.__module__.split('.')[0]

            modules = app+'.models'
            model   = object

        exec( 'from {0} import {1}'.format( modules, model ) )
        exec( 'obj = '+object )
        values = eval( values )

        self.assertGreater( obj.objects.filter(**values), 0 )

    def step_I_get_the_context_variables_with_values(self, variables, values):
        r'I get the context variables "([^"]+)" with values "([^"]+)"'

        variables = variables.split('|')
        values    = values.split('|')

        len_varibales = len(variables)
        len_values     = len(values)

        if len_varibales != len_values:
            raise Exception( 'Number of variables (%i) doesn\'t match number of values (%i)' % ( len_varibales, len_values ) )

        for i in range(0, len_varibales):
            vars = variables[i].split('.')

            if len(vars) > 1:
                self.assertEqual(  eval( 'self.response.context["{0}"].{1}'.format( vars[0],'.'.join(vars[1:]) ) ),  eval(values[i]) )
            else:
                self.assertEqual(  eval( 'self.response.context["{0}"]'.format( vars[0] ) ),  eval(values[i]) )

    def step_I_see_the_text_in_template(self, text):
        r'I see the text "([^"]+)" in template'
        self.assertContains( self.response, text )



class BDDTestCase(BDDBaseTestCase, LiveServerTestCase):

    def click_element(self, find_methods, name):
        """
        Click an element

        @param find_methods:
        @param name:
        """
        for find in find_methods:
            elements = find( name )
            if len(elements) > 0:
                elements.first.click()
                return

        raise Exception( 'No element found: '+name )

    def step_i_visit_url(self, url):
        r'I visit url "([^"]+)"'
        self.browser.visit( self.live_server_url+url )

    def step_I_click_the_link(self, name):
        r'I click the link "([^"]+)"'
        find_methods = [self.browser.find_link_by_text,self.browser.find_link_by_partial_text,
                        self.browser.find_link_by_href, self.browser.find_link_by_partial_href]
        self.click_element(find_methods,name)


    def step_i_click_the_button(self, name):
        r'I click the button "([^"]+)"'
        find_methods = [self.browser.find_by_id, self.browser.find_by_name,
                        self.browser.find_link_by_text, self.browser.find_by_css]

        self.click_element(find_methods,name)


    def step_I_login_as_with_password(self, username, password):
        r'I login as "([^"]+)" with password "([^"]+)"'
        self.browser.fill( 'username', username )
        self.browser.fill( 'password', password )

        submit = self.browser.find_by_css('input[type="submit"],input[value="submit"]').first
        submit.click()

    def step_i_check_fields(self, fields):
        r'I check fields "([^"]+)"'
        fields = fields.split(',')
        for i in range(0, len(fields)):
            self.browser.find_by_id('id_'+fields[i]).first.click()

    def find_input_type(self, input):
        import re
        matches = re.search( r'(type=[\'\"][^*]+[\'\"]|<[\s]*select|<[\s]*textarea)', input.outer_html )

        if matches:
            if matches.group(0).lower().find( 'text' ) >= 0 or matches.group(0).find( 'password' ) >= 0:
                return 'TEXT'
            elif matches.group(0).lower().find( 'select' ) >= 0:
                return 'SELECT'
            elif matches.group(0).lower().find( 'radio' ) >= 0:
                return 'RADIO'
            elif matches.group(0).lower().find( 'checkbox' ) >= 0:
                return 'CHECKBOX'

        return ''

    def step_i_fill_in_field_with_value(self, field, value):
        r'I fill in field "([^"]+)" with value "([^"]+)"'

        value = value.decode('utf-8')

        if value.startswith('eval:'):
            val_to_exec = value.split(':')[1]
            value = eval( val_to_exec )

        fields = self.browser.find_by_name( field )

        if len(fields) == 0:
            raise Exception( 'Element not found with name: '+field )

        for input in fields:
            input_type = self.find_input_type( input )

            if input_type == 'TEXT':
                input.fill( value )
            elif input_type == 'SELECT':

                options = self.browser.find_by_xpath("//select[@name='{0}']/option[contains(text(),'{1}')]".format( field, value ))

                if len(options) == 0:
                    raise Exception( 'Option \'{0}\' not found for select \'{1}\': '.format( value, field ) )

                self.browser.select( field, options.first.value )

            elif input_type  == 'RADIO' and input.value in value.split('/'):
                input.check()
            elif input_type == 'CHECKBOX':
                if input.value in value.split('/'):
                    input.check( )
                elif value.upper() in ('1','TRUE','CHECKED'):
                    input.check()
                else:
                    input.uncheck()


    def step_i_fill_in_fields_with_values(self, fields, values):
        r'I fill in fields "([^"]+)" with values "([^"]+)"'
        fields = fields.split(',')
        values = values.split(',')

        len_fields = len(fields)
        len_values = len(values)

        if len_fields != len_values:
            raise Exception( 'Number of fields (%i) doesn\'t match number of values (%i)' % ( len_fields, len_values ) )

        for i in range(0, len_fields):
            time.sleep(0.5)
            self.step_i_fill_in_field_with_value( fields[i], values[i] )

    def step_i_see_the_text(self, text):
        r'I see the text "([^"]+)"'
        self.assertTrue( self.browser.is_text_present(text,wait_time=5) )

    def step_i_don_t_see_the_text(self, text):
        r'I don\'t see the text "([^"]+)"'
        self.assertFalse( self.browser.is_text_present(text,wait_time=5) )

    def step_i_see_the_element(self, id):
        r'I see the element "([^"]+)"'
        self.assertTrue( self.browser.is_element_present_by_id(id,wait_time=5) )

    def step_im_redirected_to_url(self, url):
        r'I\'m redirected to url "([^"]+)"'
        self.assertEqual( self.browser.url, self.live_server_url+url )

    def step_I_see_the_element_with_class(self, name, class_name):
        r'I see the element "([^"]+)" with class "([^"]+)"'
        elems = self.browser.find_by_name( name )

        if len(elems) == 0:
            raise Exception( 'No element found: '+name )

        self.assertTrue( elems.first.has_class(class_name) )

    def step_I_see_the_element_parent_with_class(self, name, class_name):
        r'I see the element "([^"]+)" parent with class "([^"]+)"'
        elem = self.browser.find_by_name( name )

        if len(elem) == 0:
            raise Exception( 'No element found: '+name )

        elem = elem.first.find_by_xpath('..')
        class_found = True

        while not elem.has_class(class_name):
            try:
                elem = elem.first.find_by_xpath('..')
            except InvalidSelectorException:
                class_found = False
                break

        self.assertTrue( class_found )

    def step_I_see_the_field_with_value(self, field, value):
        r'I see the field "([^"]+)" with value "([^"]+)"'
        value = value.decode('utf-8')

        values = value.split('/')

        for value in values:
            if value.startswith('eval:'):
                val_to_exec = value.split(':')[1]
                value = eval( val_to_exec )

            elements = self.browser.find_by_css( "input[name='{0}'][value='{1}']".format( field, value.encode('utf-8') ) )

            #is this a checkbox?
            if len(elements) > 0 and elements.first.outer_html.find( 'type=\'radio\'' ) >= 0:
                elements = [ elem for elem in elements if elem.checked ]

            #Maybe is a select?
            if len(elements) == 0:
                elements = [ elem for elem in self.browser.find_by_xpath( "//select[@name='{0}']/option[text() and . = ../option[@selected]]".format( field ) ) if elem.outer_html.find('selected=') > -1 and elem.text == value ]

            #or a textarea
            if len(elements) == 0:
                elements = [elem for elem in self.browser.find_by_css( "textarea[name='{0}']".format( field ) ) if elem.value == value]

            #or a checkbox
            if len(elements) == 0:
                if value == '1' or value.upper() == 'TRUE' or value.upper() == 'CHECKED':
                    value = True
                else:
                    value = False
                elements = [elem for elem in self.browser.find_by_css( "input[name='{0}']".format( field ) ) if elem.checked == value]

            if len(elements) == 0:
                raise Exception( 'Element \'{0}\' with value \'{1}\' not found'.format( field, value ) )

        return True

    def step_I_see_the_fields_with_values(self, fields, values):
        r'I see the fields "([^"]+)" with values "([^"]+)"'
        fields = fields.split(',')
        values = values.split(',')

        len_fields = len(fields)
        len_values = len(values)

        if len_fields != len_values:
            raise Exception( 'Number of fields (%i) doesn\'t match number of values (%i)' % ( len_fields, len_values ) )

        for i in range(0, len_fields):
            self.assertTrue( self.step_I_see_the_field_with_value( fields[i], values[i] ) )

