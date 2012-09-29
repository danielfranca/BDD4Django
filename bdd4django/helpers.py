# *-* coding: utf-8 *-*
try:
   from django.test import LiveServerTestCase
except ImportError: #For Django 1.3
   from django_liveserver.testcases import LiveServerTestCase

from django.core.management import call_command

from bdd4django import Parser
from splinter.browser import Browser
from selenium.common.exceptions import WebDriverException, InvalidSelectorException

import time

class BDDTestCase(LiveServerTestCase):

    def extra_setup(self):
        pass

    def setUp(self, from_bdd=False):
        if from_bdd:
            self.browser = Browser()
            self.extra_setup()
        else:
            self.prepare_database()

    def prepare_database(self):
        """
        Prepare the database
        Insert/Update data
        """
        pass

    def tearDown(self, from_bdd=False):
        if from_bdd:
            self.browser.quit()

    def parse_feature_file(self, app, scenarios = None):

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

        exec 'import '+app

        absolute_path = eval('{0}.__path__'.format( app ))[0]
        Parser().parse_file('{0}/{1}.feature'.format( absolute_path, app ), scenarios).evaluate(self)

    def today(self,format='%Y-%m-%d', add_days = 0):
        import datetime
        td = datetime.date.today()
        new_dt = td

        new_dt += datetime.timedelta(days=add_days)
        return new_dt.strftime( format )

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