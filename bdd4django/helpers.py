# *-* coding: utf-8 *-*
from django.test import LiveServerTestCase
from django.core.management import call_command

from bdd4django import Parser
from splinter.browser import Browser
from selenium.common.exceptions import WebDriverException

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

    def step_i_fill_in_field_with_value(self, field, value):
        r'I fill in field "([^"]+)" with value "([^"]+)"'
        value = value.decode('utf-8')

        if value.startswith('eval:'):
            val_to_exec = value.split(':')[1]
            value = eval( val_to_exec )

        try:
            self.browser.find_by_id( 'id_'+field ).fill( value )
        except AttributeError, e:
            #Setar valores de multipla seleção
            mult_select = value.split('/')
            for select in mult_select:
                self.browser.find_by_id('id_'+field+'_'+select).first.click()
        except WebDriverException, e:
            #Seta valores de um combobox
            self.browser.select(field, value)
            pass

    def step_i_fill_in_fields_with_values(self, fields, values):
        r'I fill in fields "([^"]+)" with values "([^"]+)"'
        fields = fields.split(',')
        values = values.split(',')

        for i in range(0, len(fields)):
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

    """
    def step_I_see_the_error_for_field(self, error, field):
        r'I see the error "([^"]+)" for field "([^"]+)"'
        self.browser.find_by_css( '' )
    """

