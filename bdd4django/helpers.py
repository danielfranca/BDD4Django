# *-* coding: utf-8 *-*
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.core.management import call_command

from model_mommy import mommy
from morelia import Parser
from splinter.browser import Browser
from selenium.common.exceptions import WebDriverException

import time

class EurecaTest(LiveServerTestCase):

    def extra_setup(self):
        pass

    def setUp(self):
        self.browser = Browser()
        self.extra_setup()

    def tearDown(self):
        self.browser.quit()

    def parse_feature_file(self, app, scenarios = None):

        try:
            import userena
            call_command('check_permissions')
        except ImportError:
            pass

        Parser().parse_file('apps/{0}/{0}.feature'.format( app ), scenarios).evaluate(self)

    def click_element(self, find_methods, name):
        for find in find_methods:
            elements = find( name )
            if len(elements) > 0:
                elements.first.click()
                break

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
        #import ipdb; ipdb.set_trace()

        try:
            self.browser.find_by_id( 'id_'+field ).fill( value )
        except AttributeError, e:
            #Setar valores de multipla seleção
            mult_select = value.split('/')
            for select in mult_select:
                self.browser.find_by_id('id_'+field+'_'+select).first.click()
        except WebDriverException, e:
            self.browser.choose(field, value)
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
        self.assertTrue( self.browser.is_text_present(text,wait_time=10) )

    def step_i_see_the_element(self, id):
        r'I see the element "([^"]+)"'
        self.assertTrue( self.browser.is_element_present_by_id(id,wait_time=10) )

    def step_im_redirected_to_url(self, url):
        r'I\'m redirected to url "([^"]+)"'
        self.assertEqual( self.browser.url, self.live_server_url+url )

    def step_a_logged_user_(self, username):
        r'a logged user "([^"]+)"'
        user = mommy.make_one( User,username=username )
        user.set_password('abc123')
        user.is_active = True
        user.save()

        self.step_i_visit_url('/accounts/login/')
        self.step_I_login_as_with_password( username=username,password='abc123')

